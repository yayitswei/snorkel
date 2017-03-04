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
