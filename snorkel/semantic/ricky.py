from grammar import Rule
from helpers import lf_helpers

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
    Rule('$Any', 'any', '.any'),
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
    Rule('$Contains', 'contains', '.in'),
    Rule('$StartsWith', 'starts with', '.startswith'),
    Rule('$EndsWith', 'ends with', '.endswith'),
    Rule('$Label', 'label ?it', '.label'),
]

lexical_rules.extend(
    [Rule('$True', w, ('.bool', True)) for w in ['true', 'True', 'correct']] +
    [Rule('$False', w, ('.bool', False)) for w in ['false', 'False', 'incorrect', 'wrong']] +
    [Rule('$Or', w, '.or') for w in ['or', 'nor']] +
    [Rule('$Not', w, '.not') for w in ['not', "n't"]] +
    [Rule('$None', w, '.none') for w in ['none', 'not any', 'neither', 'no']] +
    [Rule('$Because', w) for w in ['because', 'since', 'if']] +
    [Rule('$Upper', w, '.upper') for w in ['upper', 'uppercase', 'upper case', 'all caps', 'all capitalized']] +
    [Rule('$Lower', w, '.lower') for w in ['lower', 'lowercase', 'lower case']] +
    [Rule('$Capital', w, '.capital') for w in ['capital', 'capitals', 'capitalized']] +
    [Rule('$Equals', w, '.equals') for w in ['equal', 'equals', '=', '==', 'same ?as', 'identical']] + 
    [Rule('$LessThan', w, '.less') for w in ['less than', 'smaller than', '<']] +
    [Rule('$AtMost', w, '.atmost') for w in ['at most', 'no larger than', 'less than or equal', 'within', '<=']] +
    [Rule('$MoreThan', w, '.more') for w in ['more than', 'greater than', 'larger than', '>']] + 
    [Rule('$AtLeast', w, '.atleast') for w in ['at least', 'no less than', 'no smaller than', 'greater than or equal', '>=']] +
    [Rule('$ListWord', w) for w in ['list', 'set', 'group']] + 
    [Rule('$Separator', w) for w in [',', ';', '/']] +
    [Rule('$Count', w, '.count') for w in ['number', 'length', 'count']] +
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
    Rule('$List', '$StringList', sems0),
    Rule('$List', '$IntList', sems0),
    # ArgX may be treated as an object or a string (referring to its textual contents)
    Rule('$String', '$ArgX', lambda sems: ('.arg_to_string', sems[0])),
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
    Rule('$String', '$OpenQuote $Token $CloseQuote', lambda sems: ('.string', sems[1])),
    
    Rule('$Bool', '$String $StringToBool', lambda sems: tuple(list(sems[1]) + [sems[0]])),
    Rule('$BoolList', '$StringList $StringToBool', lambda sems: tuple(['.list'] + [tuple(list(sems[1]) + [x]) for x in sems[0][1:]])),
    
    Rule('$StringToBool', '$Lower', lambda sems: (sems[0],)),
    Rule('$StringToBool', '$Upper', lambda sems: (sems[0],)),
    Rule('$StringToBool', '$Capital', lambda sems: (sems[0],)),
    Rule('$StringToBool', '$StartsWith $String', sems_in_order),
    Rule('$StringToBool', '$EndsWith $String', sems_in_order),
    Rule('$StringToBool', '?$In $String', lambda sems: ('.in', sems[1])),
    Rule('$StringToBool', '?$In $StringList', lambda sems: ('.in', sems[1])),
    Rule('$StringToBool', '$Contains $String', lambda sems: ('.contains', sems[1])),
    Rule('$StringToBool', '$Equals $String', sems_in_order),
    
    Rule('$StringListStart', '?$ListWord $OpenParen $String', lambda sems: ('.list', sems[2])),
    Rule('$StringListStart', '$StringListStart ?$Separator ?$And $String', lambda sems: tuple(list(sems[0]) + [sems[3]])),
    Rule('$StringList', '$StringListStart $CloseParen', sems0),
    
    # Integers
    Rule('$BoolList', '$IntList $IntToBool', lambda sems: tuple(['.list'] + [tuple(list(sems[1]) + [x]) for x in sems[0][1:]])),
    Rule('$Bool', '$Int $IntToBool', lambda sems: tuple(list(sems[1]) + [sems[0]])),
    Rule('$Bool', '$Compare $Int $BoolList', lambda sems: (sems[0], sems[1], ('.sum', sems[2]))), # e.g., more than five of X words are upper

    Rule('$IntToBool', '$In $IntList', sems_in_order),
    Rule('$IntToBool', '$Contains $Int', lambda sems: ('.contains', sems[1])),
    Rule('$IntToBool', '$Compare $Int', sems_in_order),

    Rule('$Int', '$Count ?$In $List', lambda sems: (sems[0], sems[2])),
    
    # Slices
    #TODO: Test these more thoroughly
    Rule('$String', '$Int $StringList', lambda sems: ('.index', sems[1], sems[0])),
    Rule('$StringList', '$LessThan $Int $StringList', lambda sems: ('.slice', sems[2], ('.int', 0), sems[1])),
    Rule('$StringList', '$AtMost $Int $StringList', lambda sems: ('.slice', sems[2], ('.int', 0), ('.int', sems[1][1] + 1))),
    Rule('$StringList', '$AtLeast $Int $StringList', lambda sems: ('.slice', sems[2], sems[1], 100)),
    Rule('$StringList', '$MoreThan $Int $StringList', lambda sems: ('.slice', sems[2], ('.int', sems[1][1] + 1), 100)),
    Rule('$Int', '$Int $IntList', lambda sems: ('.index', sems[1], sems[0])),

    # Context
    # Note: Normal 'X in Y' does not work because we need to know what they are looking for (e.g., words, pos, ner)
    Rule('$StringList', '$Direction $ArgX', lambda sems: (sems[0], sems[1], ('.string', 'words'))),
    Rule('$StringList', '$Direction $ArgX $Or $ArgX', lambda sems: ('.merge', (sems[0], sems[1], ('.string', 'words')), (sems[0], sems[3], ('.string', 'words')))),
    Rule('$Bool', '$POS ?$In $Direction $ArgX', lambda sems: ('.in', (sems[2], sems[3], ('.string', 'pos_tags')), sems[0])),
    Rule('$Bool', '$NER ?$In $Direction $ArgX', lambda sems: ('.in', (sems[2], sems[3], ('.string', 'ner_tags')), sems[0])),
    
    Rule('$StringList', '$BetweenTokens $ArgX $And $ArgX', lambda sems: (sems[0], sems[1], sems[3], ('.string', 'words'))),
    Rule('$StringToBool', '$BetweenTokens $ArgX $And $ArgX', lambda sems: ('.in', (sems[0], sems[1], sems[3], ('.string', 'words')))),
    Rule('$Bool', '$POS ?$In $BetweenTokens $ArgX $And $ArgX', lambda sems: ('.in', (sems[2], sems[3], sems[5], ('.string', 'pos_tags')), sems[0])),
    Rule('$Bool', '$NER ?$In $BetweenTokens $ArgX $And $ArgX', lambda sems: ('.in', (sems[2], sems[3], sems[5], ('.string', 'ner_tags')), sems[0])),
    
    Rule('$StringList', '$SentenceTokens ?$ArgX ?$And ?$ArgX', lambda sems: (sems[0], ('.string', 'words'))),
    Rule('$Bool', '$POS ?$In $SentenceTokens ?$ArgX ?$And ?$ArgX', lambda sems: ('.in', (sems[2], ('.string', 'pos_tags')), sems[0])),
    Rule('$Bool', '$NER ?$In $SentenceTokens ?$ArgX ?$And ?$ArgX', lambda sems: ('.in', (sems[2], ('.string', 'ner_tags')), sems[0])),
    
    Rule('$ArgX', '$Arg $Int', sems_in_order),
]

