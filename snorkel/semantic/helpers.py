def get_left_tokens(span, attrib='words'):
    """
    Returns the tokens between span0 and span1
    """
    i = span.get_word_start()
    return span.get_parent()._asdict()[attrib][:i][::-1]

def get_right_tokens(span, attrib='words'):
    """
    Returns the tokens between span0 and span1
    """
    i = span.get_word_end()
    return span.get_parent()._asdict()[attrib][i+1:]

def get_between_tokens(span0, span1, attrib='words'):
    """
    Returns the tokens between span0 and span1
    """
    if span0.get_word_start() < span1.get_word_start():
        left_span = span0
        dist_btwn = span1.get_word_start() - span0.get_word_end() - 1
    else:
        left_span = span1
        dist_btwn = span0.get_word_start() - span1.get_word_end() - 1
    i = left_span.get_word_end()
    return left_span.get_parent()._asdict()[attrib][i+1:i+1+dist_btwn]

def get_sentence_tokens(span, attrib='words'):
    """
    Returns the tokens in the sentence of the span
    """
    return span.get_parent()._asdict()[attrib]

def lf_helpers():
    return {'get_left_tokens': get_left_tokens,
            'get_right_tokens': get_right_tokens,
            'get_between_tokens': get_between_tokens,
            'get_sentence_tokens': get_sentence_tokens,
            }