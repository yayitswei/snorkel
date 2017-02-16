from __future__ import print_function

from pdb import set_trace as t
from grammar import Rule

# Helpers ======================================================================
def sems0(sems):
    return sems[0]

def sems1(sems):
    return sems[1]

def sems_in_order(sems):
    return tuple(sems)

def sems_reversed(sems):
    return tuple(reversed(sems))

# Rules ======================================================================
lexical_rules = [
    # arg
    Rule('$Arg', 'arg', '.arg'),
    Rule('$Arg', 'argument', '.arg'),
    # logic
    Rule('$And', 'and', '.and'),
    Rule('$All', 'all', '.all'),
    # direction
    Rule('$LeftTokens', 'left', '.lefttokens'),
    Rule('$RightTokens', 'right', '.righttokens'),
    Rule('$BetweenTokens', 'between', '.betweentokens'),
    Rule('$SentenceTokens', 'sentence', '.sentencetokens'),
    # POS tags
    Rule('$NounPOS', 'noun', ('.string', 'NN')),
    Rule('$NumberPOS', 'number', ('.string', 'CD')),
    # other
    Rule('$In', 'in', '.in'),
    Rule('$Contains', 'contains', '.contains'),
    Rule('$StartsWith', 'starts with', '.startswith'),
    Rule('$EndsWith', 'ends with', '.endswith'),
    Rule('$Label', 'label ?it', '.label'),
]

lexical_rules.extend(
    [Rule('$True', w, ('.bool', True)) for w in ['true', 'True', 'correct']] +
    [Rule('$False', w, ('.bool', False)) for w in ['false', 'False', 'incorrect', 'wrong']] +
    [Rule('$Or', w, '.or') for w in ['or', 'nor']] +
    [Rule('$Any', w, '.any') for w in ['any', 'a']] +
    [Rule('$Not', w, '.not') for w in ['not', "n't"]] +
    [Rule('$None', w, '.none') for w in ['none', 'not any', 'neither', 'no']] +
    [Rule('$Because', w) for w in ['because', 'since', 'if']] +
    [Rule('$Upper', w, '.upper') for w in ['upper', 'uppercase', 'upper case', 'all caps', 'all capitalized']] +
    [Rule('$Lower', w, '.lower') for w in ['lower', 'lowercase', 'lower case']] +
    [Rule('$Capital', w, '.capital') for w in ['capital', 'capitals', 'capitalized']] +
    [Rule('$Equals', w, '.equals') for w in ['is', 'equal', 'equals', '=', '==', 'same ?as', 'identical']] + 
    [Rule('$LessThan', w, '.less') for w in ['less than', 'smaller than', '<']] +
    [Rule('$AtMost', w, '.atmost') for w in ['at most', 'no larger than', 'less than or equal', 'within', '<=']] +
    [Rule('$MoreThan', w, '.more') for w in ['more than', 'greater than', 'larger than', '>']] + 
    [Rule('$AtLeast', w, '.atleast') for w in ['at least', 'no less than', 'no smaller than', 'greater than or equal', '>=']] +
    # [Rule('$ListWord', w) for w in ['list', 'set', 'group']] + 
    [Rule('$Separator', w) for w in [',', ';', '/']] +
    [Rule('$Count', w, '.count') for w in ['number', 'length', 'count']] +
    [Rule('$Word', w) for w in ['word', 'words', 'term']] + 
    [Rule('$NER', w, ('.string', w.upper())) for w in ['person', 'location', 'organization']] + 
    [Rule('$Punctuation', w) for w in ['.', ',', ';', '!', '?']]
    )

