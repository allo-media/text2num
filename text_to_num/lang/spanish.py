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

import re
from typing import Dict, Optional, Set, Tuple, List

from .base import Language

#
# CONSTANTS
# Built once on import.
#

# Those words multiplies lesser numbers (see Rules)
# Exception: "(de) milliards" that can multiply bigger numbers ("milliards de milliards")
MULTIPLIERS = {
    "mil": 1000,
    "miles": 1000,
    "millon": 1000000,
    "millón": 1000000,
    "millones": 1000000,
    "millardo": 10**9,  # not common, but no harm having it
    "billón": 10**12,
    "billon": 10**12,
    "billones": 10**12,
}


# Units are terminals (see Rules)
UNITS: Dict[str, int] = {
    word: value
    for value, word in enumerate(
        "uno dos tres cuatro cinco seis siete ocho nueve".split(), 1
    )
}
UNITS_std = UNITS.copy()

# Unit variants
UNITS["un"] = 1
UNITS["una"] = 1

# Single tens are terminals (see Rules)
STENS: Dict[str, int] = {
    word: value
    for value, word in enumerate(
        "diez once doce trece catorce quince dieciseis diecisiete dieciocho diecinueve"
        " veinte veintiuno veintidos veintitres veinticuatro veinticinco veintiseis"
        " veintisiete veintiocho veintinueve".split(),
        10,
    )
}

STENS["dieciséis"] = 16
STENS["veintiuna"] = 21  # feminine
STENS["veintiún"] = 21  # masculine
STENS["veintiun"] = 21  # masculine
STENS["veintidós"] = 22
STENS["veintitrés"] = 23
STENS["veintiséis"] = 26


# Ten multiples
# Ten multiples may be followed by a unit only;
MTENS: Dict[str, int] = {
    word: value * 10
    for value, word in enumerate(
        "treinta cuarenta cincuenta sesenta setenta ochenta noventa".split(), 3
    )
}

# Ten multiples that can be combined with STENS
MTENS_WSTENS: Set[str] = set()

# "cent" has a special status (see Rules)
HUNDRED = {
    "cien": 100,
    "ciento": 100,
    "cienta": 100,
    "doscientos": 200,
    "trescientos": 300,
    "cuatrocientos": 400,
    "quinientos": 500,
    "seiscientos": 600,
    "setecientos": 700,
    "ochocientos": 800,
    "novecientos": 900,
    #
    "doscientas": 200,
    "trescientas": 300,
    "cuatrocientas": 400,
    "quinientas": 500,
    "seiscientas": 600,
    "setecientas": 700,
    "ochocientas": 800,
    "novecientas": 900,
}

COMPOSITES: Dict[str, int] = {}

# All number words

NUMBERS = MULTIPLIERS.copy()
NUMBERS.update(UNITS)
NUMBERS.update(STENS)
NUMBERS.update(MTENS)
NUMBERS.update(HUNDRED)
NUMBERS.update(COMPOSITES)


class Spanish(Language):
    MULTIPLIERS = MULTIPLIERS
    UNITS = UNITS
    STENS = STENS
    MTENS = MTENS
    MTENS_WSTENS = MTENS_WSTENS
    HUNDRED = HUNDRED
    NUMBERS = NUMBERS

    SIGN = {"mas": "+", "menos": "-"}
    ZERO = {"cero"}
    DECIMAL_SEP = "coma,punto"
    DECIMAL_SYM = "."

    AND_NUMS = {
        "un",
        "uno",
        "una",
        "dos",
        "tres",
        "cuatro",
        "cinco",
        "seis",
        "siete",
        "ocho",
        "nueve",
    }
    AND = "y"
    NEVER_IF_ALONE = {"un", "uno", "una"}

    # Relaxed composed numbers (two-words only)
    # start => (next, target)
    RELAXED: Dict[str, Tuple[str, str]] = {}

    ES_ORDINALS = {
        # 1 - 9
        "primero": "uno",
        "segundo": "dos",
        "tercero": "tres",
        "cuarto": "cuatro",
        "quinto": "cinco",
        "sexto": "seis",
        "séptimo": "siete",
        "octavo": "ocho",
        "noveno": "nueve",
        # 10 - 19
        "décimo": "diez",
        "undécimo": "once",
        "decimoprimero": "once",
        "duodécimo": "doce",
        "decimosegundo": "doce",
        "décimoprimero": "once",  # tmp fix to handle num2words bug
        "décimosegundo": "doce",  # tmp fix to handle num2words bug
        "decimotercero": "trece",
        "decimocuarto": "catorce",
        "decimoquinto": "quince",
        "decimosexto": "dieciseis",
        "decimoséptimo": "diecisiete",
        "decimooctavo": "dieciocho",
        "decimonoveno": "diecinueve",
        # 20 - 90
        "vigésimo": "veinte",
        "trigésimo": "treinta",
        "cuadragésimo": "cuarenta",
        "quadragésimo": "cuarenta",  # tmp fix to handle num2words bug
        "quincuagésimo": "cincuenta",
        "sexagésimo": "sesenta",
        "septuagésimo": "setenta",
        "octogésimo": "ochenta",
        "nonagésimo": "noventa",
        # 100 - 900
        "centésimo": "ciento",
        "ducentésimo": "doscientos",
        "tricentésimo": "trescientos",
        "cuadringentésimo": "cuatrocientos",
        "quingentésimo": "quinientos",
        "sexcentésimo": "seiscientos",
        "septingentésimo": "setecientos",
        "octingentésimo": "ochocientos",
        "noningentésimo": "novecientos",
        # 1000, 10**6, 10**12
        "milésimo": "mil",
        "millonésimo": "millones",
        "billonésimo": "billones",
    }
    # for u,v in UNITS_std.items():

    ES_ORD_FEMININE = {o[:-1]+"a":c for o, c in ES_ORDINALS.items()}
    ES_ORDINALS.update(ES_ORD_FEMININE)
    ES_ORD_PLURAL = {o+"s":c for o, c in ES_ORDINALS.items()}
    ES_ORDINALS.update(ES_ORD_PLURAL)
    ES_ORD_NOACCENT = {o.replace("é", "e").replace("ó", "o"):c for o, c in ES_ORDINALS.items()}
    ES_ORDINALS.update(ES_ORD_NOACCENT)

    ES_ORDINALS["primer"] = "un"
    ES_ORDINALS["tercer"] = "tres"
    ES_ORDINALS["decimoprimer"] = "once"
    ES_ORDINALS["decimotercer"] = "trece"

    # TODO
    def ord2card(self, word: str) -> Optional[str]:
        """Convert ordinal number to cardinal.

        Return None if word is not an ordinal or is better left in letters
        as is the case for fist and second.
        """
        ord_ = self.ES_ORDINALS.get(word, None)
        return ord_

    def num_ord(self, digits: str, original_word: str) -> str:
        """Add suffix to number in digits to make an ordinal. Currently dropping plural `s`, OrdinalsMerger also not expects plurals."""
        masculine = original_word.endswith("o") or original_word.endswith("os") or original_word.endswith("primer")  or original_word.endswith("tercer")
        return f"{digits}º" if masculine  else f"{digits}ª"

    def normalize(self, word: str) -> str:
        return word

