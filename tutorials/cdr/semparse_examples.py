
class Example(object):
    def __init__(self, name=None, explanation=None, paraphrase=None,
                 candidate=None, denotation=None, semantics=None):
        self.name = name
        self.explanation = explanation
        self.paraphrase = paraphrase
        self.candidate = candidate
        self.denotation = denotation # True label on this candidate
        self.semantics = semantics

    def __str__(self):
        return 'Example("%s")' % (self.explanation)
    
    def display(self):
        print 'Example'
        print('%-12s %s' % ('name', self.name))
        print('%-12s %s' % ('explanation', self.explanation))
        print('%-12s %s' % ('candidate', self.candidate))
        print('%-12s %d' % ('denotation', self.denotation))
        print('%-12s %s' % ('semantics', self.semantics))



# -7563346943193853808 =>
# "\n \nIt has been almost two years since Klaus Andres, 71, was handed a life 
# sentence for the 2011 killing of wife Li Ping Cao."

# -3658950303959694808 =>
# "David Beckham already had four other perfumes, two of which also had a women's 
# version fronted by his lovely wife Victoria Beckham."
# arg1 = Victoria Beckham
# arg2 = David Beckham

# -5889490471583847150 =>
# "Clinical and experimental data published to date suggest several possible 
# mechanisms by which cocaine may result in acute myocardial infarction."

