from grammar import Rule

import re

class Annotator:
    """A base class for annotators."""
    def __init__(self):
        self.rules = self.make_rules()

    def annotate(self, tokens):
        """Returns a list of pairs, each a category and a semantic representation."""
        return []
    
    def make_rules(self):
        """Returns a list of lexical rules"""
        rules = []
        for lhs in self.categories:
            rules.append(Rule(lhs, (lhs, '$Token'), lambda sems: sems[0]))
        return rules

class TokenAnnotator(Annotator):
    def __init__(self):
        self.categories = []
        Annotator.__init__(self)
    
    def annotate(self, tokens):
        if len(tokens) == 1:
            return [('$Token', tokens[0]['word'])]
        else:
            return []

class PunctuationAnnotator(Annotator):
    def __init__(self):
        self.categories = ['$OpenQuote', '$CloseQuote', '$OpenParen', '$CloseParen']
        Annotator.__init__(self)
    
    def annotate(self, tokens):
        if len(tokens) == 1:
            if tokens[0]['pos'] == "``":
                return [('$OpenQuote', tokens[0]['word'])]
            elif tokens[0]['pos'] == "\'\'":
                return [('$CloseQuote', tokens[0]['word'])]
            elif tokens[0]['pos'] == "-LRB-":
                return [('$OpenParen', tokens[0]['word'])]
            elif tokens[0]['pos'] == "-RRB-":
                return [('$CloseParen', tokens[0]['word'])]
        return []

class IntegerAnnotator(Annotator):
    def __init__(self):
        self.categories = ['$Int']
        Annotator.__init__(self)

    def annotate(self, tokens):
        if len(tokens) == 1:
            if all(token['ner'] in ['NUMBER','ORDINAL'] for token in tokens):
                ner_number = tokens[0]['normalizedNER']
                number = re.sub('[^\d\.]','', ner_number)
                value = int(float(number))
                return [('$Int', ('.int', value))]
        return []