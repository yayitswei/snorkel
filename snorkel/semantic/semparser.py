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

    def preprocess(self, explanations):
        stopwords = (['is', 'are', 'be',
                      'a', 'the', 
                      'to', 'of', 'from'])
        for explanation in explanations:
            explanation = explanation.replace("'", '"')
            words = explanation.split()
            yield ' '.join([w for w in words if w not in stopwords])

    def parse(self, explanations, candidates=None, verbose=False, return_parses=False):
        """
        Accepts natural language explanations and returns parses
        """
        LFs = []
        parses = []
        explanations = explanations if isinstance(explanations, list) else [explanations]
        for i, exp in enumerate(self.preprocess(explanations)):
            exp_parses = self.grammar.parse_input(exp)
            for j, parse in enumerate(exp_parses):
                # print(parse.semantics)
                lf = self.grammar.evaluate(parse)
                if return_parses:
                    parse.function = lf
                    parses.append(parse)
                lf.__name__ = "exp%d_parse%d" % (i, j)
                LFs.append(lf)
        if return_parses:
            if verbose:
                print("{} parses created from {} explanations".format(len(LFs), len(explanations)))
            return parses
        else:
            if verbose:
                print("{} LFs created from {} explanations".format(len(LFs), len(explanations)))
            return LFs

    def evaluate(self, examples, 
                show_explanation=False, 
                show_correct=False, 
                show_incorrect=False,
                show_redundant=False,
                show_failed=False,
                show_all=False,
                only=[]):
        """Returns a pandas DataFrame with the explanations and various per-explanation stats"""
        if show_all:
            show_correct = show_incorrect = show_redundant = show_failed = True
        examples = examples if isinstance(examples, list) else [examples]
        col_names = ['Correct', 'Incorrect', 'Redundant', 'Failed', 'Unknown']
        d = {}
        example_names = []
        
        correct = []
        incorrect = []
        redundant = []
        failed = []
        unknown = []
        
        for i, example in enumerate(examples):
            if only and i not in only:
                continue
            if show_explanation: print("Example {}: {}".format(i, example.explanation))
            nCorrect = nIncorrect = nRedundant = nFailed = nUnknown = 0
            semantics = set()
            parses = self.parse(
                        example.explanation, 
                        example.candidate, 
                        verbose=False, 
                        return_parses=True)
            for parse in parses:
                try:
                    if parse.semantics in semantics:
                        if show_redundant: print("R: {}".format(parse.semantics))
                        nRedundant += 1
                    else:
                        semantics.add(parse.semantics)
                        if example.candidate is None:
                            nUnknown += 1
                        else:
                            if parse.function(example.candidate)==example.denotation:
                                if show_correct: print("C: {}".format(parse.semantics))
                                nCorrect += 1
                            else:
                                if show_incorrect: print("I: {}".format(parse.semantics))
                                nIncorrect += 1
                except:
                    if show_failed: print("F: {}".format(parse.semantics))
                    print parse.semantics
                    print parse.function(example.candidate) #to display traceback
                    import pdb; pdb.set_trace()
                    nFailed += 1
            if nCorrect == 0:
                print("WARNING: No correct parses found for the following explanation:")
                print(example.explanation)

            example_names.append('Example{}'.format(i))
            correct.append(nCorrect)
            incorrect.append(nIncorrect)
            redundant.append(nRedundant)
            failed.append(nFailed)
            unknown.append(nUnknown)

        d['Correct'] = Series(data=correct, index=example_names)
        d['Incorrect'] = Series(data=incorrect, index=example_names)
        d['Redundant'] = Series(data=redundant, index=example_names)
        d['Failed'] = Series(data=failed, index=example_names)
        d['Unknown'] = Series(data=unknown, index=example_names)
        
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