snorkel_rules = lexical_rules + unary_rules + compositional_rules

snorkel_ops = {
    # root
    '.root': lambda x: lambda c: x({'lf_helpers': lf_helpers(), 'candidate': c}),
    '.label': lambda x, y: lambda c: (-1 if not x(c) else 1) if y(c) else 0,
    # primitives
    '.bool': lambda x: lambda c: x,
    '.string': lambda x: lambda c: x,
    '.int': lambda x: lambda c: x,
    '.list': lambda *x: lambda c: [z(c) for z in x],
    # logic
    '.and': lambda x, y: lambda c: x(c) and y(c),
    '.or': lambda x, y: lambda c: x(c) or y(c),
    '.not': lambda x: lambda c: not x(c),
    '.all': lambda x: lambda c: all(x(c)),
    '.any': lambda x: lambda c: any(x(c)),
    '.none': lambda x: lambda c: not any(x(c)),
    # comparisons
    '.equals': lambda x, y: lambda c: y(c) == x(c),
    '.less': lambda x, y: lambda c: y(c) < x(c),
    '.atmost': lambda x, y: lambda c: y(c) <= x(c),
    '.more': lambda x, y: lambda c: y(c) > x(c),
    '.atleast': lambda x, y: lambda c: y(c) >= x(c),
    # string functions
    '.upper': lambda x: lambda c: x(c).isupper(),
    '.lower': lambda x: lambda c: x(c).islower(),
    '.capital': lambda x: lambda c: x(c)[0].isupper(),
    '.startswith': lambda x, y: lambda c: y(c).startswith(x(c)),
    '.endswith': lambda x, y: lambda c: y(c).endswith(x(c)),
    # lists
    '.index': lambda x, y: lambda c: x(c)[max(0, y(c) - 1)], # account for 0-indexing 
    '.slice': lambda x, y, z: lambda c: x(c)[y(c):z(c)], 
    '.in': lambda x, y: lambda c: y(c) in x(c),
    '.contains': lambda x, y: lambda c: x(c) in y(c),
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