"""
Base type for language objects.
"""

from typing import Dict, Optional, Set, Tuple


class Language:
    """Base class for language object."""

    MULTIPLIERS: Dict[str, int]
    UNITS: Dict[str, int]
    STENS: Dict[str, int]
    MTENS: Dict[str, int]
    MTENS_WSTENS: Set[str]
    CENT: Dict[str, int]
    NUMBERS: Dict[str, int]

    SIGN: Dict[str, str]
    ZERO: str
    DECIMAL_SEP: str
    DECIMAL_SYM: str

    AND_NUMS: Set[str]
    AND: str
    UNIT_ARTICLES: Set[str]

    # Relaxed composed numbers (two-words only)
    # start => (next, target)
    RELAXED: Dict[str, Tuple[str, str]]

    def ord2card(self, word: str) -> Optional[str]:
        """Convert ordinal number to cardinal.

        Return None if word is not an ordinal or is better left in letters
        as is the case for fist and second.
        """
        return NotImplemented

    def num_ord(self, digits: str, original_word: str) -> str:
        """Add suffix to number in digits to make an ordinal"""
        return NotImplemented

    def normalize(self, word: str) -> str:
        return NotImplemented

    def not_numeric_word(self, word: Optional[str]) -> bool:
        return (
            word is not None and word != self.DECIMAL_SEP and word not in self.NUMBERS
        )
