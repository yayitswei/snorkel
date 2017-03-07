# Semparser
from semparse_examples import get_examples
from load_external_annotations import load_external_labels
from cdr_lfs import get_cdr_lfs, LF_closer_chem, LF_closer_dis
from utils import TaggerOneTagger

# Snorkel
from snorkel.models import Document, Sentence, candidate_subclass
from snorkel.parser import CorpusParser, TSVDocPreprocessor, XMLMultiDocPreprocessor
from snorkel.candidates import Ngrams, CandidateExtractor, PretaggedCandidateExtractor
from snorkel.matchers import PersonMatcher
from snorkel.annotations import (FeatureAnnotator, LabelAnnotator, 
    save_marginals, load_marginals, load_gold_labels)
from snorkel.learning import GenerativeModel, SparseLogisticRegression
from snorkel.learning import RandomSearch, ListParameter, RangeParameter
from snorkel.learning.utils import MentionScorer
from snorkel.learning.structure import DependencySelector
from snorkel.semantic import SemanticParser

# Python
import matplotlib.pyplot as plt
import os
import csv
import cPickle
import bz2

TRAIN = 0
DEV = 1
TEST = 2

class SnorkelModel(object):
    def __init__(self, session, candidate_class, splits=3, parallelism=1, seed=0, verbose=True):
        self.session = session
        self.candidate_class = candidate_class
        self.splits = splits
        self.parallelism = parallelism
        self.seed = seed
        self.verbose = verbose
        self.featurizer = None
        self.labeler = None

    def parse(self, doc_preprocessor, fn=None, clear=True):
        corpus_parser = CorpusParser(fn=fn)
        corpus_parser.apply(doc_preprocessor, count=doc_preprocessor.max_docs, 
                            parallelism=self.parallelism, clear=clear)

    def extract(self, cand_extractor, sents, split, clear=True):
        cand_extractor.apply(sents, split=split, parallelism=self.parallelism, clear=clear)

    def load_gold(self):
        raise NotImplementedError

    def featurize(self, featurizer, split):
        if split == TRAIN:
            F = featurizer.apply(split=split, parallelism=self.parallelism)
        else:
            F = featurizer.apply_existing(split=split, parallelism=self.parallelism)
        return F

    def label(self, labeler, split):
        if split == TRAIN:
            L = labeler.apply(split=split, parallelism=self.parallelism)
        else:
            L = labeler.apply_existing(split=split, parallelism=self.parallelism)
        return L

    def generative(self):
        raise NotImplementedError
    
    def discriminative(self):
        raise NotImplementedError