unary_rules = [
    Rule('$Bool', '$BoolLit', sems0),
    Rule('$BoolLit', '$True', sems0),
    Rule('$BoolLit', '$False', sems0),
    Rule('$Conj', '$And', sems0),
    Rule('$Conj', '$Or', sems0),
    Rule('$Inequals', '$LessThan', sems0),
    Rule('$Inequals', '$AtMost', sems0),
    Rule('$Inequals', '$MoreThan', sems0),
    Rule('$Inequals', '$AtLeast', sems0),
    Rule('$Compare', '$Inequals', sems0),
    Rule('$Compare', '$Equals', sems0),
    Rule('$Direction', '$LeftTokens', sems0),
    Rule('$Direction', '$RightTokens', sems0),
    Rule('$POS', '$NounPOS', sems0),
    Rule('$POS', '$NumberPOS', sems0),
    Rule('$StringList', '$UserList', sems0),
    Rule('$UnaryStringToBool', '$Lower', sems0),
    Rule('$UnaryStringToBool', '$Upper', sems0),
    Rule('$UnaryStringToBool', '$Capital', sems0),
    Rule('$BinaryStringToBool', '$StartsWith', sems0),
    Rule('$BinaryStringToBool', '$EndsWith', sems0),
    Rule('$BinaryStringToBool', '$In', sems0),
    Rule('$BinaryStringToBool', '$Contains', sems0),
    Rule('$BinaryStringToBool', '$Equals', sems0),
    # ArgX may be treated as an object or a string (referring to its textual contents)
    Rule('$String', '$ArgX', lambda sems: ('.arg_to_string', sems[0])),
    Rule('$StringList', 'StringListOr', sems0),
    Rule('$StringList', 'StringListAnd', sems0),
    Rule('$ROOT', '$LF', lambda sems: ('.root', sems[0])),
]

