
class Example(object):
    def __init__(self, explanation=None, candidate=None, denotation=None):
        self.explanation = explanation
        self.candidate = candidate
        self.denotation = denotation # True label on this candidate

    def __str__(self):
        return 'Example("%s")' % (self.input)
    
    def display(self):
        print 'Example'
        print('%-12s %s' % ('explanation', self.explanation))
        print('%-12s %s' % ('candidate', self.candidate))
        print('%-12s %d' % ('denotation', self.denotation))


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
        denotation=1),
    # And
    Example(
        explanation="label True because True and True",
        candidate=('foo', 'bar'),
        denotation=1),
    # Or
    Example(
        explanation="label True because False or True",
        candidate=('foo', 'bar'),
        denotation=1),
    # Not
    Example(
        explanation="label True because not False",
        candidate=('foo', 'bar'),
        denotation=1),
    # Equals (String)
    Example(
        explanation="label True because 'yes' equals 'yes'",
        candidate=('foo', 'bar'),
        denotation=1),
    # Equals (Int)
    Example(
        explanation="label True because 1 is equal to 1",
        candidate=('foo', 'bar'),
        denotation=1),
    # Integers (digit or text)
    Example(
        explanation="label True because 1 is equal to one",
        candidate=('foo', 'bar'),
        denotation=1),
    # Less than
    Example(
        explanation="label True because 1 is less than 2",
        candidate=('foo', 'bar'),
        denotation=1),
    # At most
    Example(
        explanation="label True because 2 is less than or equal to 2",
        candidate=('foo', 'bar'),
        denotation=1),
    # Greater than
    Example(
        explanation="label True because 2 > 1",
        candidate=('foo', 'bar'),
        denotation=1),
    # At least
    Example(
        explanation="label True because 2 is at least 2",
        candidate=('foo', 'bar'),
        denotation=1),
    # Lowercase
    Example(
        explanation="label True because arg 1 is lowercase",
        candidate=('foo', 'bar'),
        denotation=1),
    # Uppercase
    Example(
        explanation="label True because arg 1 is upper case",
        candidate=('FOO', 'bar'),
        denotation=1),
    # Capitalized
    Example(
        explanation="label True because arg 1 is capitalized",
        candidate=('Foo', 'bar'),
        denotation=1),
    # Starts with
    Example(
        explanation="label True because the word 'blueberry' starts with 'blue'",
        candidate=('foo', 'bar'),
        denotation=1),
    # Ends with
    Example(
        explanation="label True because the word 'blueberry' ends with 'berry'",
        candidate=('foo', 'bar'),
        denotation=1),
    # Candidate as string
    Example(
        explanation="label True because argument 1 equals 'foo'",
        candidate=('foo', 'bar'),
        denotation=1),
    # In
    Example(
        explanation="label True because 'bar' is in 'foobarbaz'",
        candidate=('foo', 'bar'),
        denotation=1),
    # Not Inversion
    Example(
        explanation="label True because 'rab' is not in 'foobarbaz'",
        candidate=('foo', 'bar'),
        denotation=1),
    # Contains
    Example(
        explanation="label True because the word 'foobarbaz' contains 'oobarba'",
        candidate=('foo', 'bar'),
        denotation=1),
    # List
    Example(
        explanation="label True because arg 2 equals 'foo', 'bar', or 'baz'",
        candidate=('foo', 'bar'),
        denotation=1),
    # UserList
    Example(
        explanation="label True because 'blue' in colors",
        candidate=('foo', 'bar'),
        denotation=1),
   # OrList left
    Example(
        explanation="label True because 'blue' or 'shmoo' is in colors",
        candidate=('foo', 'bar'),
        denotation=1),
   # OrList right
    Example(
        explanation="label True because 'blue' ends with 'moe' or 'lue'",
        candidate=('foo', 'bar'),
        denotation=1),
    # AndList left
    Example(
        explanation="label True because 'blue' and 'red' are in colors",
        candidate=('foo', 'bar'),
        denotation=1),
    # AndList right
    Example(
        explanation="label True because 'blue' contains 'l' and 'u'",
        candidate=('foo', 'bar'),
        denotation=1),
    # Left words (list)
    Example(
        explanation="label True because 'wife' is in the words left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),    
    # Right words (list)
    Example(
        explanation="label True because 'wife' is in the words to the right of arg 2",
        candidate=-3658950303959694808,
        denotation=1),    
    # Between words (list)
    Example(
        explanation="label True because 'wife' is in the words between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1),    
    # Sentence (list)
    Example(
        explanation='label True because "wife" is in the sentence',
        candidate=-3658950303959694808,
        denotation=1),
    # Index left
    Example(
        explanation="label True because arg 2 is left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Index right
    Example(
        explanation="label True because arg 1 is right of arg 2",
        candidate=-3658950303959694808,
        denotation=1),
    # Index left equality
    Example(
        explanation="label True because 'wife' is one word to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Index left inequality 0
    Example(
        explanation="label True because arg 2 is more than three words to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Index left inequality 1
    Example(
        explanation="label True because not arg 2 is more than fifty words to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Index within (<=)
    Example(
        explanation="label True because 'wife' is within three words to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Index OrList left
    Example(
        explanation="label True because 'husband' or 'wife' is within three words to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Index AndList left
    Example(
        explanation="label True because not 'husband' and 'wife' are within three words to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # # Index OrList right
    # Example(
    #     explanation="label True because 'wife' is less than three words to the left of arg 1 or arg2",
    #     candidate=-3658950303959694808,
    #     denotation=1),
    # # Index within
    # Example(
    #     explanation="label True because 'wife' is within three words of arg 1",
    #     candidate=-3658950303959694808,
    #     denotation=1),
    # # Index without
    # Example(
    #     explanation="label True because arg 1 is not within 5 words of arg 2",
    #     candidate=-3658950303959694808,
    #     denotation=1),
    # Between
    Example(
        explanation="label True because 'wife' is between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1),
    # Characters0
    Example(
        explanation="label True because 'wife' is less than 10 characters to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Characters1
    Example(
        explanation="label True because 'wife' is more than 20 characters to the right of arg 2",
        candidate=-3658950303959694808,
        denotation=1),
    # Paraphrase0
    Example(
        explanation="label True because 'wife' is immediately to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Tokens
    Example(
        explanation="label True because at least one word to the left of arg 1 is lower case",
        candidate=-3658950303959694808,
        denotation=1),    
    # POS
    Example(
        explanation="label True because at least one noun exists between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1),
    # NER
    Example(
        explanation="label True because there are no people between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1),
    # Count0
    Example(
        explanation="label True because there are not three people in the sentence",
        candidate=-3658950303959694808,
        denotation=1),
    # Count1
    Example(
        explanation="label True because the number of words between arg 1 and arg 2 is less than 25",
        candidate=-3658950303959694808,
        denotation=1),
    # Count2
    Example(
        explanation="label True because there are more than 3 words between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1),
    # Count3
    Example(
        explanation="label True because at least one word exists between arg 1 and arg 2",
        candidate=-3658950303959694808,
        denotation=1),
    # Count4
    Example(
        explanation="label True because there are two nouns to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Count5
    Example(
        explanation="label True because there are less than three nouns to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Count6
    Example(
        explanation="label True because there are not more than two nouns to the left of arg 1",
        candidate=-3658950303959694808,
        denotation=1),
    # Count7
    Example(
        explanation="label True because at least one word to the left of arg 1 starts with a spouse word",
        candidate=-3658950303959694808,
        denotation=1),
    # # Intersection0
    # Example(
    #     explanation="label True because there is at least one word from colors in the bluebird words",
    #     candidate=('foo', 'bar'),
    #     denotation=1),
    # # Intersection1
    # Example(
    #     explanation="label True because less than two colors words are in bluebird",
    #     candidate=('foo', 'bar'),
    #     denotation=1),
    # # Disjoint
    # Example(
    #     explanation="label True because there are no colors words in the greek words",
    #     candidate=('foo', 'bar'),
    #     denotation=1),
    # All
    Example(
        explanation='label True because all of the colors are lowercase',
        candidate=('foo', 'bar'),
        denotation=1),
    # Any
    Example(
        explanation='label True because any of the letters are lowercase',
        candidate=('foo', 'bar'),
        denotation=1),
    # None
    Example(
        explanation='label True because none of the smalls are capitalized',
        candidate=('foo', 'bar'),
        denotation=1),
#     # Composition0
#     Example(
#         explanation="label True because 'wife' is between arg 1 and arg 2 and 'years' is to the left of arg 1",
#         candidate=-3658950303959694808,
#         denotation=1),
#     # Composition1
#     Example(
#         explanation="label True because arg 1 is identical to arg 2",
#         candidate=('foo', 'foo'),
#         denotation=1),
#     # Composition2
#     Example(
#         explanation="label True because there is at least one spouse word between arg 1 and arg 2",
#         candidate=-3658950303959694808,
#         denotation=1),
#     # Composition3
#     Example(
#         explanation="label True because there is at least one spouse word within two words to the left of arg 1 or arg 2",
#         candidate=-3658950303959694808,
#         denotation=1),
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
        denotation=-1),
    Example(
        explanation="Label false because there is a person between arg 1 and arg 2",
        candidate=-8692729291220282012,
        denotation=-1),
    Example(
        explanation="Label true because there is at least one spouse word in the words between arg 1 and arg 2",
        candidate=-3135315734051751361,
        denotation=1),
    Example(
        explanation="Label true because there is at least one spouse word within two words to the left of arg 1 or arg 2",
        candidate=-7563346943193853808,
        denotation=1),
    Example(
        explanation="Label false because there are no spouse words in the sentence",
        candidate=-8021416815354059709,
        denotation=-1),
    Example(
        explanation="Label true because the word 'and' is between arg 1 and arg 2 and 'married' is to the right of arg 2",
        candidate=None,
        denotation=1),
    Example(
        explanation="Label false because there are no spouse words in the sentence",
        candidate=-8021416815354059709,
        denotation=-1),
    Example(
        explanation="Label false because there is at least one family word between arg 1 and arg 2",
        candidate=-8692729291220282012,
        denotation=-1),
    Example(
        explanation="Label false because arg 1 is identical to arg 2",
        candidate=660552142898381681,
        denotation=-1),
]


cdr_examples = [
    ### TESTING ###
    # Example(
    #     explanation="Label True because the chemical is to the left of the disease",
    #     candidate=-5889490471583847150,
    #     denotation=1
    # ),    
    ### TESTING ###
    # LF_c_cause_d
    Example(
        explanation="""Label true because any causal phrase is between the 
            chemical and the disease and the word 'not' is not between the 
            chemical and the disease""",
        candidate=6606713828167518488,
        denotation=1),
    # LF_c_d
    Example(
        explanation="Label true because the disease is immediately after the chemical",
        candidate=4911918761913559389,
        denotation=1),
    # LF_c_induced_d
    Example(
        explanation="""Label true because the disease is immediately after the 
            chemical and 'induc' or 'assoc' is in the chemical""",
        candidate=6618773943628884463,
        denotation=1),
    # LF_c_treat_d
    Example(
        explanation="""Label false because any word between the chemical and 
            the disease contains a treat word and the chemical is within 100 
            characters to the left of the disease""",
        candidate=5000202430163451980,
        denotation=-1),
    # LF_c_treat_d_wide
    Example(
        explanation="""Label false because any word between the chemical and 
            the disease contains a treat word and the chemical is left of the 
            disease""",
        candidate=-5412508044020208858,
        denotation=-1),
    # # LF_closer_chem
    # Example(
    #     explanation=None,
    #     candidate=-1954799400282697253,
    #     denotation=-1),
    # # LF_closer_dis
    # Example(
    #     explanation=None,
    #     candidate=-130640710948826159,
    #     denotation=-1),
    # # LF_ctd_marker_c_d
    # Example(
    #     explanation=None,
    #     candidate=3829603392041554457,
    #     denotation=1),
    # # LF_ctd_marker_induce
    # Example(
    #     explanation=None,
    #     candidate=-305419566691337972,
    #     denotation=1),
    # # LF_ctd_therapy_treat
    # Example(
    #     explanation=None,
    #     candidate=9013931201987912271,
    #     denotation=-1),
    # # LF_ctd_unspecified_treat
    # Example(
    #     explanation=None,
    #     candidate=-6222536315024461563,
    #     denotation=-1),
    # # LF_ctd_unspecified_induce
    # Example(
    #     explanation=None,
    #     candidate=-249729854237013355,
    #     denotation=1),
    # LF_d_following_c
    Example(
        explanation="""Label true because 'following' is between the disease 
            and the chemical and any word after the chemical contains a 
            procedure word""",
        candidate=None,
        denotation=1),
    # LF_d_induced_by_c
    Example(
        explanation="""Label True because 'induced by', 'caused by', or 'due to' 
            is between the disease and the chemical.""",
        candidate=-6762188659294394913,
        denotation=1),
    # LF_d_induced_by_c_tight
    Example(
        explanation=None,
        candidate=-8780309308829124768,
        denotation=1),
    # LF_d_treat_c
    Example(
        explanation="""Label false because any word between the chemical and 
            the disease contains a treat word and the chemical is within 100
            characters to the right of the disease""",
        candidate=192760603909025752,
        denotation=-1),
    # LF_develop_d_following_c
    Example(
        explanation=None,
        candidate=-1817051214703978965,
        denotation=1),
    # LF_far_c_d
    Example(
        explanation=None,
        candidate=6240026992471976183,
        denotation=-1),
    # LF_far_d_c
    Example(
        explanation=None,
        candidate=-5736847953411058109,
        denotation=-1),
    # LF_improve_before_disease
    Example(
        explanation=None,
        candidate=None,
        denotation=-1),
    # LF_in_ctd_unspecified
    Example(
        explanation=None,
        candidate=-5889490471583847150,
        denotation=-1),
    # LF_in_ctd_therapy
    Example(
        explanation=None,
        candidate=1928996051652884359,
        denotation=-1),
    # LF_in_ctd_marker
    Example(
        explanation=None,
        candidate=-5889490471583847150,
        denotation=1),
    # LF_in_patient_with
    Example(
        explanation=None,
        candidate=-1516295839967862351,
        denotation=-1),
    # LF_induce
    Example(
        explanation="Label true because any word between the chemical and the disease contains 'induc'",
        candidate=-6270620972052954916,
        denotation=1),
    # LF_induce_name
    Example(
        explanation="Label True because the chemical contains 'induc'",
        candidate=3240895064801201846,
        denotation=1),
    # LF_induced_other
    Example(
        explanation="Label false if any word between the chemical and the disease ends with 'induced'",
        candidate=2418695948208481836,
        denotation=-1),
    # LF_level
    Example(
        explanation=None,
        candidate=7137204889488246129,
        denotation=-1),
    # LF_measure
    Example(
        explanation=None,
        candidate=4105760717408167415,
        denotation=-1),
    # LF_neg_d
    Example(
        explanation=None,
        candidate=7708285380769583739,
        denotation=-1),
    # LF_risk_d
    Example(
        explanation=None,
        candidate=4499078534190694908,
        denotation=1),
    # LF_treat_d
    Example(
        explanation=None,
        candidate=-4670194985477947653,
        denotation=-1),
    # LF_uncertain
    Example(
        explanation="Label false if any word before the chemical starts with an uncertain word",
        candidate=1589307577177419147,
        denotation=-1),
    # LF_weak_assertions
    Example(
        explanation=None,
        candidate=8898005229761872427,
        denotation=-1),
]


def get_examples(which, candidates):
    if which=='test':
        examples = test_examples
    elif which=='spouse':
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