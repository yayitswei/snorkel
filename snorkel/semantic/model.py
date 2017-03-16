# Semparser
from semparse_examples import get_examples
from load_external_annotations import load_external_labels
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
from snorkel.learning.utils import MentionScorer, training_set_summary_stats
from snorkel.learning.structure import DependencySelector
from snorkel.semantic import SemanticParser

# Python
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import csv
import cPickle
import bz2

TRAIN = 0
DEV = 1
TEST = 2

class SnorkelModel(object):
    def __init__(self, session, candidate_class, **kwargs):
        self.session = session
        self.candidate_class = candidate_class

        self.splits = kwargs.get('splits', 3)
        self.parallelism = kwargs.get('parallelism', 1)
        self.seed = kwargs.get('seed', 0)
        self.verbose = kwargs.get('verbose', True)

        self.LFs = None
        self.labeler = None
        self.featurizer = None

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
    def __init__(self, session, candidate_class, **kwargs):
        self.traditional = kwargs['traditional']
        self.max_train = kwargs['max_train']
        SnorkelModel.__init__(self, session, candidate_class, **kwargs)

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
            if len(sents) > 0 and split < self.splits:
                SnorkelModel.extract(self, candidate_extractor, sents, split=split, clear=clear)
                nCandidates = self.session.query(self.candidate_class).filter(self.candidate_class.split == split).count()
                if self.verbose:
                    print("Candidates [Split {}]: {}".format(split, nCandidates))

    def load_gold(self, split=None):
        if not split:
            splits = range(self.splits)
        else:
            splits = [split] if not isinstance(split, list) else split
        for split in splits:
            print("Split {}:".format(split))
            load_external_labels(self.session, self.candidate_class, split=split, annotator='gold')

    def featurize(self):
        featurizer = FeatureAnnotator()
        for split in range(self.splits):
            F = SnorkelModel.featurize(self, featurizer, split)
            nCandidates, nFeatures = F.shape
            if self.verbose:
                print("\nFeaturized split {}: ({},{}) sparse (nnz = {})".format(split, nCandidates, nFeatures, F.nnz))
        self.featurizer = featurizer

    def generate_lfs(self, source='py', include=[], max_lfs=None, remove_paren=True):
        if source == 'py':
            from cdr_lfs import get_cdr_lfs
            LFs = get_cdr_lfs()
        elif source == 'nl':
            with bz2.BZ2File(os.environ['SNORKELHOME'] + '/tutorials/cdr/data/ctd.pkl.bz2', 'rb') as ctd_f:
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
            sp.evaluate(examples,
                        show_everything=False,
                        show_explanation=False,
                        show_candidate=False,
                        show_sentence=False,
                        show_parse=False,
                        show_passing=False,
                        show_correct=False,
                        pseudo_python=False,
                        remove_paren=remove_paren,
                        only=[])
            (correct, passing, failing, redundant, erroring, unknown) = sp.LFs
            LFs = []
            for (name, lf_group) in [('correct', correct),
                                     ('passing', passing),
                                     ('failing', failing),
                                     ('erroring', erroring),
                                     ('unkonwn', unknown)]:
                if name in include:
                    LFs += lf_group
                else:
                    if len(lf_group) > 0:
                        print("Discarding {0} {1} LFs...".format(len(lf_group), name))
            from cdr_lfs import LF_closer_chem, LF_closer_dis
            LFs = sorted(LFs + [LF_closer_chem, LF_closer_dis], key=lambda x: x.__name__)
        else:
            raise Exception("Argument for 'lfs' must be in {'py', 'nl'}")
        if max_lfs:
            random.shuffle(LFs)
            LFs = LFs[:max_lfs]
        self.LFs = LFs

    def label(self):
        if self.LFs is None:
            raise ValueError("Must run generate_LFs() before calling generative model.")        
        labeler = LabelAnnotator(f=self.LFs)
        for split in range(self.splits):
            L = SnorkelModel.label(self, labeler, split)
            nCandidates, nLabels = L.shape
            if self.verbose:
                print("\nLabeled split {}: ({},{}) sparse (nnz = {})".format(split, nCandidates, nLabels, L.nnz))
                training_set_summary_stats(L, return_vals=False, verbose=True)
        self.labeler = labeler

    def supervise(self, lfs='py', 
                   model_dep=False, 
                   majority_vote=False, 
                   empirical_from_train=False, 
                   threshold=(1.0/3.0),
                   display_correlation=False):
        if not self.labeler:
            self.labeler = LabelAnnotator(f=None)
        L_train = self.labeler.load_matrix(self.session, split=TRAIN)
        # TEMP:
        # L_train = self.labeler.load_matrix(self.session, split=DEV) # NOTE: this is temporary hack

        if self.traditional:
            # Do traditional supervision with hard labels
            L_gold_train = load_gold_labels(self.session, annotator_name='gold', split=TRAIN)
            train_marginals = np.array(L_gold_train.todense()).reshape((L_gold_train.shape[0],))
            train_marginals[train_marginals==-1] = 0
        else:
            if majority_vote:
                train_marginals = np.where(np.ravel(np.sum(L_train, axis=1)) <= 0, 0.0, 1.0)
            else:
                if model_dep:
                    ds = DependencySelector()
                    deps = ds.select(L_train, threshold=threshold)
                    if self.verbose:
                        self.display_dependencies(deps)
                else:
                    deps = ()
            
                gen_model = GenerativeModel(lf_propensity=True)
                gen_model.train(
                    L_train, deps=deps, epochs=20, decay=0.95, 
                    step_size=0.1/L_train.shape[0], init_acc=2.0, reg_param=0.0)

                train_marginals = gen_model.marginals(L_train)
                
            if majority_vote:
                self.LF_stats = None
            else:
                if self.verbose:
                    if empirical_from_train:
                        L = self.labeler.load_matrix(self.session, split=TRAIN)
                        L_gold = load_gold_labels(self.session, annotator_name='gold', split=TRAIN)
                    else:
                        L = self.labeler.load_matrix(self.session, split=DEV)
                        L_gold = load_gold_labels(self.session, annotator_name='gold', split=DEV)
                    self.LF_stats = L.lf_stats(self.session, L_gold, gen_model.weights.lf_accuracy())
                    if display_correlation:
                        self.display_accuracy_correlation()
            
        save_marginals(self.session, L_train, train_marginals)

        if self.verbose:
            # Display marginals
            plt.hist(train_marginals, bins=20)
            plt.show()

    def classify(self, model='logreg', search_n=20, 
                       lr=0.01, l1_penalty=0.0, l2_penalty=0.0, 
                       n_epochs=50, rebalance=True, print_freq=25):

        train_marginals = load_marginals(self.session, split=TRAIN)

        if self.splits > DEV:
            L_gold_dev = load_gold_labels(self.session, annotator_name='gold', split=DEV)
        if self.splits > TEST:
            L_gold_test = load_gold_labels(self.session, annotator_name='gold', split=TEST)
        # dev = self.session.query(self.candidate_class).filter(self.candidate_class.split == 1).all()
        # if dev[0] != L_gold_dev.get_candidate(self.session, 0):
        #     print("FAILING!")
        # else:
        #     print("PASSING!")

        if model=='logreg':
            disc_model = SparseLogisticRegression()
            # TEMP
            self.model = disc_model
            # TEMP

            if not self.featurizer:
                self.featurizer = FeatureAnnotator()
            if self.splits > TRAIN:
                F_train =  self.featurizer.load_matrix(self.session, split=TRAIN)
            if self.splits > DEV:
                F_dev =  self.featurizer.load_matrix(self.session, split=DEV)
            if self.splits > TEST:
                F_test =  self.featurizer.load_matrix(self.session, split=TEST)
            # TEMP
            # import pdb; pdb.set_trace()
            # print(hash(F_dev))
            # TEMP

            if self.traditional:
                train_size = self.traditional
                F_train = F_train[:train_size, :]
                train_marginals = train_marginals[:train_size]
                print("Using {0} hard-labeled examples for supervision\n".format(train_marginals.shape[0]))

            if search_n > 1:
                rate_param = RangeParameter('lr', 1e-6, 1e-1, step=1, log_base=10)
                l1_param  = RangeParameter('l1_penalty', 1e-6, 1e-1, step=1, log_base=10)
                l2_param  = RangeParameter('l2_penalty', 1e-6, 1e-1, step=1, log_base=10)
            
                searcher = RandomSearch(self.session, disc_model, F_train, train_marginals, 
                                        [rate_param, l1_param, l2_param], n=search_n)

                print("\nRandom Search:")
                search_stats = searcher.fit(F_dev, L_gold_dev, n_epochs=n_epochs, 
                                            rebalance=rebalance, print_freq=print_freq)

                if self.verbose:
                    print(search_stats)
                
                disc_model = searcher.model
                    
            else:
                disc_model.train(F_train, train_marginals, 
                                 lr=lr, l1_penalty=l1_penalty, l2_penalty=l2_penalty,
                                 n_epochs=n_epochs, rebalance=rebalance)
            
            if self.splits > DEV:
                print("\nDev:")
                TP, FP, TN, FN = disc_model.score(self.session, F_dev, L_gold_dev, train_marginals=train_marginals)
            
            if self.splits > TEST:
                print("\nTest:")
                TP, FP, TN, FN = disc_model.score(self.session, F_test, L_gold_test, train_marginals=train_marginals)

        else:
            raise NotImplementedError

    def display_accuracy_correlation(self):
        empirical = self.LF_stats['Empirical Acc.'].get_values()
        learned = self.LF_stats['Learned Acc.'].get_values()
        conflict = self.LF_stats['Conflicts'].get_values()
        N = len(learned)
        colors = np.random.rand(N)
        area = np.pi * (30 * conflict)**2  # 0 to 30 point radii
        plt.scatter(empirical, learned, s=area, c=colors, alpha=0.5)
        plt.xlabel('empirical')
        plt.ylabel('learned')
        plt.show()

    def display_dependencies(self, deps_encoded):
        dep_names = {
            0: 'DEP_SIMILAR',
            1: 'DEP_FIXING',
            2: 'DEP_REINFORCING',
            3: 'DEP_EXCLUSIVE',
        }
        LF_names = {i:lf.__name__ for i, lf in enumerate(self.LFs)}
        deps_decoded = []
        for dep in deps_encoded:
            (lf1, lf2, d) = dep
            deps_decoded.append((LF_names[lf1], LF_names[lf2], dep_names[d]))
        for dep in sorted(deps_decoded):
            (lf1, lf2, d) = dep
            print('{:16}: ({}, {})'.format(d, lf1, lf2))

            # lfs = sorted([lf1, lf2])
            # deps_decoded.append((LF_names[lfs[0]], LF_names[lfs[1]], dep_names[d]))
        # for dep in sorted(list(set(deps_decoded))):
        #     (lf1, lf2, d) = dep
        #     print('{:16}: ({}, {})'.format(d, lf1, lf2))