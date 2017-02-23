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
# fields = ['words', 'char_offsets', 'pos_tags', 'ner_tags', 'entity_types']
# Token = namedtuple('Token', fields)
# phrase_fields = ['words', 'word_offsets', 'char_offsets', 'pos_tags', 'ner_tags', 'entity_types']
# Phrase = namedtuple('Phrase', phrase_fields)

# def get_phrase_from_span(span):
#     contents = []
#     for f in phrase_fields:
#         if f=='word_offsets':
#             word_indices = range(span.get_word_start(), span.get_word_end() + 1)
#             contents.append(word_indices)
#         elif f=='char_offsets':
#             contents.append([span.word_to_char_index(wi) for wi in word_indices])
#         else:
#             contents.append(span.get_attrib_tokens(a=f))
#     return Phrase(*contents)

# def get_phrase_from_text(sentence, text):
#     # TODO: precompute these and hash them with each sentence for speed?
#     import pdb; pdb.set_trace()
#     sent_dict = sentence._asdict()
#     sent_text = sent_dict['text']
#     sent_tokens = sent_dict['words']
#     num_sent_tokens = len(sent_tokens)
#     num_text_tokens = len(text.split())
#     char_starts = []
#     print sent_text
#     print text
#     for L in range(num_text_tokens, num_text_tokens + 2):
#         for i in range(0, len_sent_tokens - L + 1):
#             char_start = sent_dict['char_offsets'][i]
#             char_end = char_start + len(sent_dict['words'][i+L])
#             print sent_text[char_start:char_end]
#             # if sent_text[char_start:char_end]
    
#     # TODO: get char_starts of tokens/phrases only (don't just search in text)
#     # ci = -1
#     # while ci < sent_len:
#     #     ci = sent_text[ci+1:]
#     #     if ci == -1:
#     #         ci = sent_len
#     #     else:
#     #         char_starts.append(ci)
#     return [] # return a list

fields = ['words', 'char_offsets', 'pos_tags', 'ner_tags', 'entity_types']
Phrase = namedtuple('Phrase', fields)

def get_left_tokens(span):
    tokens = []
    k = span.get_word_start()
    sent = span.get_parent()._asdict()
    for i in range(k):
        tokens.append(Phrase(*[[sent[field][i]] for field in fields]))
    return tokens

def get_right_tokens(span):
    tokens = []
    k = span.get_word_start()
    sent = span.get_parent()._asdict()
    for i in range(k+1, len(sent['words'])):
        tokens.append(Phrase(*[[sent[field][i]] for field in fields]))
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
        tokens.append(Phrase(*[[sent[field][i]]for field in fields]))
    return tokens

def get_sentence_tokens(span):
    tokens = []
    k = span.get_word_start()
    sent = span.get_parent()._asdict()
    for i in range(len(sent['words'])):
        tokens.append(Phrase(*[[sent[field][i]]for field in fields]))
    return tokens

def lf_helpers():
    return {
            # 'get_phrase_from_text': get_phrase_from_text,
            # 'get_phrase_from_span': get_phrase_from_span,
            'get_left_tokens': get_left_tokens,
            'get_right_tokens': get_right_tokens,
            'get_between_tokens': get_between_tokens,
            'get_sentence_tokens': get_sentence_tokens,
            }