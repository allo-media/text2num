# MIT License

# Copyright (c) 2018 Groupe Allo-Media

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

from .parsers import WordStreamValueParser, WordToDigitParser


def look_ahead(sequence):
    """Look-ahead iterator.

    Iterate over a sequence by returning couples (current element, next element).
    The last couple returned before StopIteration is raised, is (last element, None).

    Example:

    >>> for elt, nxt_elt in look_ahead(sequence):
    ... # do something

    """
    maxi = len(sequence) - 1
    for i, val in enumerate(sequence):
        ahead = sequence[i + 1] if i < maxi else None
        yield val, ahead


def text2num(text, relaxed=False):
    """Convert the ``text`` string containing an integer number written in French
    into an integer value.

    Set ``relaxed`` to True if you want to accept "quatre vingt(s)" as "quatre-vingt".

    Raises an AssertionError if ``text`` does not describe a valid number.
    Return an int.
    """

    num_parser = WordStreamValueParser(relaxed=relaxed)
    tokens = text.split()
    if not all(num_parser.push(word, ahead) for word, ahead in look_ahead(tokens)):
        raise ValueError('invalid literal for text2num: {}'.format(repr(text)))
    return num_parser.value


def alpha2digit(text, relaxed=False):
    """Return the text of ``text`` with all the French spelled numbers converted to digits.
    Takes care of punctuation.
    Set ``relaxed`` to True if you want to accept "quatre vingt(s)" as "quatre-vingt".
    """
    segments = re.split(r'\s*[\.,;\(\)…\[\]:!\?]+\s*', text)
    punct = re.findall(r'\s*[\.,;\(\)…\[\]:!\?]+\s*', text)
    if len(punct) < len(segments):
        punct.append('')
    out_segments = []
    for segment, sep in zip(segments, punct):
        tokens = segment.split()
        num_builder = WordToDigitParser(relaxed=relaxed)
        in_number = False
        out_tokens = []
        for word, ahead in look_ahead(tokens):
            if num_builder.push(word.lower(), ahead):
                in_number = True
            elif in_number:
                out_tokens.append(num_builder.value)
                num_builder = WordToDigitParser(relaxed=relaxed)
                in_number = num_builder.push(word.lower(), ahead)
            if not in_number:
                out_tokens.append(word)
        # End of segment
        num_builder.close()
        if num_builder.value:
            out_tokens.append(num_builder.value)
        out_segments.append(' '.join(out_tokens))
        out_segments.append(sep)
    return ''.join(out_segments)
