from snorkel.models import Document, Sentence, candidate_subclass
from snorkel.parser import CorpusParser, TSVDocPreprocessor, XMLMultiDocPreprocessor
from snorkel.candidates import Ngrams, CandidateExtractor, PretaggedCandidateExtractor
from snorkel.matchers import PersonMatcher
from snorkel.annotations import FeatureAnnotator, LabelAnnotator

import os
import csv
import cPickle

class SnorkelModel(object):
    def __init__(self, session, parallelism=1, seed=0, verbose=True):
        self.session = session
        self.parallelism = parallelism
        self.seed = seed
        self.verbose = verbose

    def parse(self, doc_preprocessor, fn=None, clear=True):
        corpus_parser = CorpusParser(fn=fn)
        corpus_parser.apply(doc_preprocessor, count=doc_preprocessor.max_docs, 
                            parallelism=self.parallelism, clear=clear)

    def extract(self, cand_extractor, sents, split=0, clear=True):
        cand_extractor.apply(sents, split=split, parallelism=self.parallelism, clear=clear)

    def load_gold(self):
        raise NotImplementedError

    def featurize(self):
        raise NotImplementedError

    def label(self):
        raise NotImplementedError

    def classify(self):
        raise NotImplementedError

class CDRModel(SnorkelModel):
    def __init__(self, session, parallelism=1, seed=0, verbose=True):
        from snorkel.semantic import SemanticParser
        from utils import TaggerOneTagger
        from load_external_annotations import load_external_labels
        from cdr_lfs import get_cdr_lfs
        SnorkelModel.init(self, session, parallelism, seed, verbose)

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

    def extract(self, candidate_class, clear=True):
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

        candidate_extractor = PretaggedCandidateExtractor(candidate_class, ['Chemical', 'Disease'])
        for k, sents in enumerate([train_sents, dev_sents, test_sents]):
            SnorkelModel.extract(self, candidate_extractor, sents, split=k, clear=clear)
            if self.verbose:
                print("Candidates: {}".format(
                    self.session.query(candidate_class).filter(candidate_class.split == k).count()))

    def load_gold(self, candidate_class):
        for k in range(3):
            load_external_labels(self.session, candidate_class, split=k, annotator='gold')

    def featurize(self):
        featurizer = FeatureAnnotator()
        for k in range(3):
            if k == 0:
                F = featurizer.apply(split=k, parallelism=self.parallelism)
            else:
                F = featurizer.apply_existing(split=k, parallelism=self.parallelism)
            nCandidates, nFeatures = F.shape
            print("Featurized split {}: ({},{}) sparse matrix".format(k, nCandidates, nFeatures))

    def label(self, lfs='python'):
        if lfs == 'python':
            LFs = get_cdr_lfs()
        else:
            raise NotImplementedError
            # get it from the user (with candidates)
            # sp = SemanticParser(candidate_class, user_lists, absorb=False)

        labeler = LabelAnnotator(f=LFs)
        L_train = labeler.apply(split=0, parallelism=self.parallelism)
        if self.verbose:
            return L_train.lf_stats(self.session)



# ### NOTE: THIS IS LIKELY BROKEN
# class SpouseModel(SnorkelModel):
#     def parse(self, file_path, max_docs=float('inf'), clear=True):
#         doc_preprocessor = TSVDocPreprocessor(file_path, max_docs=max_docs)
#         SnorkelModel.parse(self, doc_preprocessor, clear=clear)
#         self.dev_path = file_path
#         # doc_preprocessor = TSVDocPreprocessor(dev_path, max_docs=max_dev)
#         # SnorkelModel.parse(self, doc_preprocessor, clear=False)
#         # if self.verbose:
#         #     nDocs = self.session.query(Document).count()
#         #     nSent = self.session.query(Sentence).count()
#         #     nDevDocs = nDocs - nTrainDocs
#         #     nDevSent = nSent - nTrainSent
#         #     print "Split 0: {} Documents, {} Sentences".format(nTrainDocs, nTrainSent)
#         #     print "Split 1: {} Documents, {} Sentences".format(nDevDocs, nDevSent)

#     def extract(self, split=0, clear=True):
#         def number_of_people(sentence):
#             active_sequence = False
#             count = 0
#             for tag in sentence.ner_tags:
#                 if tag == 'PERSON' and not active_sequence:
#                     active_sequence = True
#                     count += 1
#                 elif tag != 'PERSON' and active_sequence:
#                     active_sequence = False
#             return count

#         def get_dev_doc_names():
#             # TEMP
#             self.dev_path = 'data/articles_dev.tsv'
#             # TEMP
#             dev_doc_names = set()
#             with open(self.dev_path) as csvin:
#                 reader = csv.reader(csvin, delimiter='\t')
#                 for row in reader:
#                     doc, _ = row
#                     dev_doc_names.add(doc)
#             return dev_doc_names

#         Spouse = candidate_subclass('Spouse', ['person1', 'person2'])
#         ngrams         = Ngrams(n_max=3)
#         person_matcher = PersonMatcher(longest_match_only=True)
#         cand_extractor = CandidateExtractor(Spouse, 
#                                             [ngrams, ngrams], 
#                                             [person_matcher, person_matcher],
#                                             symmetric_relations=False)
        
#         dev_doc_names = get_dev_doc_names()
#         docs = self.session.query(Document).order_by(Document.name).all()
#         train_sents = set()
#         dev_sents = set()
#         for doc in docs:
#             if doc.name in dev_doc_names:
#                 sents = dev_sents
#             else:
#                 sents = train_sents
#             for s in doc.sentences:
#                 if number_of_people(s) < 5:
#                     sents.add(s)
#         SnorkelModel.extract(self, cand_extractor, train_sents, split=0)
#         SnorkelModel.extract(self, cand_extractor, dev_sents, split=1)
        
#         if self.verbose:
#             for split in [0, 1]:
#                 nCandidates = self.session.query(Spouse).filter(Spouse.split == split).count()
#                 print "Split {}: {} Candidates".format(split, nCandidates)

#     def load_gold(self):
#         load_external_labels(self.session, Spouse, annotator_name='gold')

#     def featurize(self):   
#         featurizer = FeatureAnnotator()
