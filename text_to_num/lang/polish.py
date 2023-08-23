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
# Special case: "hundred" is processed apart.
MULTIPLIERS = {
    "tysiąc": 1_000
    ,"tysięcy": 1_000
    ,"million": 1_000_000
    ,"millionów": 1_000_000
    ,"billion": 1_000_000_000
    ,"billionów": 1_000_000_000
    ,"trillion": 1_000_000_000_000
    ,"trillionów": 1_000_000_000_000
}


# Units are terminals (see Rules)
# Special case: "zero/O" is processed apart.
UNITS: Dict[str, int] = {
    word: value
    for value, word in enumerate(
        "jeden dwa trzy cztery pięć sześć siedem osiem dziewięć".split(), 1
    )
}

# Single tens are terminals (see Rules)
STENS: Dict[str, int] = {
    word: value
    for value, word in enumerate(
        "dziesięć jedenaście dwanaście trzynaście czternaście piętnaście szesnaście siedemnaście osiemnaście dziewiętnaście".split(),
        10,
    )
}


# Ten multiples
# Ten multiples may be followed by a unit only;
MTENS: Dict[str, int] = {
    word: value * 10
    for value, word in enumerate(
        "dwadzieścia trzydzieści czterdzieści pięćdziesiąt sześćdziesiąt siedemdziesiąt osiemdziesiąt dziewięćdziesiąt".split(), 2
    )
}

# Ten multiples that can be combined with STENS
MTENS_WSTENS: Set[str] = set()


# "hundred" has a special status (see Rules)
HUNDRED = {
    "sto": 100
    ,"dwieście": 200
    ,"trzysta": 300
    ,"czterysta": 400
    ,"pięćset": 500
    ,"sześćset": 600
    ,"siedemset": 700
    ,"osiemset": 800
    ,"dziewięćset": 900
}

HUNDRED_ORDINALS = {
    "stu": 100
    ,"setki": 100
    ,"dwustu": 200
    ,"trzystu": 300
    ,"czterystu": 400
    ,"pięciuset": 500
    ,"sześciuset": 600
    ,"siedmiuset": 700
    ,"ośmiuset": 800
    ,"dziewięciuset": 900
}
HUNDRED.update(HUNDRED_ORDINALS)


# Composites are tens already composed with terminals in one word.
# Composites are terminals.

COMPOSITES: Dict[str, int] = {}

# All number words

NUMBERS = MULTIPLIERS.copy()
NUMBERS.update(UNITS)
NUMBERS.update(STENS)
NUMBERS.update(MTENS)
NUMBERS.update(HUNDRED)
NUMBERS.update(COMPOSITES)


class Polish(Language):

    MULTIPLIERS = MULTIPLIERS
    UNITS = UNITS
    STENS = STENS
    MTENS = MTENS
    MTENS_WSTENS = MTENS_WSTENS
    HUNDRED = HUNDRED
    NUMBERS = NUMBERS

    SIGN = {"plus": "+", "minus": "-"}
    ZERO = {"zero"}
    DECIMAL_SEP = "przecinek"
    DECIMAL_SYM = ","

    AND_NUMS: Set[str] = set()
    AND = "oraz"
    NEVER_IF_ALONE = {"jeden"}

    # Relaxed composed numbers (two-words only)
    # start => (next, target)
    RELAXED: Dict[str, Tuple[str, str]] = {}

    # Ordinal numbers
    POL_ORDINALS = {
        "jednej": "jeden"
        ,"jedna": "jeden"
        ,"jednego": "jeden"
        ,"dwie": "dwa"
        ,"dwóch": "dwa"
        ,"trzech": "trzy"
        ,"czterech": "cztery"
        ,"pięciu": "pięć"
        ,"sześciu": "sześć"
        ,"siedmiu": "siedem"
        ,"ośmiu": "osiem"
        ,"dziewięciu": "dziewięć"
        ,"dziesięciu": "dziesięć"
        ,"dwunastu": "dwanaście"
        ,"dwudziestu": "dwadzieścia"
    }

    STENS_ORDINALS_SURFIXES = ('nastu')
    MTENS_ORDINALS_SURFIXES = ('stu','ciu')

    def normalize(self, word: str) -> str:
        if word in self.NUMBERS:
            return word

        ord_ = self.POL_ORDINALS.get(word, None)

        if not ord_ and isinstance(word, str):
            try:
                if word.endswith(self.STENS_ORDINALS_SURFIXES):
                    prefix = word[:5]
                    for x in self.STENS:
                        if x.startswith(prefix):
                            ord_ = x
                            break
                elif word.endswith(self.MTENS_ORDINALS_SURFIXES):
                    prefix = word[:4]
                    for x in self.MTENS:
                        if x.startswith(prefix):
                            ord_ = x
                            break
            except Exception:
                pass

        if not ord_ and isinstance(word, str):
            try:
                for x in self.MULTIPLIERS:
                    if word.startswith(x):
                        ord_ = x
                        break
            except Exception:
                pass

        return ord_ if ord_ else word