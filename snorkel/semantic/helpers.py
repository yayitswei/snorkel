from collections import namedtuple

# VERSION 1

# def get_left_tokens(span, attrib='words'):
#     """
#     Returns the tokens between span0 and span1
#     """
#     i = span.get_word_start()
#     return span.get_parent()._asdict()[attrib][:i][::-1]

# def get_right_tokens(span, attrib='words'):
#     """
#     Returns the tokens between span0 and span1
#     """
#     i = span.get_word_end()
#     return span.get_parent()._asdict()[attrib][i+1:]

# def get_between_tokens(span0, span1, attrib='words'):
#     """
#     Returns the tokens between span0 and span1
#     """
#     if span0.get_word_start() < span1.get_word_start():
#         left_span = span0
#         dist_btwn = span1.get_word_start() - span0.get_word_end() - 1
#     else:
#         left_span = span1
#         dist_btwn = span0.get_word_start() - span1.get_word_end() - 1
#     i = left_span.get_word_end()
#     return left_span.get_parent()._asdict()[attrib][i+1:i+1+dist_btwn]

# def get_sentence_tokens(span, attrib='words'):
#     """
#     Returns the tokens in the sentence of the span
#     """
#     return span.get_parent()._asdict()[attrib]

# VERSION 2

# def get_left_tokens(span):
    # i = span.get_word_start()
    # sent = span.get_parent()
    # partial = {}
    # for key, values in sent._asdict().iteritems():
    #     if key in relevant:
    #         partial[key] = values[:i]
    # return partial

# def get_right_tokens(span):
#     i = span.get_word_start()
#     sent = span.get_parent()
#     partial = {}
#     for key, values in sent._asdict().iteritems():
#         if key in relevant:
#             partial[key] = values[i+1:]
#     return partial

# def get_between_tokens(span0, span1):
#     if span0.get_word_start() < span1.get_word_start():
#         left_span = span0
#         dist_btwn = span1.get_word_start() - span0.get_word_end() - 1
#     else:
#         left_span = span1
#         dist_btwn = span0.get_word_start() - span1.get_word_end() - 1
#     i = left_span.get_word_end()
#     sent = span0.get_parent()
#     partial = {}
#     for key, values in sent._asdict().iteritems():
#         if key in relevant:
#             partial[key] = values[i+1:i+1+dist_btwn]
#     return partial

# def get_sentence_tokens(span):
#     sent = span.get_parent()
#     partial = {}
#     for key, values in sent._asdict().iteritems():
#         if key in relevant:
#             partial[key] = values
#     return partial

# VERSION 3
fields = ['words', 'char_offsets', 'pos_tags', 'ner_tags', 'entity_types']
Token = namedtuple('Token', fields)

def get_left_tokens(span):
    tokens = []
    k = span.get_word_start()
    sent = span.get_parent()._asdict()
    for i in range(k):
        tokens.append(Token(*[sent[field][i] for field in fields]))
    return tokens

def get_right_tokens(span):
    tokens = []
    k = span.get_word_start()
    sent = span.get_parent()._asdict()
    for i in range(k+1, len(sent['words'])):
        tokens.append(Token(*[sent[field][i] for field in fields]))
    return tokens

def get_between_tokens(span0, span1):
    tokens = []
    if span0.get_word_start() < span1.get_word_start():
        left_span = span0
        dist_btwn = span1.get_word_start() - span0.get_word_end() - 1
    else:
        left_span = span1
        dist_btwn = span0.get_word_start() - span1.get_word_end() - 1
    k = left_span.get_word_end()
    sent = span0.get_parent()._asdict()
    for i in range(k+1, k+1+dist_btwn):
        tokens.append(Token(*[sent[field][i] for field in fields]))
    return tokens

def get_sentence_tokens(span):
    tokens = []
    k = span.get_word_start()
    sent = span.get_parent()._asdict()
    for i in range(len(sent['words'])):
        tokens.append(Token(*[sent[field][i] for field in fields]))
    return tokens

def lf_helpers():
    return {'get_left_tokens': get_left_tokens,
            'get_right_tokens': get_right_tokens,
            'get_between_tokens': get_between_tokens,
            'get_sentence_tokens': get_sentence_tokens,
            }