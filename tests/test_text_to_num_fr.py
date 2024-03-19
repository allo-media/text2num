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


"""
Test the ``text_to_num`` library.
"""
from unittest import TestCase
from text_to_num import alpha2digit, text2num


class TestTextToNumFR(TestCase):
    def test_text2num(self):
        test1 = "cinquante trois mille millions deux cent quarante trois mille sept cent vingt quatre"
        self.assertEqual(text2num(test1, "fr"), 53_000_243_724)

        test2 = (
            "cinquante et un million cinq cent soixante dix-huit mille trois cent deux"
        )
        self.assertEqual(text2num(test2, "fr"), 51_578_302)

        test3 = "quatre-vingt cinq"
        self.assertEqual(text2num(test3, "fr"), 85)

        test4 = "quatre-vingt un"
        self.assertEqual(text2num(test4, "fr"), 81)

        self.assertEqual(text2num("quinze", "fr"), 15)
        self.assertEqual(text2num("soixante quinze mille", "fr"), 75000)
        self.assertEqual(text2num("un milliard vingt-cinq millions", "fr"), 1_025_000_000)

    def test_text2num_variants(self):
        self.assertEqual(text2num("quatre-vingt dix-huit", "fr"), 98)
        self.assertEqual(text2num("nonante-huit", "fr"), 98)
        self.assertEqual(text2num("soixante-dix-huit", "fr"), 78)
        self.assertEqual(text2num("septante-huit", "fr"), 78)
        self.assertEqual(text2num("quatre-vingt-huit", "fr"), 88)
        self.assertEqual(text2num("octante-huit", "fr"), 88)
        self.assertEqual(text2num("huitante-huit", "fr"), 88)
        self.assertEqual(text2num("huitante-et-un", "fr"), 81)
        self.assertEqual(text2num("quatre-vingts", "fr"), 80)
        self.assertEqual(text2num("mil neuf cent vingt", "fr"), 1920)

    def test_text2num_centuries(self):
        self.assertEqual(text2num("dix-neuf cent soixante-treize", "fr"), 1973)

    def test_text2num_exc(self):
        self.assertRaises(ValueError, text2num, "mille mille deux cent", "fr")
        self.assertRaises(ValueError, text2num, "soixante quinze cent", "fr")

    def test_text2num_zeroes(self):
        self.assertEqual(text2num("zéro", "fr"), 0)
        self.assertEqual(text2num("zéro huit", "fr"), 8)
        self.assertEqual(text2num("zéro zéro cent vingt-cinq", "fr"), 125)
        self.assertRaises(ValueError, text2num, "cinq zéro", "fr")
        self.assertRaises(ValueError, text2num, "cinquante zéro trois", "fr")
        self.assertRaises(ValueError, text2num, "cinquante trois zéro", "fr")

    def test_alpha2digit_integers(self):
        source = (
            "Vingt-cinq vaches, douze poulets et cent vingt-cinq kg de pommes de terre."
        )
        expected = "25 vaches, 12 poulets et 125 kg de pommes de terre."
        self.assertEqual(alpha2digit(source, "fr"), expected)

        source = "Mille deux cent soixante-six clous."
        expected = "1266 clous."
        self.assertEqual(alpha2digit(source, "fr"), expected)

        source = "Mille deux cents soixante-six clous."
        self.assertEqual(alpha2digit(source, "fr"), expected)

        source = "Nonante-cinq = quatre-vingt-quinze"
        expected = "95 = 95"
        self.assertEqual(alpha2digit(source, "fr"), expected)

        source = "Nonante cinq = quatre-vingt quinze"
        self.assertEqual(alpha2digit(source, "fr"), expected)

        source = "un deux trois quatre vingt quinze"
        expected = "1 2 3 4 20 15"
        self.assertEqual(alpha2digit(source, "fr"), expected)

        source = "Vingt et un, trente et un."
        expected = "21, 31."
        self.assertEqual(alpha2digit(source, "fr"), expected)

    def test_relaxed(self):
        source = "un deux trois quatre vingt quinze."
        expected = "1 2 3 95."
        self.assertEqual(alpha2digit(source, "fr", relaxed=True), expected)

        source = "Quatre, vingt, quinze, quatre-vingts."
        expected = "4, 20, 15, 80."
        self.assertEqual(alpha2digit(source, "fr", relaxed=True), expected)

        source = "trente-quatre = trente quatre"
        expected = "34 = 34"
        self.assertEqual(alpha2digit(source, "fr"), expected)

    def test_alpha2digit_formal(self):
        source = "plus trente-trois neuf soixante zéro six douze vingt et un"
        expected = "+33 9 60 06 12 21"
        self.assertEqual(alpha2digit(source, "fr"), expected)

        source = "zéro neuf soixante zéro six douze vingt et un"
        expected = "09 60 06 12 21"
        self.assertEqual(alpha2digit(source, "fr"), expected)

    def test_trente_et_onze(self):
        source = "cinquante soixante trente et onze"
        expected = "50 60 30 11"
        self.assertEqual(alpha2digit(source, "fr"), expected)

    def test_alpha2digit_zero(self):
        source = "treize mille zéro quatre-vingt-dix"
        expected = "13000 090"
        self.assertEqual(alpha2digit(source, "fr"), expected)
        source = "treize mille zéro quatre-vingts"
        expected = "13000 080"
        self.assertEqual(alpha2digit(source, "fr"), expected)

        # source = "Votre service est zéro !"
        # self.assertEqual(alpha2digit(source, "fr"), source)

        self.assertEqual(alpha2digit("zéro", "fr"), "0")
        self.assertEqual(alpha2digit("a a un trois sept trois trois sept cinq quatre zéro c c", "fr"), "a a 1 3 7 3 3 7 5 4 0 c c")
        self.assertEqual(alpha2digit("sept un zéro", "fr"), "7 1 0")

    def test_alpha2digit_ordinals(self):
        source = (
            "Cinquième premier second troisième vingt et unième centième mille deux cent trentième."
        )
        expected = "5ème premier second troisième 21ème 100ème 1230ème."
        self.assertEqual(alpha2digit(source, "fr"), expected)
        self.assertEqual(alpha2digit("un millième", "fr"), "un 1000ème")
        self.assertEqual(alpha2digit("un millionième", "fr"), "un 1000000ème")

    def test_alpha2digit_all_ordinals(self):
        source = (
            "Cinquième premier second troisième vingt et unième centième mille deux cent trentième."
        )
        expected = "5ème 1er 2nd 3ème 21ème 100ème 1230ème."
        self.assertEqual(alpha2digit(source, "fr", ordinal_threshold=0), expected)

    def test_alpha2digit_decimals(self):
        source = (
            "Douze virgule quatre-vingt dix-neuf, cent vingt virgule zéro cinq,"
            " un virgule deux cent trente six."
        )
        expected = "12,99, 120,05, 1,236."
        self.assertEqual(alpha2digit(source, "fr"), expected)

        self.assertEqual(
            alpha2digit("la densité moyenne est de zéro virgule cinq.", "fr"),
            "la densité moyenne est de 0,5."
        )


    def test_alpha2digit_signed(self):
        source = (
            "Il fait plus vingt degrés à l'intérieur et moins quinze à l'extérieur."
        )
        expected = "Il fait +20 degrés à l'intérieur et -15 à l'extérieur."
        self.assertEqual(alpha2digit(source, "fr"), expected)

        source = "J'en ai vu au moins trois dans le jardin, et non plus deux."
        expected = "J'en ai vu au moins 3 dans le jardin, et non plus 2."

        self.assertEqual(alpha2digit(source, "fr", signed=False), expected)
        self.assertNotEqual(alpha2digit(source, "fr", signed=True), expected)

    def test_article(self):
        source = (
            "Ne pas confondre un article ou un nom avec un chiffre et inversement : "
            "les uns et les autres ; une suite de chiffres : un, deux, trois !"
        )
        expected = (
            "Ne pas confondre un article ou un nom avec un chiffre et inversement : "
            "les uns et les autres ; une suite de chiffres : 1, 2, 3 !"
        )
        self.assertEqual(alpha2digit(source, "fr"), expected)

    def test_un_pronoun(self):
        source = "Je n'en veux qu'un. J'annonce: le un"
        self.assertEqual(alpha2digit(source, "fr"), source)

    def test_alpha2digit_newline(self):
        self.assertEqual(alpha2digit("dix + deux\n= douze", "fr"), "10 + 2\n= 12")
