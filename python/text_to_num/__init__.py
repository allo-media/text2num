"""text_to_num


The function ``find_numbers`` operates on sequence of tokens.

A token is any object that implements the ``Token`` Protocol:

    def text(self):
        # return orginal text this token reprensents

    def nt_separated(self, previous):
        # Whether this token and the previous one are "separated" by some non-textual feature.
        # For example, the token may represent Speech-to-text timestamped words, and two consecutive
        # tokens may be separated by some amount of silence that has not been rendered by a punctuation token.


"""
from abc import abstractmethod
from typing import Protocol

from ._text2num import (Occurence, alpha2digit, find_numbers, text2num)


class Token(Protocol):
    """Protocol for natural language tokens suitable for ``find_numbers```.

    The only mandatory method is ``self.text()``.
    """

    @abstractmethod
    def text(self) -> str:
        """Return the text content of the token."""
        ...

    def nt_separated(self, previous: "Token") -> bool:
        """In some token streams (e.g. ASR output), there is no punctuation
        tokens to separate words that must be undestood separately, but
        the tokens themselves may embed additional information to convey that
        distinction (e.g. timing information that can reveal voice pauses).
        This method should return true if `self` and `previous` are unrelated.

        Default implementation return ``False``.
        """
        return False

    def not_a_number_part(self) -> bool:
        """Despite its form, we have evidence that this token is not a number part.

        Default implementation return ``False``.
        """
        return False


__all__ = [Occurence, Token, alpha2digit, find_numbers, text2num]