test_examples = [
    # Base
    Example(
        explanation="label True because True",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # And
    Example(
        explanation="label True because True and True",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Or
    Example(
        explanation="label True because False or True",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Not
    Example(
        explanation="label True because not False",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Parentheses
    Example(
        explanation="label True because True or (True and False)",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Equals (String)
    Example(
        explanation="label True because 'yes' equals 'yes'",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Equals (Int)
    Example(
        explanation="label True because 1 is equal to 1",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Integers (digit or text)
    Example(
        explanation="label True because 1 is equal to one",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Less than
    Example(
        explanation="label True because 1 is less than 2",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # At most
    Example(
        explanation="label True because 2 is less than or equal to 2",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Greater than
    Example(
        explanation="label True because 2 > 1",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # At least
    Example(
        explanation="label True because 2 is at least 2",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Lowercase
    Example(
        explanation="label True because arg 1 is lowercase",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Uppercase
    Example(
        explanation="label True because arg 1 is upper case",
        candidate=('FOO', 'bar'),
        denotation=1,
        semantics=None),
    # Capitalized
    Example(
        explanation="label True because arg 1 is capitalized",
        candidate=('Foo', 'bar'),
        denotation=1,
        semantics=None),
    # Starts with
    Example(
        explanation="label True because the word 'blueberry' starts with 'blue'",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Ends with
    Example(
        explanation="label True because the word 'blueberry' ends with 'berry'",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Candidate as string
    Example(
        explanation="label True because argument 1 equals 'foo'",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # In
    Example(
        explanation="label True because 'bar' is in 'foobarbaz'",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Not Inversion
    Example(
        explanation="label True because 'rab' is not in 'foobarbaz'",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Contains
    Example(
        explanation="label True because the word 'foobarbaz' contains 'oobarba'",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # List
    Example(
        explanation="label True because arg 2 equals 'foo', 'bar', or 'baz'",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # UserList
    Example(
        explanation="label True because 'blue' in colors",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
   # OrList left
    Example(
        explanation="label True because 'blue' or 'shmoo' is in colors",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
   # OrList right
    Example(
        explanation="label True because 'blue' ends with 'moe' or 'lue'",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # AndList left
    Example(
        explanation="label True because 'blue' and 'red' are in colors",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # AndList right
    Example(
        explanation="label True because 'blue' contains 'l' and 'u'",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Left words (list)
    Example(
        explanation="label True because 'wife' is in the words left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None), 
    # Right words (list)
    Example(
        explanation="label True because 'wife' is in the words to the right of arg 2",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None), 
    # Between words (list)
    Example(
        explanation="label True because 'wife' is in the words between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None), 
    # Sentence (list)
    Example(
        explanation='label True because "wife" is in the sentence',
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Index left
    Example(
        explanation="label True because arg 2 is left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Index right
    Example(
        explanation="label True because arg 1 is right of arg 2",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Index left equality
    Example(
        explanation="label True because 'wife' is one word to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Index left inequality 0
    Example(
        explanation="label True because arg 2 is more than three words to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Index left inequality 1
    Example(
        explanation="label True because not arg 2 is more than fifty words to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Index within (<=)
    Example(
        explanation="label True because 'wife' is within three words to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Index OrList left
    Example(
        explanation="label True because 'husband' or 'wife' is within three words to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Index AndList left
    Example(
        explanation="label True because not 'husband' and 'wife' are within three words to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # # Index OrList right
    # Example(
    #     explanation="label True because 'wife' is less than three words to the left of arg 1 or arg2",
    #     candidate=-3658950303959694808,
    #     denotation=1,
    # semantics=None),
    # # Index within
    # Example(
    #     explanation="label True because 'wife' is within three words of arg 1",
    #     candidate=-3658950303959694808,
    #     denotation=1,
    # semantics=None),
    # # Index without
    # Example(
    #     explanation="label True because arg 1 is not within 5 words of arg 2",
    #     candidate=-3658950303959694808,
    #     denotation=1,
    # semantics=None),
    # Between
    Example(
        explanation="label True because 'wife' is between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Characters0
    Example(
        explanation="label True because 'wife' is less than 10 characters to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Characters1
    Example(
        explanation="label True because 'wife' is more than 20 characters to the right of arg 2",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Paraphrase0
    Example(
        explanation="label True because 'wife' is immediately to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Tokens
    Example(
        explanation="label True because at least one word to the left of arg 1 is lower case",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None), 
    # POS
    Example(
        explanation="label True because at least one noun exists between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # NER
    Example(
        explanation="label True because there are no people between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Count0
    Example(
        explanation="label True because there are not three people in the sentence",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Count1
    Example(
        explanation="label True because the number of words between arg 1 and arg 2 is less than 25",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Count2
    Example(
        explanation="label True because there are more than 3 words between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Count3
    Example(
        explanation="label True because at least one word exists between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Count4
    Example(
        explanation="label True because there are two nouns to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Count5
    Example(
        explanation="label True because there are less than three nouns to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Count6
    Example(
        explanation="label True because there are not more than two nouns to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Count7
    Example(
        explanation="label True because at least one word to the left of arg 1 starts with a spouse word",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # # Intersection0
    # Example(
    #     explanation="label True because there is at least one word from colors in the bluebird words",
    #     candidate=('foo', 'bar'),
    #     denotation=1,
    # semantics=None),
    # # Intersection1
    # Example(
    #     explanation="label True because less than two colors words are in bluebird",
    #     candidate=('foo', 'bar'),
    #     denotation=1,
    # semantics=None),
    # # Disjoint
    # Example(
    #     explanation="label True because there are no colors words in the greek words",
    #     candidate=('foo', 'bar'),
    #     denotation=1,
    # semantics=None),
    # All
    Example(
        explanation='label True because all of the colors are lowercase',
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Any
    Example(
        explanation='label True because any of the letters are lowercase',
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # None
    Example(
        explanation='label True because none of the smalls are capitalized',
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
#     # Composition0
#     Example(
#         explanation="label True because 'wife' is between arg 1 and arg 2 and 'years' is to the left of arg 1",
#         candidate=-3658950303959694808,
#         denotation=1,
# semantics=None),
#     # Composition1
#     Example(
#         explanation="label True because arg 1 is identical to arg 2",
#         candidate=('foo', 'foo'),
#         denotation=1,
# semantics=None),
#     # Composition2
#     Example(
#         explanation="label True because there is at least one spouse word between arg 1 and arg 2",
#         candidate=-3658950303959694808,
#         denotation=1,
# semantics=None),
#     # Composition3
#     Example(
#         explanation="label True because there is at least one spouse word within two words to the left of arg 1 or arg 2",
#         candidate=-3658950303959694808,
#         denotation=1,
# semantics=None),
    # Partially unparseable
    Example(
        explanation="label True because 1 is less than 2 and the moon is full",
        candidate=('foo', 'bar'),
        denotation=1,
        semantics=None),
    # Right before
    Example(
        explanation="label True because 'wife' is right before arg 1",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Them
    Example(
        explanation="label True because 'wife' is between arg 1 and arg 2 and 'divorced' is not between them",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
    # Inverted sentence
    Example(
        explanation="label True because to the left of arg 1 is a spouse word",
        candidate=-3658950303959694808,
        denotation=1,
        semantics=None),
]


spouse_examples = [
#     explanations = [
#     "Label false because the number of words between arg 1 and arg 2 is larger than 10",
#     "Label false because there is a person between arg 1 and arg 2",
#     "Label true because there is at least one spouse word in the words between arg 1 and arg 2",
#     "Label true because there is at least one spouse word within two words to the left of arg 1 or arg 2",
#     "Label false because there are no spouse words in the sentence",
#     "Label true because the word 'and' is between arg 1 and arg 2 and 'married' is to the right of arg 2",
#     "Label false because there is at least one family word between arg 1 and arg 2",
#     "Label false because there is at least one family word within two words to the left of arg 1 or arg 2",
#     "Label false because there is at least one coworker word between arg 1 and arg 2",
#     "Label false because arg 1 is identical to arg 2",
#     ]
    Example(
        explanation="Label false because the number of words between arg 1 and arg 2 is larger than 10",
        candidate=-5729816328165410632,
        denotation=-1,
        semantics=None),
    Example(
        explanation="Label false because there is a person between arg 1 and arg 2",
        candidate=-8692729291220282012,
        denotation=-1,
        semantics=None),
    Example(
        explanation="Label true because there is at least one spouse word in the words between arg 1 and arg 2",
        candidate=-3135315734051751361,
        denotation=1,
        semantics=None),
    Example(
        explanation="Label true because there is at least one spouse word within two words to the left of arg 1 or arg 2",
        candidate=-7563346943193853808,
        denotation=1,
        semantics=None),
    Example(
        explanation="Label false because there are no spouse words in the sentence",
        candidate=-8021416815354059709,
        denotation=-1,
        semantics=None),
    Example(
        explanation="Label true because the word 'and' is between arg 1 and arg 2 and 'married' is to the right of arg 2",
        candidate=None,
        denotation=1,
        semantics=None),
    Example(
        explanation="Label false because there are no spouse words in the sentence",
        candidate=-8021416815354059709,
        denotation=-1,
        semantics=None),
    Example(
        explanation="Label false because there is at least one family word between arg 1 and arg 2",
        candidate=-8692729291220282012,
        denotation=-1,
        semantics=None),
    Example(
        explanation="Label false because arg 1 is identical to arg 2",
        candidate=660552142898381681,
        denotation=-1,
        semantics=None),
]


cdr_examples = [
    ### TESTING ###
    # Example(
    #     explanation="Label True because the chemical is to the left of the disease",
    #     candidate=-5889490471583847150,
    #     denotation,
    # semantics=None=1
    # ),    
    ### TESTING ###
    # LF_c_cause_d
    Example(
        name='LF_c_cause_d',
        explanation="""Label true because any causal phrase is between the 
            chemical and the disease and the word 'not' is not between the 
            chemical and the disease""",
        paraphrase="""Label true because between the chemical and the disease, 
            there is a causal word and the word 'not' is not between them.""",
        candidate=6606713828167518488,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.any', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.user_list', ('.string', u'causal')))), ('.not', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'not'))))))),
    # LF_c_d
    Example(
        name='LF_c_d',
        explanation="Label true because the disease is immediately after the chemical",
        paraphrase="""Label true because the disease is immediately preceded by the chemical.""",
        candidate=4911918761913559389,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.arg_to_string', ('.arg', ('.int', 2))))))),
    # LF_c_induced_d
    Example(
        name='LF_c_induced_d',
        explanation="""Label true because the disease is immediately after the 
            chemical and 'induc' or 'assoc' is in the chemical""",
        paraphrase="""Label true because the disease is immediately preceded by the chemical, 
            and the chemical name contains an "induc" or "assoc" root.""",
        candidate=6618773943628884463,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.arg_to_string', ('.arg', ('.int', 2)))), ('.any', ('.map', ('.in', ('.arg_to_string', ('.arg', ('.int', 1)))), ('.list', ('.string', u'induc'), ('.string', u'assoc')))))))),
    # LF_c_treat_d
    Example(
        name='LF_c_treat_d',
        explanation="""Label false because any word between the chemical and 
            the disease contains a treat word and the chemical is within 100 
            characters to the left of the disease""",
        paraphrase="""Label false because the chemical precedes the disease by no more than 100 characters, 
            and a word between the disease and the chemical contains a root in the treat dictionary.""",
        candidate=5000202430163451980,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.any', ('.map', ('.composite_or', ('.contains',), ('.user_list', ('.string', u'treat'))), ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 100), ('.string', 'chars')))), ('.arg_to_string', ('.arg', ('.int', 1)))))))),
    # LF_c_treat_d_wide
    Example(
        name='LF_c_treat_d_wide',
        explanation="""Label false because any word between the chemical and 
            the disease contains a treat word and the chemical is left of the 
            disease""",
        paraphrase="""Label false because the chemical comes before the disease, 
            and a word between them contains a treat root.""",
        candidate=-5412508044020208858,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.any', ('.map', ('.composite_or', ('.contains',), ('.user_list', ('.string', u'treat'))), ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.arg_to_string', ('.arg', ('.int', 1)))))))),
    # # LF_closer_chem
    # Example(
    #     name='LF_closer_chem',
    #     explanation=None,
    #     paraphrase="""""",
    #     candidate=-1954799400282697253,
    #     denotation=-1,
    #     semantics=None),
    # # LF_closer_dis
    # Example(
    #     name='LF_closer_dis',
    #     explanation=None,
    #     paraphrase="""""",
    #     candidate=-130640710948826159,
    #     denotation=-1,
    #     semantics=None),
    # LF_ctd_marker_c_d
    Example(
        name='LF_ctd_marker_c_d',
        explanation="""Label true because the disease is immediately after the 
            chemical and the pair of canonical ids of the chemical and disease 
            is in ctd_marker""",
        paraphrase="""Label true because the disease is immediately preceded by the chemical, 
            and the pair of the chemical and the disease canonical IDs appears in the ctd_marker dictionary.""",
        candidate=3829603392041554457,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.arg_to_string', ('.arg', ('.int', 2)))), ('.call', ('.in', ('.user_list', ('.string', u'ctd_marker'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))),
    # LF_ctd_marker_induce
    # Example(
    #     name='LF_ctd_marker_induce',
    #     explanation="""Label True because
    #         (
    #             (the disease is immediately after the chemical and the chemical contains 'induc' or 'assoc')
    #             or
    #             ('induced by', 'caused by', or 'due to' is between the disease and the chemical)
    #         )
    #         and 
    #         (the pair of canonical ids of the chemical and disease is in ctd_marker)""",
    #     paraphrase="""Label true because 
    #         (
    #             (the disease is immediately preceded by the chemical, and the chemical name contains an "induc" or "assoc" root)
    #             or 
    #             ("induced by", "caused by", or "due to" appears between the chemical and the disease)
    #         )
    #         and
    #         (the pair of the chemical and the disease canonical IDs appears in the ctd_marker dictionary.)""",
    #     candidate=-305419566691337972,
    #     denotation=1,
    #     semantics=('.root', ('.label', ('.bool', True), ('.and', ('.or', ('.and', ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.arg_to_string', ('.arg', ('.int', 2)))), ('.call', ('.composite_or', ('.contains',), ('.list', ('.string', u'induc'), ('.string', u'assoc'))), ('.arg_to_string', ('.arg', ('.int', 1))))), ('.any', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 2)), ('.arg', ('.int', 1)))))), ('.list', ('.string', u'induced by'), ('.string', u'caused by'), ('.string', u'due to'))))), ('.call', ('.in', ('.user_list', ('.string', u'ctd_marker'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))),
    # LF_ctd_therapy_treat
    Example(
        name='LF_ctd_therapy_treat',
        explanation="""Label false because 
            (any word between the chemical and the disease contains a treat word and the chemical is left of the 
            disease)
            and 
            (the pair of canonical ids of the chemical and disease is in ctd_therapy)""",
        paraphrase="""Label false because
            (the chemical comes before the disease, and a word between them contains a treat word)
            and
            (the pair of the chemical and the disease canonical IDs appears in the ctd_therapy dictionary.)""",
        candidate=9013931201987912271,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.and', ('.any', ('.map', ('.composite_or', ('.contains',), ('.user_list', ('.string', u'treat'))), ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.arg_to_string', ('.arg', ('.int', 1))))), ('.call', ('.in', ('.user_list', ('.string', u'ctd_therapy'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))),
    # LF_ctd_unspecified_treat
    Example(
        name='LF_ctd_unspecified_treat',
        explanation="""Label false because 
            (any word between the chemical and the disease contains a treat word and the chemical is left of the 
            disease)
            and 
            (the pair of canonical ids of the chemical and disease is in ctd_unspecified)""",
        paraphrase="""Label false because
            (the chemical comes before the disease, and a word between them contains a treat word)
            and
            (the pair of the chemical and the disease canonical IDs appears in the ctd_unspecified dictionary.)""",
        candidate=-6222536315024461563,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.and', ('.any', ('.map', ('.composite_or', ('.contains',), ('.user_list', ('.string', u'treat'))), ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.arg_to_string', ('.arg', ('.int', 1))))), ('.call', ('.in', ('.user_list', ('.string', u'ctd_unspecified'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))),
    # LF_ctd_unspecified_induce
    # Example(
    #     name='LF_ctd_unspecified_induce',
    #     explanation="""Label True because
    #         (
    #             (the disease is immediately after the chemical and the chemical contains 'induc' or 'assoc')
    #             or
    #             ('induced by', 'caused by', or 'due to' is between the disease and the chemical)
    #         )
    #         and 
    #         (the pair of canonical ids of the chemical and disease is in ctd_unspecified)""",
    #     paraphrase="""Label true because 
    #         (
    #             (the disease is immediately preceded by the chemical, and the chemical name contains an "induc" or "assoc" root)
    #             or 
    #             ("induced by", "caused by", or "due to" appears between the chemical and the disease)
    #         )
    #         and
    #         (the pair of the chemical and the disease canonical IDs appears in the ctd_unspecified dictionary.)""",
    #     candidate=-249729854237013355,
    #     denotation=1,
    #     semantics=('.root', ('.label', ('.bool', True), ('.and', ('.or', ('.and', ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.arg_to_string', ('.arg', ('.int', 2)))), ('.call', ('.composite_or', ('.contains',), ('.list', ('.string', u'induc'), ('.string', u'assoc'))), ('.arg_to_string', ('.arg', ('.int', 1))))), ('.any', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 2)), ('.arg', ('.int', 1)))))), ('.list', ('.string', u'induced by'), ('.string', u'caused by'), ('.string', u'due to'))))), ('.call', ('.in', ('.user_list', ('.string', u'ctd_unspecified'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))),
    # LF_d_following_c
    Example(
        name='LF_d_following_c',
        explanation="""Label true because 'following' is between the disease 
            and the chemical and any word after the chemical contains a 
            procedure word""",
        paraphrase="""Label True because after the chemical is a word that contains a procedure root, 
            and the word "following" appears between the chemical and the disease.""",
        candidate=-6971513852802444953,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 2)), ('.arg', ('.int', 1)))))), ('.string', u'following')), ('.any', ('.map', ('.composite_or', ('.contains',), ('.user_list', ('.string', u'procedure'))), ('.extract_text', ('.right', ('.arg', ('.int', 1)))))))))),
    # LF_d_induced_by_c
    Example(
        name='LF_d_induced_by_c',
        explanation="""Label True because 'induced by', 'caused by', or 'due to' 
            is between the disease and the chemical.""",
        paraphrase="""Label True because "induced by", "caused by", or "due to" 
        appears between the chemical and the disease.""",
        candidate=-6762188659294394913,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.any', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 2)), ('.arg', ('.int', 1)))))), ('.list', ('.string', u'induced by'), ('.string', u'caused by'), ('.string', u'due to'))))))),
    # LF_d_induced_by_c_tight
    Example(
        name='LF_d_induced_by_c_tight',
        explanation="""Label True because 'induced by', 'caused by', or 'due to' 
            is between the disease and the chemical and 'by' or 'to' is 
            immediately to the left of the chemical.""",
        paraphrase="""Label true because the chemical is immediately preceded by 
            the word "by" or "to", and the words "induced by", "caused by", or "due to" 
            appear between the chemical and the disease.""",
        candidate=-8780309308829124768,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.any', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 2)), ('.arg', ('.int', 1)))))), ('.list', ('.string', u'induced by'), ('.string', u'caused by'), ('.string', u'due to')))), ('.any', ('.map', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.list', ('.string', u'by'), ('.string', u'to')))))))),
    # LF_d_treat_c
    Example(
        name='LF_d_treat_c',
        explanation="""Label false because any word between the chemical and 
            the disease contains a treat word and the chemical is within 100
            characters to the right of the disease""",
        paraphrase="""Label false because the disease precedes the chemical by no more than 100 characters, 
            and at least word between them contains a treat word.""",
        candidate=192760603909025752,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.any', ('.map', ('.composite_or', ('.contains',), ('.user_list', ('.string', u'treat'))), ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 100), ('.string', 'chars')))), ('.arg_to_string', ('.arg', ('.int', 1)))))))),
    # LF_develop_d_following_c
    Example(
        name='LF_develop_d_following_c',
        explanation="""Label true because any word before the chemical contains 
            'develop' and 'following' is between the disease and the chemical""",
        paraphrase="""Label true because a word containing 'develop' appears somewhere before the chemical, 
            and the word 'following' is between the disease and the chemical.""",
        candidate=-1817051214703978965,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.any', ('.map', ('.contains', ('.string', u'develop')), ('.extract_text', ('.left', ('.arg', ('.int', 1)))))), ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 2)), ('.arg', ('.int', 1)))))), ('.string', u'following')))))),
    # LF_far_c_d
    Example(
        name='LF_far_c_d',
        explanation="""Label false if the disease is more than 100 characters
            to the right of the chemical.""",
        paraphrase="""Label false because the chemical appears more than 100 characters before the disease.""",
        candidate=6240026992471976183,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.gt'), ('.int', 100), ('.string', 'chars')))), ('.arg_to_string', ('.arg', ('.int', 2))))))),
    # LF_far_d_c
    Example(
        name='LF_far_d_c',
        explanation="""Label false if the chemical is more than 100 characters
            to the right of the disease.""",
        paraphrase="""Label false because the disease appears more than 100 characters before the chemical.""",
        candidate=-5736847953411058109,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2)), ('.string', '.gt'), ('.int', 100), ('.string', 'chars')))), ('.arg_to_string', ('.arg', ('.int', 1))))))),
    # LF_improve_before_disease
    Example(
        name='LF_improve_before_disease',
        explanation="""Label false if any word before the disease starts with 'improv'""",
        paraphrase="""Label false because a word starting with "improv" appears before the chemical.""",
        candidate=4358774324608031121,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.startswith', ('.string', u'improv')), ('.extract_text', ('.left', ('.arg', ('.int', 2))))))))),
    # LF_in_ctd_unspecified
    Example(
        name='LF_in_ctd_unspecified',
        explanation="""Label false if the pair of canonical ids of the chemical 
            and disease is in ctd_unspecified""",
        paraphrase="""Label false because the pair of canonical IDs of the 
            chemical and the disease are in the ctd_unspecified dictionary.""",
        candidate=-5889490471583847150,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.user_list', ('.string', u'ctd_unspecified'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))))),
    # LF_in_ctd_therapy
    Example(
        name='LF_in_ctd_therapy',
        explanation="""Label false if the pair of canonical ids of the chemical 
            and disease is in ctd_therapy""",
        paraphrase="""Label false because the pair of canonical IDs of the 
            chemical and the disease are in the ctd_therapy dictionary.""",
        candidate=1928996051652884359,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.user_list', ('.string', u'ctd_therapy'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))))),
    # LF_in_ctd_marker
    Example(
        name='LF_in_ctd_marker',
        explanation="""Label true if the pair of canonical ids of the chemical 
            and disease is in ctd_marker""",
        paraphrase="""Label true because the pair of canonical IDs of the 
            chemical and the disease are in the ctd_marker dictionary.""",
        candidate=-5889490471583847150,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.user_list', ('.string', u'ctd_marker'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))))),
    # LF_in_patient_with
    Example(
        name='LF_in_patient_with',
        explanation="""Label false if any patient phrase is within four words 
            before the disease""",
        paraphrase="""Label false because a patient phrase comes no more than 
            four words before the disease.""",
        candidate=-1516295839967862351,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 4), ('.string', 'words')))), ('.user_list', ('.string', u'patient'))))))),
    # LF_induce
    Example(
        name='LF_induce',
        explanation="""Label true because any word between the chemical and the 
            disease contains 'induc'""",
        paraphrase="""Label true because a word between the chemical and the 
            disease contains "induc".""",
        candidate=-6270620972052954916,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.any', ('.map', ('.contains', ('.string', u'induc')), ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))),
    # LF_induce_name
    Example(
        name='LF_induce_name',
        explanation="Label True because the chemical contains 'induc'",
        paraphrase="""Label True because the chemical contains "induc".""",
        candidate=3240895064801201846,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.contains', ('.string', u'induc')), ('.arg_to_string', ('.arg', ('.int', 1))))))),
    # LF_induced_other
    Example(
        name='LF_induced_other',
        explanation="""Label false if any word between the chemical and the 
            disease ends with 'induced'""",
        paraphrase="""Label false because a word between the chemical and the 
            disease ends with "induced".""",
        candidate=2418695948208481836,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.endswith', ('.string', u'induced')), ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))),
    # LF_level
    Example(
        name='LF_level',
        explanation="""Label false because 'level' comes after the chemical""",
        paraphrase="""Label false because the word "level" comes after the chemical.""",
        candidate=7137204889488246129,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1))))), ('.string', u'level'))))),
    # LF_measure
    Example(
        name='LF_measure',
        explanation="""Label false because any word before the chemical starts 
            with 'measur'""",
        paraphrase="""Label false because a word before the chemical starts 
            with "measur".""",
        candidate=4105760717408167415,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.startswith', ('.string', u'measur')), ('.extract_text', ('.left', ('.arg', ('.int', 1))))))))),
    # LF_neg_d
    Example(
        name='LF_neg_d',
        explanation="""Label false because 'none', 'not', or 'no' is within 30 
            characters to the left of the disease""",
        paraphrase="""Label false because "none", "not", or "no" precedes the 
            disease by no more than 30 characters.
        """,
        candidate=7708285380769583739,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 30), ('.string', 'chars')))), ('.list', ('.string', u'none'), ('.string', u'not'), ('.string', u'no'))))))),
    # LF_risk_d
    Example(
        name='LF_risk_d',
        explanation="""Label true because the phrase 'risk of' occurs before 
            the disease""",
        paraphrase="""Label true because "risk of" comes before the disease.""",
        candidate=4499078534190694908,
        denotation=1,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.string', u'risk of'))))),
    # LF_treat_d
    Example(
        name='LF_treat_d',
        explanation="""Label false because at least one treat word is less than
            50 characters before the disease""",
        paraphrase="""Label false because there is at least one treat word 
            no more than 50 characters before the disease.""",
        candidate=-4670194985477947653,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.geq', ('.int', 1)), ('.sum', ('.map', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.lt'), ('.int', 50), ('.string', 'chars')))), ('.user_list', ('.string', u'treat')))))))),
    # LF_uncertain
    Example(
        name='LF_uncertain',
        explanation="""Label false if any word before the chemical starts with 
            an uncertain word""",
        paraphrase="""Label false because the chemical is preceded by a word 
            that starts with a word that appears in the uncertain dictionary.
        """,
        candidate=1589307577177419147,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.composite_or', ('.startswith',), ('.user_list', ('.string', u'uncertain'))), ('.extract_text', ('.left', ('.arg', ('.int', 1))))))))),
    # LF_weak_assertions
    Example(
        name='LF_weak_assertions',
        explanation="""Label false because at least one weak phrase is in 
            the sentence""",
        paraphrase="""Label false because at least one weak phrase is in the sentence.""",
        candidate=8898005229761872427,
        denotation=-1,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.geq', ('.int', 1)), ('.sum', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'weak')))))))),
]


def get_examples(which, candidates):
    if which=='semparse_test':
        examples = test_examples
    elif which=='semparse_spouse':
        examples = spouse_examples
    elif which=='semparse_cdr':
        examples = cdr_examples
    else:
        raise Exception("Invalid example set provided.")
    
    candidate_dict = {hash(c) : c for c in candidates}
    for example in examples:
        if example.candidate and not isinstance(example.candidate, tuple):
            example.candidate = candidate_dict[hash(example.candidate)]
    # assert(example.candidate is not None for example in examples)
    return examples