compositional_rules = [
    Rule('$LF', '$Label $Bool $Because $Bool', lambda sems: (sems[0], sems[1], sems[3])),
    
    # Logicals
    Rule('$Bool', '$Bool $Conj $Bool', lambda sems: (sems[1], sems[0], sems[2])),
    Rule('$Bool', '$Not $Bool', sems_in_order),
    Rule('$Bool', '$All $BoolList', sems_in_order),
    Rule('$Bool', '$Any $BoolList', sems_in_order),
    Rule('$Bool', '$None $BoolList', sems_in_order),

    # Strings
        # building strings
    Rule('$StringStub', '$Quote $Token', lambda sems: [sems[1]]),
    Rule('$StringStub', '$StringStub $Token', lambda sems: sems[0] + [sems[1]]),
    Rule('$String', '$StringStub $Quote', lambda sems: ('.string', ' '.join(sems[0]))),
    
        # building explicit string lists
    # Rule('$StringListStub', '?$OpenParen $String', lambda sems: ('.list', sems[1])),
    # Rule('$StringListStub', '$StringListStub ?$Separator ?$And $String', lambda sems: tuple(list(sems[0]) + [sems[3]])),
    # Rule('$StringList', '$StringListStub ?$CloseParen', sems0),

        # building implicit string lists
    Rule('$StringList', '$String', lambda sems: ('.list', sems[0])),
    Rule('$StringList', '$StringList ?$Separator $String', lambda sems: tuple((list(sems[0]) + [sems[2]]))),
    Rule('$StringListOr', '$StringList ?$Separator $Or $String', lambda sems: tuple(list(sems[0]) + [sems[3]])),
    Rule('$StringListAnd', '$StringList ?$Separator $And $String', lambda sems: tuple(list(sems[0]) + [sems[3]])),

        # applying $StringToBool functions
    Rule('$Bool', '$String $StringToBool', lambda sems: ('.call', sems[1], sems[0])),
    Rule('$Bool', '$StringListOr $StringToBool', lambda sems: ('.or', ('.map', sems[1], sems[0]))),
    Rule('$Bool', '$StringListAnd $StringToBool', lambda sems: ('.and', ('.map', sems[1], sems[0]))),
    Rule('$BoolList', '$StringList $StringToBool', lambda sems: ('.map', sems[1], sems[0])),

        # defining #StringToBool functions
    Rule('$StringToBool', '$UnaryStringToBool', lambda sems: (sems[0],)),
    Rule('$StringToBool', '$BinaryStringToBool $String', lambda sems: (sems[0], sems[1])),
    # Rule('$StringToBool', '$BinaryStringToBool $StringListAnd', lambda sems: ('.composite_and', (sems[0], sems[1]))),
    Rule('$StringToBool', '$BinaryStringToBool $StringListOr', lambda sems: ('.composite_or', (sems[0],), sems[1])),
    
    Rule('$StringToBool', '$In $StringList', sems_in_order), # TODO: unify me with the rest of the stringlisting going on
    
    # Integers
        # applying $IntoToBool functions
    Rule('$Bool', '$Int $IntToBool', lambda sems: ('.call', sems[1], sems[0])),
    Rule('$BoolList', '$IntList $IntToBool', lambda sems: ('.map', sems[1], sems[0])),
    
    # e.g., more than five of X words are upper
    Rule('$Bool', '$Compare $Int $BoolList', lambda sems: ('.call', (sems[0], sems[1]), ('.sum', sems[2]))),

    Rule('$IntToBool', '$In $IntList', sems_in_order),
    Rule('$IntToBool', '$Contains $Int', sems_in_order),
    Rule('$IntToBool', '$Compare $Int', sems_in_order),

    # Rule('$Int', '$Count ?$In $List', lambda sems: (sems[0], sems[2])),
    
    # Slices
    #TODO: Test these more thoroughly
    # Rule('$String', '$Int $StringList', lambda sems: ('.index', sems[1], sems[0])),
    # Rule('$StringList', '$LessThan $Int $StringList', lambda sems: ('.slice', sems[2], ('.int', 0), sems[1])),
    # Rule('$StringList', '$AtMost $Int $StringList', lambda sems: ('.slice', sems[2], ('.int', 0), ('.int', sems[1][1] + 1))),
    # Rule('$StringList', '$AtLeast $Int $StringList', lambda sems: ('.slice', sems[2], sems[1], 100)),
    # Rule('$StringList', '$MoreThan $Int $StringList', lambda sems: ('.slice', sems[2], ('.int', sems[1][1] + 1), 100)),
    # Rule('$Int', '$Int $IntList', lambda sems: ('.index', sems[1], sems[0])),

    # Context
    # Note: Normal 'X in Y' does not work because we need to know what they are looking for (e.g., words, pos, ner)
    # Rule('$StringList', '$Direction $ArgX', lambda sems: (sems[0], sems[1], ('.string', 'words'))),
    # Rule('$StringList', '$Direction $ArgX $Or $ArgX', lambda sems: ('.merge', (sems[0], sems[1], ('.string', 'words')), (sems[0], sems[3], ('.string', 'words')))),
    # Rule('$StringToBool', '$Direction $ArgX', lambda sems: ('.in', (sems[0], sems[1], ('.string', 'words')))),
    
    # Rule('$Bool', '$POS ?$In $Direction $ArgX', lambda sems: ('.in', (sems[2], sems[3], ('.string', 'pos_tags')), sems[0])),
    # Rule('$Bool', '$NER ?$In $Direction $ArgX', lambda sems: ('.in', (sems[2], sems[3], ('.string', 'ner_tags')), sems[0])),
    
    # Rule('$StringList', '$BetweenTokens $ArgX $And $ArgX', lambda sems: (sems[0], sems[1], sems[3], ('.string', 'words'))),
    # Rule('$StringToBool', '$BetweenTokens $ArgX $And $ArgX', lambda sems: ('.in', (sems[0], sems[1], sems[3], ('.string', 'words')))),
    
    # Rule('$Bool', '$POS ?$In $BetweenTokens $ArgX $And $ArgX', lambda sems: ('.in', (sems[2], sems[3], sems[5], ('.string', 'pos_tags')), sems[0])),
    # Rule('$Bool', '$NER ?$In $BetweenTokens $ArgX $And $ArgX', lambda sems: ('.in', (sems[2], sems[3], sems[5], ('.string', 'ner_tags')), sems[0])),
    
    # Rule('$StringList', '$SentenceTokens ?$ArgX ?$And ?$ArgX', lambda sems: (sems[0], ('.string', 'words'))),
    
    # Rule('$Bool', '$POS ?$In $SentenceTokens ?$ArgX ?$And ?$ArgX', lambda sems: ('.in', (sems[2], ('.string', 'pos_tags')), sems[0])),
    # Rule('$Bool', '$NER ?$In $SentenceTokens ?$ArgX ?$And ?$ArgX', lambda sems: ('.in', (sems[2], ('.string', 'ner_tags')), sems[0])),
    
    Rule('$ArgX', '$Arg $Int', sems_in_order),
    # Rule('$TokenList', '$ArgXToTokenList $ArgX', lambda sems: ('.call', )),
    
    # Rule('$ArgXToTokenList', '$Direction')
    # Rule('$StringList', '$TokenList', TBD),
    # Rule('$POSList', '$TokenList', TBD),
    # Rule('$NERList', '$TokenList', TBD),
]

