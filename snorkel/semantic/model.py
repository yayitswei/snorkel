from snorkel import SnorkelSession
from snorkel.models import Document, Sentence, candidate_subclass
from snorkel.parser import TSVDocPreprocessor, CorpusParser
from snorkel.candidates import Ngrams, CandidateExtractor
from snorkel.matchers import PersonMatcher
from snorkel.annotations import FeatureAnnotator

from load_external_annotations import load_external_labels

import os
import csv

class SnorkelModel(object):
    def __init__(self, db=None, parallelism=1, seed=0, verbose=True):
        if db:
            os.environ['SNORKELDB'] = db
        self.db = db
        self.session = SnorkelSession()
        self.parallelism = parallelism
        self.verbose = verbose

    def parse(self, doc_preprocessor, clear=True):
        corpus_parser = CorpusParser()
        corpus_parser.apply(doc_preprocessor, parallelism=self.parallelism, clear=clear)
    
    def extract(self, cand_extractor, sents, split=0, clear=True):
        cand_extractor.apply(sents, split=split, parallelism=self.parallelism, clear=clear)

    def annotate(self):
        raise NotImplementedError

    def featurize(self):
        raise NotImplementedError

    def label(self):
        raise NotImplementedError

    def classify(self):
        raise NotImplementedError


Spouse = candidate_subclass('Spouse', ['person1', 'person2'])

class SpouseModel(SnorkelModel):
    def parse(self, train_path, max_train, dev_path, max_dev):
        self.train_path = train_path
        self.dev_path = dev_path
        doc_preprocessor = TSVDocPreprocessor(train_path, max_docs=max_train)
        SnorkelModel.parse(self, doc_preprocessor, clear=True)
        if self.verbose:
            nTrainDocs = self.session.query(Document).count()
            nTrainSent = self.session.query(Sentence).count()
        doc_preprocessor = TSVDocPreprocessor(dev_path, max_docs=max_dev)
        SnorkelModel.parse(self, doc_preprocessor, clear=False)
        if self.verbose:
            nDocs = self.session.query(Document).count()
            nSent = self.session.query(Sentence).count()
            nDevDocs = nDocs - nTrainDocs
            nDevSent = nSent - nTrainSent
            print "Split 0: {} Documents, {} Sentences".format(nTrainDocs, nTrainSent)
            print "Split 1: {} Documents, {} Sentences".format(nDevDocs, nDevSent)

    def extract(self, split=0, clear=True):
        def number_of_people(sentence):
            active_sequence = False
            count = 0
            for tag in sentence.ner_tags:
                if tag == 'PERSON' and not active_sequence:
                    active_sequence = True
                    count += 1
                elif tag != 'PERSON' and active_sequence:
                    active_sequence = False
            return count

        def get_dev_doc_names():
            dev_doc_names = set()
            with open(os.environ['SNORKELHOME'] + '/tutorials/semparse/{}'.format(self.dev_path)) as csvin:
                reader = csv.reader(csvin, delimiter='\t')
                for row in reader:
                    doc, _ = row
                    dev_doc_names.add(doc)
            return dev_doc_names

        ngrams         = Ngrams(n_max=3)
        person_matcher = PersonMatcher(longest_match_only=True)
        cand_extractor = CandidateExtractor(Spouse, 
                                            [ngrams, ngrams], 
                                            [person_matcher, person_matcher],
                                            symmetric_relations=False)
        
        dev_doc_names = get_dev_doc_names()
        docs = self.session.query(Document).order_by(Document.name).all()
        train_sents = set()
        dev_sents = set()
        for doc in docs:
            if doc.name in dev_doc_names:
                sents = dev_sents
            else:
                sents = train_sents
            for s in doc.sentences:
                if number_of_people(s) < 5:
                    sents.add(s)
        SnorkelModel.extract(self, cand_extractor, train_sents, split=0)
        SnorkelModel.extract(self, cand_extractor, dev_sents, split=1)
        
        if self.verbose:
            for split in [0, 1]:
                nCandidates = self.session.query(Spouse).filter(Spouse.split == split).count()
                print "Split {}: {} Candidates".format(split, nCandidates)

    def annotate(self):
        load_external_labels(self.session, Spouse, annotator_name='gold')

    def featurize(self):   
        featurizer = FeatureAnnotator()