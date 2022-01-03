from typing import Dict

from text_to_num.lang import Portuguese


class BrazilianPortuguese(Portuguese):
    STENS: Dict[str, int] = {
        'dez': 10,
        'onze': 11,
        'doze': 12,
        'treze': 13,
        'catorze': 14,
        'quatorze': 14,
        'quinze': 15,
        'dezesseis': 16,
        'dezessete': 17,
        'dezoito': 18,
        'dezenove': 19
    }

    AND_NUMS = Portuguese.AND_NUMS.union({'catorze'})

    NUMBERS = {**Portuguese.NUMBERS, **STENS}
