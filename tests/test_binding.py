from unittest import TestCase

import text_to_num


class MyToken(text_to_num.Token):
    def __init__(self, text):
        self.content = text

    def text(self):
        return self.content


def tokenize(text):
    """Poor man's tokenizer."""
    return [MyToken(piece) for piece in text.split()]


class TestBindingBase(TestCase):

    def test_text2num(self):
        self.assertEqual(text_to_num.text2num("deux cent vingt-cinq", "fr"), 225)
        self.assertRaises(ValueError, text_to_num.text2num, "fr", "trente et onze")

    def test_alpha2digit(self):
        text = "Vingt-cinq vaches, douze poulets et cent vingt-cinq kg de pommes de terre."
        self.assertEqual(
            text_to_num.alpha2digit(text, "fr"),
            "25 vaches, 12 poulets et 125 kg de pommes de terre."
        )


class TestBindingExtensions(TestCase):

    def test_find_numbers(self):
        text = "Vingt-cinq vaches, douze poulets et cent vingt-cinq kg de pommes de terre."
        occurences = text_to_num.find_numbers(tokenize(text), "fr")

        self.assertEqual(len(occurences), 3)
        self.assertEqual(occurences[0].value, 25.0)
        self.assertEqual(occurences[0].start, 0)
        self.assertEqual(occurences[0].end, 1)
        self.assertEqual(occurences[1].value, 12.0)
        self.assertEqual(occurences[1].start, 2)
        self.assertEqual(occurences[1].end, 3)
        self.assertEqual(occurences[2].value, 125.0)
        self.assertEqual(occurences[2].start, 5)
        self.assertEqual(occurences[2].end, 7)
        self.assertEqual(occurences[2].text, "125")