snorkel_rules = lexical_rules + unary_rules + compositional_rules

snorkel_ops = {
    # root
    '.root': lambda x: lambda c: x(c),
    '.label': lambda x, y: lambda c: (-1 if not x(c) else 1) if y(c)==True else 0,
    # primitives
    '.bool': lambda x: lambda c: x,
    '.string': lambda x: lambda c: x,
    '.int': lambda x: lambda c: x,
    '.list': lambda *x: lambda c: [z(c) for z in x],
    '.user_list': lambda x: lambda c: c['user_lists'][x(c)],
    '.call': lambda *x: lambda c: x[0](c) if len(x)==1 else x[0](c)(x[1](c)), #TODO: extend to more than one argument?
    '.map': lambda x, y: lambda c: [x(c)(yi) for yi in y(c)],
    # '.composite_and': lambda x, y: lambda c: lambda z: all([x(yi)(z) for yi in y(c)]),
    '.composite_or': lambda x, y: lambda c: lambda z: any([x(yi)(c)(z) for yi in y]),
    # logic
    '.and': lambda *x: lambda c: all(xi(c) for xi in x),
    '.or': lambda *x: lambda c: any(xi(c) for xi in x),
    '.not': lambda x: lambda c: not x(c),
    '.all': lambda x: lambda c: all(x(c)),
    '.any': lambda x: lambda c: any(x(c)),
    '.none': lambda x: lambda c: not any(x(c)),
    # comparisons
    '.equals': lambda x: lambda c: lambda y: y == x(c),
    '.less': lambda x: lambda c: lambda y: y < x(c),
    '.atmost': lambda x: lambda c: lambda y: y <= x(c),
    '.more': lambda x: lambda c: lambda y: y > x(c),
    '.atleast': lambda x: lambda c: lambda y: y >= x(c),
    # string functions
    '.upper': lambda c: lambda x: x.isupper(),
    '.lower': lambda c: lambda x: x.islower(),
    '.capital': lambda c: lambda x: x[0].isupper(),
    '.startswith': lambda x: lambda c: lambda y: y.startswith(x(c)),
    '.endswith': lambda x: lambda c: lambda y: y.endswith(x(c)),
    # lists
    '.in': lambda x: lambda c: lambda y: y in x(c),
    '.contains': lambda x: lambda c: lambda y: x(c) in y,
    '.index': lambda x, y: lambda c: x(c)[max(0, y(c) - 1)], # account for 0-indexing 
    '.slice': lambda x, y, z: lambda c: x(c)[y(c):z(c)], 
    '.count': lambda x: lambda c: len(x(c)),
    '.sum': lambda x: lambda c: sum(x(c)),
    '.merge': lambda x, y: lambda c: x(c) + y(c),
    # context
    '.lefttokens': lambda x, y: lambda c: c['lf_helpers']['get_left_tokens'](x(c), y(c)),
    '.righttokens': lambda x, y: lambda c: c['lf_helpers']['get_right_tokens'](x(c), y(c)),
    '.betweentokens': lambda x, y, z: lambda c: c['lf_helpers']['get_between_tokens'](x(c), y(c), z(c)),
    '.sentencetokens': lambda x: lambda c: c['lf_helpers']['get_sentence_tokens'](c['candidate'][0], x(c)),
    '.arg': lambda x: lambda c: c['candidate'][x(c) - 1],
        # FIXME: For ease of testing, temporarily allow tuples of strings in place of legitimate candidates
    '.arg_to_string': lambda x: lambda c: x(c) if isinstance(x(c), basestring) else x(c).get_span(),
    }