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
"""
Convert spelled numbers into numeric values or digit strings.
"""

from typing import List, Optional

from text_to_num.lang import Language

##


class WordStreamValueParser:
    """The actual value builder engine.

    The engine incrementaly recognize a stream of words as a valid number and build the
    corresponding numeric (interger) value.

    The algorithm is based on the observation that humans gather the
    digits by group of three to more easily speak them out.
    And indeed, the language uses powers of 1000 to structure big numbers.

    Public API:

        - ``self.push(word)``
        - ``self.value: int``
    """

    def __init__(self, lang: Language, relaxed: bool = False) -> None:
        """Initialize the parser.

        If ``relaxed`` is True, we treat the sequence "quatre vingt" as
        a single "quatre-vingt".
        """
        self.lang = lang
        self.relaxed = relaxed
        self.skip: Optional[str] = None
        self.n000_val: int = 0  # the number value part > 1000
        self.grp_val: int = 0  # the current three digit group value
        self.last_word: Optional[
            str
        ] = None  # the last valid word for the current group

    @property
    def value(self) -> int:
        """At any moment, get the value of the currently recognized number."""
        return self.n000_val + self.grp_val

    def group_expects(self, word: str, update: bool = True) -> bool:
        """Does the current group expect ``word`` to complete it as a valid number?
        ``word`` should not be a multiplier; multiplier should be handled first.
        """
        expected = False
        if self.last_word is None:
            expected = True
        elif (
            self.last_word in self.lang.UNITS
            and self.grp_val < 10
            or self.last_word in self.lang.STENS
            and self.grp_val < 20
        ):
            expected = word in self.lang.CENT
        elif self.last_word in self.lang.MTENS:
            expected = (
                word in self.lang.UNITS
                or word in self.lang.STENS
                and self.last_word in self.lang.MTENS_WSTENS
            )
        elif self.last_word in self.lang.CENT:
            expected = word not in self.lang.CENT

        if update:
            self.last_word = word
        return expected

    def is_coef_appliable(self, coef: int) -> bool:
        """Is this multiplier expected?"""
        if coef > self.value and (self.value > 0 or coef == 1000):
            # a multiplier can be applied to anything lesser than itself,
            # as long as it not zero (special case for 1000 which then implies 1)
            return True
        if coef * coef <= self.n000_val:
            # a multiplier can not be applied to a value bigger than itself,
            # so it must be applied to the current group only.
            # ex. for "mille": "deux millions cent cinquante mille"
            # ex. for "millions": "trois milliard deux cent millions"
            # But not twice: "dix mille cinq mille" is invalid for example. Therefore,
            # we test the square of ``coef``.
            return (
                self.grp_val > 0 or coef == 1000
            )  # "mille" without unit before is additive
        # TODO: There is one exception to the above rule: "de milliard"
        # ex. : "mille milliards de milliards"
        return False

    def push(self, word: str, look_ahead: Optional[str] = None) -> bool:
        """Push next word from the stream.

        Don't push punctuation marks or symbols, only words. It is the responsability
        of the caller to handle punctuation or any marker of pause in the word stream.
        The best practice is to call ``self.close()`` on such markers and start again after.

        Return ``True`` if  ``word`` contributes to the current value else ``False``.

        The first time (after instanciating ``self``) this function returns True marks
        the beginning of a number.

        If this function returns False, and the last call returned True, that means you
        reached the end of a number. You can get its value from ``self.value``.

        Then, to parse a new number, you need to instanciate a new engine and start
        again from the last word you tried (the one that has just been rejected).
        """
        if not word:
            return False

        if word == self.lang.AND and look_ahead in self.lang.AND_NUMS:
            return True

        word = self.lang.normalize(word)
        if word not in self.lang.NUMBERS:
            return False

        RELAXED = self.lang.RELAXED

        if word in self.lang.MULTIPLIERS:
            coef = self.lang.MULTIPLIERS[word]
            if not self.is_coef_appliable(coef):
                return False
            # a multiplier can not be applied to a value bigger than itself,
            # so it must be applied to the current group
            if coef < self.n000_val:
                self.n000_val = self.n000_val + coef * (
                    self.grp_val or 1
                )  # or 1 for "mille"
            else:
                self.n000_val = (self.value or 1) * coef

            self.grp_val = 0
            self.last_word = None
        elif (
            self.relaxed
            and word in RELAXED
            and look_ahead
            and look_ahead.startswith(RELAXED[word][0])
            and self.group_expects(RELAXED[word][1], update=False)
        ):
            self.skip = RELAXED[word][0]
            self.grp_val += self.lang.NUMBERS[RELAXED[word][1]]
        elif self.skip and word.startswith(self.skip):
            self.skip = None
        elif self.group_expects(word):
            if word in self.lang.CENT:
                self.grp_val = 100 * self.grp_val if self.grp_val else 100
            else:
                self.grp_val += self.lang.NUMBERS[word]
        else:
            self.skip = None
            return False
        return True


