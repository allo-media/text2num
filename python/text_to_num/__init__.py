"""text_to_num


The function ``find_numbers`` operates on sequence of tokens.

A token is any object that implements the following methods:

    def text(self):
        # return orginal text this token reprensents

    def text_lowercase(self):
        # the lowercase "simplified" representation of the text

    def nt_separated(self, previous):
        # Whether this token and the previous one are "separated" by some non-textual feature.
        # For example, the token may represent Speech-to-text timestamped words, and two consecutive
        # tokens may be separated by some amount of silence that has not been rendered by a punctuation token.


"""


from ._text2num import (Occurence, alpha2digit, find_numbers, text2num)

__all__ = [Occurence, alpha2digit, find_numbers, text2num]
