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


class TestTextToNumCA(TestCase):
    def test_text2num(self):
        test1 = "cinquanta-tres mil milions dos-cents quaranta-tres mil set-cents vint-i-quatre"
        self.assertEqual(text2num(test1, "ca"), 53_000_243_724)

        test2 = (
            "cinquanta-un milions cinc-centes setanta-vuit mil tres-centes dues"
        )
        self.assertEqual(text2num(test2, "ca"), 51_578_302)

        test3 = "vuitanta-cinc"
        self.assertEqual(text2num(test3, "ca"), 85)

        test4 = "huitanta-u"
        self.assertEqual(text2num(test4, "ca"), 81)

        self.assertEqual(text2num("quinze", "ca"), 15)
        self.assertEqual(text2num("setanta cinc mil", "ca"), 75000)

    def test_text2num_variants(self):
        self.assertEqual(text2num("noranta-vuit", "ca"), 98)
        self.assertEqual(text2num("noranta-huit", "ca"), 98)
        self.assertEqual(text2num("setanta-vuit", "ca"), 78)
        self.assertEqual(text2num("vuitanta-vuit", "ca"), 88)
        self.assertEqual(text2num("huitanta-huit", "ca"), 88)
        self.assertEqual(text2num("vuitanta-una", "ca"), 81)
        self.assertEqual(text2num("vuitanta", "ca"), 80)
        self.assertEqual(text2num("mil nou-cents vint", "ca"), 1920)

#    No equivalent in Catalan
#    def test_text2num_centuries(self):
#        self.assertEqual(text2num("dix-neuf cent soixante-treize", "fr"), 1973)

    def test_text2num_exc(self):
        self.assertRaises(ValueError, text2num, "mil mil dos-cents", "ca")
#        self.assertRaises(ValueError, text2num, "soixante quinze cent", "ca") #No equivalent in Catalan

    def test_text2num_zeroes(self):
        self.assertEqual(text2num("zero", "ca"), 0)
        self.assertEqual(text2num("zero vuit", "ca"), 8)
        self.assertEqual(text2num("zero zero cent vint-i-cinc", "ca"), 125)
        self.assertRaises(ValueError, text2num, "cinc zero", "ca")
        self.assertRaises(ValueError, text2num, "cinquanta zero tres", "ca")
        self.assertRaises(ValueError, text2num, "cinquanta tres zero", "ca")

    def test_alpha2digit_integers(self):
        source = (
            "Vint-i-cinc vaques, dotze pollastres i cent vint-i-cinc kg de creïlles."
        )
        expected = "25 vaques, 12 pollastres i 125 kg de creïlles."
        self.assertEqual(alpha2digit(source, "ca"), expected)

        source = "Mil dos-cents seixanta-sis claus."
        expected = "1266 claus."
        self.assertEqual(alpha2digit(source, "ca"), expected)

#        source = "Mille deux cents soixante-six clous."
#        self.assertEqual(alpha2digit(source, "fr"), expected)

        source = "Vuitanta-cinc = huitanta-cinc"
        expected = "85 = 85"
        self.assertEqual(alpha2digit(source, "ca"), expected)

#        source = "Nonante cinq = quatre-vingt quinze"
#        self.assertEqual(alpha2digit(source, "fr"), expected)

        source = "un dos tres quatre vint quinze"
        expected = "1 2 3 4 20 15"
        self.assertEqual(alpha2digit(source, "ca"), expected)

        source = "Vint-i-u, trenta-u."
        expected = "21, 31."
        self.assertEqual(alpha2digit(source, "ca"), expected)

#   No equivalent in Catalan
    # def test_relaxed(self):
    #     source = "un deux trois quatre vingt quinze."
    #     expected = "1 2 3 95."
    #     self.assertEqual(alpha2digit(source, "fr", relaxed=True), expected)

    #     source = "Quatre, vingt, quinze, quatre-vingts."
    #     expected = "4, 20, 15, 80."
    #     self.assertEqual(alpha2digit(source, "fr", relaxed=True), expected)

    #     source = "trente-quatre = trente quatre"
    #     expected = "34 = 34"
    #     self.assertEqual(alpha2digit(source, "fr"), expected)

    def test_alpha2digit_formal(self):
        source = "més trenta-tres nou seixanta zero sis dotze vint-i-u"
        expected = "+33 9 60 06 12 21"
        self.assertEqual(alpha2digit(source, "ca"), expected)

        source = "zero nou seixanta zero sis dotze vint-i-u"
        expected = "09 60 06 12 21"
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_trente_et_onze(self):
        source = "cinquanta seixanta trenta i onze"
        expected = "50 60 30 i 11"
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_alpha2digit_zero(self):
        source = "tretze mil zero noranta"
        expected = "13000 090"
        self.assertEqual(alpha2digit(source, "ca"), expected)
        source = "tretze mil zero huitanta"
        expected = "13000 080"
        self.assertEqual(alpha2digit(source, "ca"), expected)

        # source = "Votre service est zéro !"
        # self.assertEqual(alpha2digit(source, "fr"), source)

        self.assertEqual(alpha2digit("zero", "ca"), "0")

    def test_alpha2digit_ordinals(self):
        source = (
            "Cinquè primer segon tercer vint-i-unè centè mil dos-cents trentè."
        )
        expected = "5è primer segon tercer 21è 100è 1230è."
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_alpha2digit_all_ordinals(self):
        source = (
            "Cinquè primer segon tercer vint-i-unè centè mil dos-cents trentè."
        )
        expected = "5è 1r 2n 3r 21è 100è 1230è."
        self.assertEqual(alpha2digit(source, "ca", ordinal_threshold=0), expected)

    def test_alpha2digit_decimals(self):
        source = (
            "Dotze coma noranta-nou, cent vint coma zero cinc,"
            " u coma dos-cents trenta-sis."
        )
        expected = "12,99, 120,05, 1,236."
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_alpha2digit_signed(self):
        source = (
            "Fa més vint graus a l'interior i menys quinze a l'exterior."
        )
        expected = "Fa +20 graus a l'interior i -15 a l'exterior."
        self.assertEqual(alpha2digit(source, "ca"), expected)

        source = "Menys tres al jardí, i ja no més dos."
        expected = "Menys 3 al jardí, i ja no més 2."

        self.assertEqual(alpha2digit(source, "ca", signed=False), expected)
        self.assertNotEqual(alpha2digit(source, "ca", signed=True), expected)

    def test_article(self):
        source = (
            "No confondre un article o un nom amb una xifra i viceversa: "
            "els uns i els altres; una seqüència de xifres: un, dos, tres!"
        )
        expected = (
            "No confondre un article o un nom amb una xifra i viceversa: "
            "els uns i els altres; una seqüència de xifres: 1, 2, 3!"
        )
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_un_pronoun(self):
        source = "Només en vull un. Anuncie: l'un"
        self.assertEqual(alpha2digit(source, "ca"), source)
