"""
Test the ``text_to_num`` library.
"""
from unittest import TestCase
from text_to_num import alpha2digit, text2num


class TestTextToNum(TestCase):
    def test_text2num(self):
        test1 = "cinquante trois mille millions deux cent quarante trois mille sept cent vingt quatre"
        self.assertEqual(text2num(test1), 53_000_243_724)

        test2 = "cinquante et un million cinq cent soixante dix-huit mille trois cent deux"
        self.assertEqual(text2num(test2), 51_578_302)

        test3 = "quatre-vingt cinq"
        self.assertEqual(text2num(test3), 85)

        test4 = "quatre-vingt un"
        self.assertEqual(text2num(test4), 81)

    def test_alpha2digit_integers(self):
        source = "Vingt-cinq vaches, douze poulets et cent vingt-cinq kg de pommes de terre."
        expected = "25 vaches, 12 poulets et 125 kg de pommes de terre."
        self.assertEqual(alpha2digit(source), expected)

        source = "Mille deux cent soixante-six clous."
        expected = "1266 clous."
        self.assertEqual(alpha2digit(source), expected)

        source = "Nonante-cinq = quatre-vingt-quinze"
        expected = "95 = 95"
        self.assertEqual(alpha2digit(source), expected)

        source = "Nonante cinq = quatre-vingt quinze"
        self.assertEqual(alpha2digit(source), expected)

        source = "un deux trois quatre vingt quinze"
        expected = "1 2 3 4 20 15"
        self.assertEqual(alpha2digit(source), expected)

        source = "Vingt et un, trente et un."
        expected = "21, 31."
        self.assertEqual(alpha2digit(source), expected)

    def test_relaxed(self):
        source = "un deux trois quatre vingt quinze."
        expected = "1 2 3 95."
        self.assertEqual(alpha2digit(source, relaxed=True), expected)

        source = "Quatre, vingt, quinze."
        expected = "4, 20, 15."
        self.assertEqual(alpha2digit(source, relaxed=True), expected)

        source = "trente-quatre = trente quatre"
        expected = "34 = 34"
        self.assertEqual(alpha2digit(source, relaxed=True), expected)

    def test_alpha2digit_formal(self):
        source = "plus trente-trois neuf soixante zéro six douze vingt et un"
        expected = "+33 9 60 06 12 21"
        self.assertEqual(alpha2digit(source), expected)

        source = "zéro neuf soixante zéro six douze vingt et un"
        expected = "09 60 06 12 21"
        self.assertEqual(alpha2digit(source), expected)

    def test_alpha2digit_zero(self):
        source = "treize mille zéro quatre-vingt-dix"
        expected = "13000 090"
        self.assertEqual(alpha2digit(source), expected)

    def test_alpha2digit_ordinals(self):
        source = "Cinquième troisième vingt et unième centième mille deux cent trentième."
        expected = "5ème 3ème 21ème 100ème 1230ème."
        self.assertEqual(alpha2digit(source), expected)

    def test_alpha2digit_decimals(self):
        source = "Douze virgule quatre-vingt dix-neuf, cent vingt virgule zéro cinq, un virgule deux cent trente six."
        expected = "12,99, 120,05, 1,236."
        self.assertEqual(alpha2digit(source), expected)

    def test_article(self):
        source = ("Ne pas confondre un article ou un nom avec un chiffre et inversement : "
                  "les uns et les autres ; une suite de chiffres : un, deux, trois !")
        expected = ("Ne pas confondre un article ou un nom avec un chiffre et inversement : "
                    "les uns et les autres ; une suite de chiffres : 1, 2, 3 !")
        self.assertEqual(alpha2digit(source), expected)
