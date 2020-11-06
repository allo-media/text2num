# MIT License

# Copyright (c) 2018-2019 Groupe Allo-Media

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

from typing import Dict, Optional, Set, Tuple

from .base import Language

#
# CONSTANTS
# Built once on import.
#

# Those words multiplies lesser numbers (see Rules)
# Exception: "(de) milliards" that can multiply bigger numbers ("milliards de milliards")
MULTIPLIERS = {
    "mil":      1000,
    "milhar":   1000,
    "milhares": 1000,
    "milhão":   1000000,
    "milhões":  1000000,
}


# Units are terminals (see Rules)
UNITS: Dict[str, int] = {
    word: value
    for value, word in enumerate(
        "um dois três quatro cinco seis sete oito nove".split(), 1
    )
}
# Unit variants
UNITS["uma"] = 1
UNITS["duas"] = 2

# Single tens are terminals (see Rules)
# exact find
STENS: Dict[str, int] = {
    word: value
    for value, word in enumerate(
        "dez onze doze treze quatorze quinze dezasseis dezassete dezoito dezanove"
        .split(),
        10,
    )
}

# Ten multiples
# Ten multiples may be followed by a unit only;
# the number is the multiplier of the first token
MTENS: Dict[str, int] = {
    word: value * 10
    for value, word in enumerate(
        "vinte trinta quarenta cinquenta sessenta setenta oitenta noventa".split(), 2
    )
}

# Ten multiples that can be combined with STENS
MTENS_WSTENS: Set[str] = set()

HUNDRED = {
    "cem": 100,
    "centena": 100,
    "cento": 100,
    "centenas": 100,
    "duzentos": 200,
    "duzentas": 200,
    "trezentos": 300,
    "trezentas": 300,
    "quatrocentos": 400,
    "quatrocentas": 400,
    "quinhentos": 500,
    "quinhentas": 500,
    "seiscentos": 600,
    "seiscentas": 600,
    "setecentos": 700,
    "setecentas": 700,
    "oitocentos": 800,
    "oitocentas": 800,
    "novecentos": 900,
    "novecentas": 900,
}

COMPOSITES: Dict[str, int] = {}

# All number words

NUMBERS = MULTIPLIERS.copy()
NUMBERS.update(UNITS)
NUMBERS.update(STENS)
NUMBERS.update(MTENS)
NUMBERS.update(HUNDRED)
NUMBERS.update(COMPOSITES)


class Portuguese(Language):

    MULTIPLIERS = MULTIPLIERS
    UNITS = UNITS
    STENS = STENS
    MTENS = MTENS
    MTENS_WSTENS = MTENS_WSTENS
    HUNDRED = HUNDRED
    NUMBERS = NUMBERS

    SIGN = {"mais": "+", "menos": "-"}
    ZERO = {"zero"}
    DECIMAL_SEP = "vírgula"
    DECIMAL_SYM = ","

    AND_NUMS = {
        "um",
       "uma",
       "duas",
        "dois",
        "três",
        "quatro",
        "cinco",
        "seis",
        "sete",
        "oito",
        "nove",
    }
    AND = "e"
    NEVER_IF_ALONE = {"um", "uma"}

    # Relaxed composed numbers (two-words only)
    # start => (next, target)
    RELAXED: Dict[str, Tuple[str, str]] = {}

    # TODO
    def ord2card(self, word: str) -> Optional[str]:
        """Convert ordinal number to cardinal.

        Return None if word is not an ordinal or is better left in letters
        as is the case for fist and second.
        """
        return None

    def num_ord(self, digits: str, original_word: str) -> str:
        """Add suffix to number in digits to make an ordinal"""
        return f"{digits}º" if original_word.endswith("o") else f"{digits}ª"

    def normalize(self, word: str) -> str:
        return word