class CDRModel(SnorkelModel):
    def __init__(self, session, candidate_class, splits=3, parallelism=1, seed=0, verbose=True):
        SnorkelModel.__init__(
            self, 
            session, 
            candidate_class=candidate_class, 
            splits=splits,
            parallelism=parallelism, 
            seed=seed, 
            verbose=verbose)

    def parse(self, file_path='data/CDR.BioC.xml', max_docs=float('inf'), clear=True):
        doc_preprocessor = XMLMultiDocPreprocessor(
            path=file_path,
            doc='.//document',
            text='.//passage/text/text()',
            id='.//id/text()',
            max_docs=max_docs
        )
        tagger_one = TaggerOneTagger()
        fn=tagger_one.tag
        SnorkelModel.parse(self, doc_preprocessor, fn=fn, clear=clear)
        if self.verbose:
            print("Documents: {}".format(self.session.query(Document).count()))
            print("Sentences: {}".format(self.session.query(Sentence).count()))

    def extract(self, clear=True):
        with open('data/doc_ids.pkl', 'rb') as f:
            train_ids, dev_ids, test_ids = cPickle.load(f)
        train_ids, dev_ids, test_ids = set(train_ids), set(dev_ids), set(test_ids)

        train_sents, dev_sents, test_sents = set(), set(), set()
        docs = self.session.query(Document).order_by(Document.name).all()
        for i, doc in enumerate(docs):
            for s in doc.sentences:
                if doc.name in train_ids:
                    train_sents.add(s)
                elif doc.name in dev_ids:
                    dev_sents.add(s)
                elif doc.name in test_ids:
                    test_sents.add(s)
                else:
                    raise Exception('ID <{0}> not found in any id set'.format(doc.name))

        candidate_extractor = PretaggedCandidateExtractor(self.candidate_class, ['Chemical', 'Disease'])
        for split, sents in enumerate([train_sents, dev_sents, test_sents]):
            if len(sents) > 0:
                SnorkelModel.extract(self, candidate_extractor, sents, split=split, clear=clear)
                nCandidates = self.session.query(self.candidate_class).filter(self.candidate_class.split == split).count()
                if self.verbose:
                    print("Candidates [Split {}]: {}".format(split, nCandidates))

    def load_gold(self):
        for split in range(self.splits):
            print("Split {}:".format(split))
            load_external_labels(self.session, self.candidate_class, split=split, annotator='gold')

    def featurize(self):
        featurizer = FeatureAnnotator()
        for split in range(self.splits):
            F = SnorkelModel.featurize(self, featurizer, split)
            nCandidates, nFeatures = F.shape
            if self.verbose:
                print("Featurized split {}: ({},{}) sparse matrix".format(split, nCandidates, nFeatures))
        self.featurizer = featurizer
    
    def _get_LFs(self, source):
        if source == 'py':
            LFs = get_cdr_lfs()
        elif source == 'nl':
            with bz2.BZ2File('data/ctd.pkl.bz2', 'rb') as ctd_f:
                ctd_unspecified, ctd_therapy, ctd_marker = cPickle.load(ctd_f)
            user_lists = {
                'uncertain': ['combin', 'possible', 'unlikely'],
                'causal': ['causes', 'caused', 'induce', 'induces', 'induced', 'associated with'],
                'treat': ['treat', 'effective', 'prevent', 'resistant', 'slow', 'promise', 'therap'],
                'procedure': ['inject', 'administrat'],
                'patient': ['in a patient with', 'in patients with'],
                'weak': ['none', 'although', 'was carried out', 'was conducted', 'seems', 
                        'suggests', 'risk', 'implicated', 'the aim', 'to investigate',
                        'to assess', 'to study'],
                'ctd_unspecified': ctd_unspecified,
                'ctd_therapy': ctd_therapy,
                'ctd_marker': ctd_marker,
            }
            train_cands = self.session.query(self.candidate_class).filter(self.candidate_class.split == 0).all()
            examples = get_examples('semparse_cdr', train_cands)
            sp = SemanticParser(self.candidate_class, user_lists)
            sp.evaluate(examples,\
                        show_everything=False,\
                        show_explanation=False,\
                        show_candidate=False,\
                        show_sentence=False,\
                        show_parse=False,\
                        show_passing=False,\
                        show_correct=False,\
                        pseudo_python=False,\
                        only=[])
            (correct, passing, failing, redundant, erroring, unknown) = sp.LFs
            LFs = correct
            LFs = sorted(LFs + [LF_closer_chem, LF_closer_dis], key=lambda x: x.__name__)
        else:
            raise Exception("Argument for 'lfs' must be in {'py', 'nl'}")
        return LFs

    def label(self, source='py'):
        LFs = self._get_LFs(source)
        labeler = LabelAnnotator(f=LFs)
        for split in range(self.splits):
            L = SnorkelModel.label(self, labeler, split)
            nCandidates, nLabels = L.shape
            if self.verbose:
                print("Labeled split {}: ({},{}) sparse matrix (nnz = {})".format(TRAIN, nCandidates, nLabels, L.nnz))
        self.labeler = labeler

    def generative(self, lfs='py', train_acc=False, model_dep=False, threshold=(1.0/3.0)):
        L_train = self.labeler.load_matrix(self.session, split=TRAIN)
        
        if model_dep:
            ds = DependencySelector()
            deps = ds.select(L_train, threshold=threshold)
        else:
            deps = ()
    
        gen_model = GenerativeModel(lf_propensity=True)
        gen_model.train(
            L_train, deps=deps, epochs=20, decay=0.95, 
            step_size=0.1/L_train.shape[0], init_acc=2.0, reg_param=0.0)

        train_marginals = gen_model.marginals(L_train)
        save_marginals(self.session, L_train, train_marginals)

        if self.verbose:
            # Display marginals
            plt.hist(train_marginals, bins=20)
            plt.show()
            
        # Display LF accuracies
        if train_acc:
            L = self.labeler.load_matrix(self.session, split=TRAIN)
            L_gold = load_gold_labels(self.session, annotator_name='gold', split=TRAIN)
        else:
            L = self.labeler.load_matrix(self.session, split=DEV)
            L_gold = load_gold_labels(self.session, annotator_name='gold', split=DEV)
        self.LF_stats = L.lf_stats(self.session, L_gold, gen_model.weights.lf_accuracy())

    def discriminative(self, model='logreg', search_n=20):

        train_marginals = load_marginals(self.session, split=TRAIN)

        # L_gold_train = load_gold_labels(self.session, annotator_name='gold', split=TRAIN)
        L_gold_dev = load_gold_labels(self.session, annotator_name='gold', split=DEV)

        if model=='logreg':
            if not self.featurizer:
                self.featurizer = FeatureAnnotator()
            F_train =  self.featurizer.load_matrix(self.session, split=TRAIN)

            rate_param = RangeParameter('lr', 1e-6, 1e-2, step=1, log_base=10)
            l1_param  = RangeParameter('l1_penalty', 1e-6, 1e-2, step=1, log_base=10)
            l2_param  = RangeParameter('l2_penalty', 1e-6, 1e-2, step=1, log_base=10)
        
            disc_model = SparseLogisticRegression()
            searcher = RandomSearch(self.session, disc_model, F_train, train_marginals, 
                                    [rate_param, l1_param, l2_param], n=search_n)

            print("\nRandom Search:")
            F_dev =  self.featurizer.load_matrix(self.session, split=DEV)
            search_stats = searcher.fit(F_dev, L_gold_dev, n_epochs=50, rebalance=True, print_freq=25)
            if self.verbose:
                print(search_stats)

            print("\nEvaluation:")
            TP, FP, TN, FN = disc_model.score(self.session, F_dev, L_gold_dev)