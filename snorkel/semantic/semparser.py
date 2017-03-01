from grammar import Grammar
from ricky import snorkel_rules, snorkel_ops
from annotator import *

from pandas import DataFrame, Series

class SemanticParser():
    def __init__(self, candidate_class, user_lists={}, absorb=True):
        annotators = [TokenAnnotator(), PunctuationAnnotator(), IntegerAnnotator()]
        self.grammar = Grammar(rules=snorkel_rules, 
                               ops=snorkel_ops, 
                               candidate_class=candidate_class,
                               user_lists=user_lists,
                               annotators=annotators,
                               absorb=absorb)
        self.explanation_counter = 0
        self.LFs = tuple([None] * 6)

    def preprocess(self, explanations):
        stopwords = (['is', 'are', 'be', 'comes', 'appears', 'occurs',
                      'a', 'an', 'the', 
                      'to', 'of', 'from'])
        for explanation in explanations:
            explanation = explanation.replace("'", '"')
            words = explanation.split()
            yield ' '.join([w for w in words if w not in stopwords])

    def parse(self, explanations, names=None, verbose=False, return_parses=False):
        """
        Accepts natural language explanations and returns parses
        """
        LFs = []
        parses = []
        explanations = explanations if isinstance(explanations, list) else [explanations]
        names = names if isinstance(names, list) else [names]
        for i, exp in enumerate(self.preprocess(explanations)):
            exp_parses = self.grammar.parse_input(exp)
            for j, parse in enumerate(exp_parses):
                # print(parse.semantics)
                lf = self.grammar.evaluate(parse)
                if return_parses:
                    parse.function = lf
                    parses.append(parse)
                if names and len(names) > i:
                    lf.__name__ = "{}_{}".format(names[i], j)
                else:
                    lf.__name__ = "exp%d_%d" % (self.explanation_counter, j)
                LFs.append(lf)
            self.explanation_counter += 1
        if return_parses:
            if verbose:
                print("{} parses created from {} explanations".format(len(LFs), len(explanations)))
            return parses
        else:
            if verbose:
                print("{} LFs created from {} explanations".format(len(LFs), len(explanations)))
            return LFs

    def evaluate(self, 
                examples, 
                show_everything=False,
                show_explanation=False, 
                show_candidate=False,
                show_sentence=False, 
                show_parse=False,
                show_semantics=False,
                show_correct=False,
                show_passing=False, 
                show_failing=False,
                show_redundant=False,
                show_erroring=False,
                only=[]):
        """Returns a pandas DataFrame with the explanations and various per-explanation stats"""
        if show_everything:
            show_explanation = show_candidate = show_sentence = show_parse = show_semantics = True
        if show_semantics:
            show_correct = show_passing = show_failing = show_redundant = show_erroring = True
        self.explanation_counter = 0
        examples = examples if isinstance(examples, list) else [examples]
        col_names = ['Correct', 'Passing', 'Failing', 'Redundant', 'Error', 'Unknown']
        d = {}
        example_names = []

        nCorrect = [0] * len(examples)
        nPassing = [0] * len(examples)
        nFailing = [0] * len(examples)
        nRedundant = [0] * len(examples)
        nErroring = [0] * len(examples)
        nUnknown = [0] * len(examples)

        correct_LFs = []
        passing_LFs = []
        failing_LFs = []
        redundant_LFs = []
        erroring_LFs = []
        unknown_LFs = []
        
        for i, example in enumerate(examples):
            if only and i not in only:
                continue
            if example.explanation is None:
                continue
            if show_explanation: 
                print("Example {}: {}\n".format(i, example.explanation))
            if show_candidate:
                print("CANDIDATE: {}\n".format(example.candidate))
            if show_sentence:
                print("SENTENCE: {}\n".format(example.candidate[0].get_parent()._asdict()['text']))
            semantics = set()
            parses = self.parse(
                        example.explanation, 
                        example.name,
                        verbose=False, 
                        return_parses=True)
            for parse in parses:
                if show_parse:
                    print("PARSE: {}\n".format(parse))
                # REDUNDANT
                if parse.semantics in semantics:
                    if show_redundant: print("R: {}".format(parse.semantics))
                    nRedundant[i] += 1
                    redundant_LFs += parse.function
                    continue
                semantics.add(parse.semantics)
                # ERRORING
                try:
                    denotation = parse.function(example.candidate)
                except:
                    if show_erroring: print("E: {}".format(parse.semantics))
                    print parse.semantics
                    print parse.function(example.candidate) #to display traceback
                    import pdb; pdb.set_trace()
                    nError[i] += 1 
                    erroring_LFs.append(parse.function)
                    continue
                # CORRECT             
                if example.semantics and parse.semantics==example.semantics:
                    nCorrect[i] += 1
                    correct_LFs.append(parse.function)
                    continue
                # PASSING
                if denotation==example.denotation:
                    if show_passing: print("P: {}".format(parse.semantics))
                    nPassing[i] += 1
                    passing_LFs.append(parse.function)
                    continue
                else:
                # FAILING
                    if show_failing: print("F: {}".format(parse.semantics))
                    nFailing[i] += 1
                    failing_LFs.append(parse.function)
                    continue
                # UNKNOWN
                if example.candidate is None:
                    nUnknown[i] += 1
                    unknown_LFs.append(parse.function)
                    continue
                raise Error('This should not be reached.')
                            
            if nCorrect[i] + nPassing[i] == 0:
                print("WARNING: No correct or passing parses found for the following explanation:")
                print("EXPLANATION: {}\n".format(example.explanation))

            example_names.append(example.name)

        d['Correct'] = Series(data=nCorrect, index=example_names)
        d['Passing'] = Series(data=nPassing, index=example_names)
        d['Failing'] = Series(data=nFailing, index=example_names)
        d['Redundant'] = Series(data=nRedundant, index=example_names)
        d['Error'] = Series(data=nErroring, index=example_names)
        d['Unknown'] = Series(data=nUnknown, index=example_names)
        
        self.LFs = (correct_LFs, passing_LFs, failing_LFs, redundant_LFs, erroring_LFs, unknown_LFs)
        
        return DataFrame(data=d, index=example_names)[col_names]

        # Default LF stats
        # d = {
        #     'j'         : range(self.shape[1]),
        #     'Coverage'  : Series(data=matrix_coverage(self), index=lf_names),
        #     'Overlaps'  : Series(data=matrix_overlaps(self), index=lf_names),
        #     'Conflicts' : Series(data=matrix_conflicts(self), index=lf_names)
        # }
        # if labels is not None:
        #     col_names.extend(['TP', 'FP', 'FN', 'TN', 'Empirical Acc.'])
        #     ls = np.ravel(labels.todense() if sparse.issparse(labels) else labels)
        #     tp = matrix_tp(self, ls)
        #     fp = matrix_fp(self, ls)
        #     fn = matrix_fn(self, ls)
        #     tn = matrix_tn(self, ls)
        #     ac = (tp+tn).astype(float) / (tp+tn+fp+fn)
        #     d['Empirical Acc.'] = Series(data=ac, index=lf_names)
        #     d['TP']             = Series(data=tp, index=lf_names)
        #     d['FP']             = Series(data=fp, index=lf_names)
        #     d['FN']             = Series(data=fn, index=lf_names)
        #     d['TN']             = Series(data=tn, index=lf_names)

        # if est_accs is not None:
        #     col_names.append('Learned Acc.')
        #     d['Learned Acc.'] = Series(data=est_accs, index=lf_names)
        # return DataFrame(data=d, index=example_names)[col_names]
