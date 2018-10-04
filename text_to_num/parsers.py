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
Convert French spelled numbers into numeric values or digit strings.
"""

#
# CONSTANTS
# Built once on import.
#

# Those words multiplies lesser numbers (see Rules)
# Exception: "(de) milliards" that can multiply bigger numbers ("milliards de milliards")
# Special case: "cent" is processed apart.
MULTIPLIERS = {
    "mille": 1000,
    "milles": 1000,
    "million": 1000000,
    "millions": 1000000,
    "milliard": 1000000000,
    "milliards": 1000000000,
}

# All number words

NUMBERS = MULTIPLIERS.copy()

# Units are terminals (see Rules)
# Special case: "zéro" is processed apart.
UNITS = {word: value for value, word in enumerate("un deux trois quatre cinq six sept huit neuf".split(), 1)}
# Unit variants
UNITS['une'] = 1

NUMBERS.update(UNITS)

# Single tens are terminals (see Rules)
STENS = {
    word: value
    for value, word in enumerate(
        "dix onze douze treize quatorze quinze seize dix-sept dix-huit dix-neuf".split(), 10)
}

NUMBERS.update(STENS)

# Ten multiples
# Ten multiples may be followed by a unit only;
# Exceptions: "soixante" & "quatre-ving" (see Rules)
MTENS = {
    word: value * 10
    for value, word in enumerate("vingt trente quarante cinquante soixante septante huitante nonante".split(),
                                 2)
}
# Variants
MTENS['quatre-vingt'] = 80
MTENS['octante'] = 80

NUMBERS.update(MTENS)

# "cent" has a special status (see Rules)
CENT = {"cent": 100, "cents": 100}

NUMBERS.update(CENT)

# Composites are tens already composed with terminals in one word.
# Composites are terminals.

COMPOSITES = {
    "-".join((ten_word, unit_word)): ten_val + unit_val
    for ten_word, ten_val in MTENS.items()
    for unit_word, unit_val in UNITS.items() if unit_val != 1
}

COMPOSITES.update({
    "-".join((ten_word, et_word)): ten_val + et_val
    for ten_word, ten_val in MTENS.items()
    for et_word, et_val in (('et-un', 1), ('et-une', 1))
    if 10 < ten_val <= 90
})

COMPOSITES['quatre-vingt-un'] = 81

COMPOSITES.update({
    "-".join((ten_word, sten_word)): ten_val + sten_val
    for ten_word, ten_val in (('soixante', 60), ('quatre-vingt', 80)) for sten_word, sten_val in STENS.items()
})

COMPOSITES['soixante-et-onze'] = 71

NUMBERS.update(COMPOSITES)

SIGN = {'plus': '+', 'moins': '-'}

ET_NUMS = {'un', 'une', 'unième', 'onze', 'onzième'}


def ord2card(word):
    """Convert ordinal number to cardinal.

    Return None if word is not an ordinal.
    """
    source = word[:-4]
    if source == 'cinqu':
        source = 'cinq'
    elif source == 'neuv':
        source = 'neuf'
    elif source not in NUMBERS:
        source = source + 'e'
        if source not in NUMBERS:
            return None
    return source


def not_numeric_word(word):
    return word is not None and word != 'virgule' and word not in NUMBERS


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

    def __init__(self, relaxed=False):
        """Initialize the parser.

        If ``relaxed`` is True, we treat the sequence "quatre vingt" as
        a single "quatre-vingt".
        """
        self.relaxed = relaxed
        self.on_hold = False
        self.n000_val = 0  # the number value part > 1000
        self.grp_val = 0  # the current three digit group value
        self.last_word = None  # the last valid word for the current group

    @property
    def value(self):
        """At any moment, get the value of the currently recognized number."""
        return self.n000_val + self.grp_val

    def group_expects(self, word, update=True):
        """Does the current group expect ``word`` to complete it as a valid number?
        ``word`` should not be a multiplier; multiplier should be handled first.
        """
        expected = False
        if self.last_word is None:
            expected = True
        elif (self.last_word in UNITS and self.grp_val < 10 or
              self.last_word in STENS and self.grp_val < 20):
            expected = word in CENT
        elif self.last_word in MTENS:
            expected = word in UNITS or word in STENS and self.last_word in ("soixante", "quatre-vingt")
        elif self.last_word in CENT:
            expected = word not in CENT

        if update:
            self.last_word = word
        return expected

    def is_coef_appliable(self, coef):
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
            return self.grp_val > 0 or coef == 1000  # "mille" without unit before is additive
        # TODO: There is one exception to the above rule: "de milliard"
        # ex. : "mille milliards de milliards"
        return False

    def push(self, word, look_ahead=None):
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

        if word == 'et' and look_ahead in ET_NUMS:
            return True

        word = word.replace('vingts', 'vingt')
        if word not in NUMBERS:
            return False

        if word in MULTIPLIERS:
            coef = MULTIPLIERS[word]
            if not self.is_coef_appliable(coef):
                return False
            # a multiplier can not be applied to a value bigger than itself,
            # so it must be applied to the current group
            if coef < self.n000_val:
                self.n000_val = self.n000_val + coef * (self.grp_val or 1)  # or 1 for "mille"
            else:
                self.n000_val = (self.value or 1) * coef

            self.grp_val = 0
            self.last_word = None
        elif (self.relaxed and word == 'quatre' and look_ahead and
              look_ahead.startswith('vingt') and self.group_expects('quatre-vingt', update=False)):
            self.on_hold = True
            self.grp_val += NUMBERS['quatre-vingt']
        elif self.on_hold and word.startswith('vingt'):
            self.on_hold = False
        elif self.group_expects(word):
            if word in CENT:
                self.grp_val = 100 * self.grp_val if self.grp_val else 100
            else:
                self.grp_val += NUMBERS[word]
        else:
            self.on_hold = False
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

    def __init__(self, relaxed=False):
        """Initialize the parser.

        If ``relaxed`` is True, we treat the sequence "quatre vingt" as
        a single "quatre-vingt".
        """
        self._value = []
        self.int_builder = WordStreamValueParser(relaxed=relaxed)
        self.frac_builder = WordStreamValueParser(relaxed=relaxed)
        self.in_frac = False
        self.closed = False  # For deferred stop
        self.open = False  # For efficiency

    @property
    def value(self):
        return ''.join(self._value)

    def close(self):
        """Signal end of input if input stream ends while still in a number.

        It's safe to call it multiple times.
        """
        if not self.closed:
            if self.in_frac and self.frac_builder.value:
                self._value.append(str(self.frac_builder.value))
            elif not self.in_frac and self.int_builder.value:
                self._value.append(str(self.int_builder.value))
            self.closed = True

    def at_start_of_seq(self):
        """Return true if we are waiting for the start of the integer
        part or the start of the fraction part."""
        return (self.in_frac and self.frac_builder.value == 0
                or not self.in_frac and self.int_builder.value == 0)

    def at_start(self):
        """Return True if nothing valid parsed yet."""
        return not self.open

    def is_article(self, word, following):
        return (not self.open and (word == 'un' or word == 'une') and
                not_numeric_word(following))

    def _push(self, word, look_ahead):
        builder = self.frac_builder if self.in_frac else self.int_builder
        return builder.push(word, look_ahead)

    def push(self, word, look_ahead=None):
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

        if word in SIGN and look_ahead in NUMBERS and self.at_start():
            self._value.append(SIGN[word])
        elif word.startswith('zéro') and self.at_start_of_seq():
            self._value.append('0')
        elif word.endswith('ième') and self._push(ord2card(word), look_ahead):
            self._value.append(str(self.frac_builder.value if self.in_frac else self.int_builder.value))
            self._value.append('ème')
            self.closed = True
        elif word == 'virgule' and (look_ahead in NUMBERS or look_ahead == 'zéro') and not self.in_frac:
            self._value.append(str(self.int_builder.value))
            self._value.append(',')
            self.in_frac = True
        elif not self._push(word, look_ahead):
            if self.open:
                self.close()
            return False

        self.open = True
        return True