# TODO: Look ahead:  "de milliard"


class WordToDigitParser:
    """Words to digit transcriber.

    The engine incrementaly recognize a stream of words as a valid cardinal, ordinal,
    decimal or formal number (including leading zeros) and build the corresponding digit string.

    Zeros are not treated as isolates but are considered as starting a new formal number
    and are concatenated to the following digit.

    Public API:

     - ``self.push(word, look_ahead)``
     - ``self.close()``
     - ``self.value``: str
    """

    def __init__(
        self, lang: Language, relaxed: bool = False, signed: bool = True
    ) -> None:
        """Initialize the parser.

        If ``relaxed`` is True, we treat the sequence "quatre vingt" as
        a single "quatre-vingt".

        If ``signed`` is True, we parse signed numbers like
        « plus deux » (+2), or « moins vingt » (-20).
        """
        self.lang = lang
        self._value: List[str] = []
        self.int_builder = WordStreamValueParser(lang, relaxed=relaxed)
        self.frac_builder = WordStreamValueParser(lang, relaxed=relaxed)
        self.signed = signed
        self.in_frac = False
        self.closed = False  # For deferred stop
        self.open = False  # For efficiency

    @property
    def value(self) -> str:
        return "".join(self._value)

    def close(self) -> None:
        """Signal end of input if input stream ends while still in a number.

        It's safe to call it multiple times.
        """
        if not self.closed:
            if self.in_frac and self.frac_builder.value:
                self._value.append(str(self.frac_builder.value))
            elif not self.in_frac and self.int_builder.value:
                self._value.append(str(self.int_builder.value))
            self.closed = True

    def at_start_of_seq(self) -> bool:
        """Return true if we are waiting for the start of the integer
        part or the start of the fraction part."""
        return (
            self.in_frac
            and self.frac_builder.value == 0
            or not self.in_frac
            and self.int_builder.value == 0
        )

    def at_start(self) -> bool:
        """Return True if nothing valid parsed yet."""
        return not self.open

    def is_article(self, word: str, following: Optional[str]) -> bool:
        return (
            not self.open
            and word in self.lang.UNIT_ARTICLES
            and self.lang.not_numeric_word(following)
        )

    def _push(self, word: str, look_ahead: Optional[str]) -> bool:
        builder = self.frac_builder if self.in_frac else self.int_builder
        return builder.push(word, look_ahead)

    def push(self, word: str, look_ahead: Optional[str] = None) -> bool:
        """Push next word from the stream.

        Return ``True`` if  ``word`` contributes to the current value else ``False``.

        The first time (after instanciating ``self``) this function returns True marks
        the beginning of a number.

        If this function returns False, and the last call returned True, that means you
        reached the end of a number. You can get its value from ``self.value``.

        Then, to parse a new number, you need to instanciate a new engine and start
        again from the last word you tried (the one that has just been rejected).
        """

        if self.closed or self.is_article(word, look_ahead):
            return False

        if (
            self.signed
            and word in self.lang.SIGN
            and look_ahead in self.lang.NUMBERS
            and self.at_start()
        ):
            self._value.append(self.lang.SIGN[word])
        elif word.startswith(self.lang.ZERO) and self.at_start_of_seq():
            self._value.append("0")
        elif self._push(self.lang.ord2card(word) or "", look_ahead):
            self._value.append(
                self.lang.num_ord(
                    str(
                        self.frac_builder.value
                        if self.in_frac
                        else self.int_builder.value
                    ),
                    word,
                )
            )
            self.closed = True
        elif (
            word == self.lang.DECIMAL_SEP
            and (look_ahead in self.lang.NUMBERS or look_ahead == self.lang.ZERO)
            and not self.in_frac
        ):
            self._value.append(str(self.int_builder.value))
            self._value.append(self.lang.DECIMAL_SYM)
            self.in_frac = True
        elif not self._push(word, look_ahead):
            if self.open:
                self.close()
            return False

        self.open = True
        return True
