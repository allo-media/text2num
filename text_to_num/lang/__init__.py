"""
Language support.
"""

from .base import Language  # noqa: F401
from .french import French


LANG = {"fr": French()}