SEGMENT_BREAK = re.compile(r"\s*[\.,;\(\)…\[\]:!\?]+\s*")

SUB_REGEXES = [
    (re.compile(r"1\s"), "uno "),
    (re.compile(r"2\s"), "dos"),
    (re.compile(r"\b1[\º\°]\b"), "primero"),
    (re.compile(r"\b2[\º\°]\b"), "segundo"),
    (re.compile(r"\b3[\º\°]\b"), "tercero"),
    (re.compile(r"\b1\ª\b"), "primera"),
    (re.compile(r"\b2\ª\b"), "segunda"),
    (re.compile(r"\b3\ª\b"), "tercera"),
]

class OrdinalsMergerES:
    def merge_compound_ordinals(self, text: str) -> str:
        """join compound ordinal cases created by a text2num 1st pass

        Example:
                20° 7° -> 27°

        Greedy pusher: push along the token stream,
                       create a new ordinal sequence if an ordinal is found
                       stop sequence when no more ordinals are found
                       sum ordinal sequence

        """

        segments = re.split(SEGMENT_BREAK, text)
        punct = re.findall(SEGMENT_BREAK, text)
        if len(punct) < len(segments):
            punct.append("")
        out_segments = []
        for segment, sep in zip(segments, punct):  # loop over segments
            tokens = [t for t in segment.split(" ") if len(t) > 0]

            pointer = 0
            tokens_ = []
            current_is_ordinal = False
            seq = []

            while pointer < len(tokens):
                token = tokens[pointer]
                if self.is_ordinal(token):  # found an ordinal, push into new seq
                    current_is_ordinal = True
                    seq.append(self.get_cardinal(token))
                    gender = self.get_gender(token)
                else:
                    if current_is_ordinal is False:  # add standard token
                        tokens_.append(token)
                    else:  # close seq
                        ordinal = sum(seq)
                        tokens_.append(str(ordinal) + gender)
                        tokens_.append(token)
                        seq = []
                        current_is_ordinal = False
                pointer += 1

            if current_is_ordinal is True:  # close seq for single token expressions
                ordinal = sum(seq)
                tokens_.append(str(ordinal) + gender)

            tokens_ = self.text2num_style(tokens_)
            segment = " ".join(tokens_) + sep
            out_segments.append(segment)

        text = "".join(out_segments)

        return text

    @staticmethod
    def is_ordinal(token: str) -> bool:
        out = False
        if len(token) > 1 and ("º" in token or "°" in token or "ª" in token):
            out = True
        # in case the ordinal is left as a word since it's smaller than the threshold:
        if token in [
            "primero", "primera", "primer", "primeros", "primeras", 
            "segundo", "segunda", "segundos", "segundas",
            "tercero", "tercera", "tercer", "terceros", "terceras",
        ]:
            out = True
        return out

    @staticmethod
    def get_cardinal(token: str) -> int:
        out = 0
        try:
            out = int(token[:-1])
        except ValueError:
            if token in ["primero", "primera", "primer", "primeros", "primeras"]:
                out = 1
            elif token in ["segundo", "segunda", "segundos", "segundas"]:
                out = 2
            elif token in ["tercero", "tercera", "tercer", "terceros", "terceras"]:
                out = 3
        return out

    @staticmethod
    def get_gender(token: str) -> str:
        gender = token[-1]
        if gender == "a":
            gender = "ª"
        if gender == "o":
            gender = "º"
        return gender

    @staticmethod
    def text2num_style(tokens: List[str]) -> List[str]:
        """convert a list of tokens to text2num_style, i.e. : 1 -> un/one/uno/um"""

        for regex in SUB_REGEXES:
            tokens = [re.sub(regex[0], regex[1], token) for token in tokens]

        return tokens
