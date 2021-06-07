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


class TestTextToNumPT(TestCase):
    def test_text2num(self):
        self.assertEqual(text2num("zero", "ptbr"), 0)
        self.assertEqual(text2num("um", "ptbr"), 1)
        self.assertEqual(text2num("oito", "ptbr"), 8)
        self.assertEqual(text2num("dez", "ptbr"), 10)
        self.assertEqual(text2num("onze", "ptbr"), 11)
        self.assertEqual(text2num("dezenove", "ptbr"), 19)
        self.assertEqual(text2num("vinte", "ptbr"), 20)
        self.assertEqual(text2num("vinte e um", "ptbr"), 21)
        self.assertEqual(text2num("trinta", "ptbr"), 30)
        self.assertEqual(text2num("trinta e um", "ptbr"), 31)
        self.assertEqual(text2num("trinta e dois", "ptbr"), 32)
        self.assertEqual(text2num("trinta e três", "ptbr"), 33)
        self.assertEqual(text2num("trinta e nove", "ptbr"), 39)
        self.assertEqual(text2num("noventa e nove", "ptbr"), 99)
        self.assertEqual(text2num("cem", "ptbr"), 100)
        self.assertEqual(text2num("cento e um", "ptbr"), 101)
        self.assertEqual(text2num("duzentos", "ptbr"), 200)
        self.assertEqual(text2num("duzentos e um", "ptbr"), 201)
        self.assertEqual(text2num("mil", "ptbr"), 1000)
        self.assertEqual(text2num("mil e um", "ptbr"), 1001)
        self.assertEqual(text2num("dois mil", "ptbr"), 2000)
        self.assertEqual(text2num("dois mil noventa e nove", "ptbr"), 2099)
        self.assertEqual(text2num("nove mil novecentos noventa e nove", "ptbr"), 9999)
        self.assertEqual(
            text2num("novecentos noventa e nove mil novecentos noventa e nove", "ptbr"),
            999999,
        )

        self.assertEqual(alpha2digit("um vírgula um", "ptbr"), "1,1")
        self.assertEqual(alpha2digit("um vírgula quatrocentos e um", "ptbr"), "1,401")

        # fail
        #        self.assertEqual(alpha2digit("zero vírgula cinco", "ptbr"), "0,5")

        #     test1 = "cincuenta y tres mil veinte millones doscientos cuarenta y tres mil setecientos veinticuatro"
        #     self.assertEqual(text2num(test1, "ptbr"), 53_020_243_724)

        #     test2 = (
        #         "cincuenta y un millones quinientos setenta y ocho mil trescientos dos"
        #     )
        #     self.assertEqual(text2num(test2, "ptbr"), 51_578_302)

        test3 = "oitenta e cinco"
        self.assertEqual(text2num(test3, "ptbr"), 85)

        test4 = "oitenta e um"
        self.assertEqual(text2num(test4, "ptbr"), 81)

        self.assertEqual(text2num("quinze", "ptbr"), 15)
        self.assertEqual(text2num("cento quinze", "ptbr"), 115)
        self.assertEqual(text2num("setenta e cinco mil", "ptbr"), 75000)
        self.assertEqual(text2num("mil novecentos vinte", "ptbr"), 1920)

    def test_text2num_exc(self):
        self.assertRaises(ValueError, text2num, "mil mil duzentos", "ptbr")
        self.assertRaises(ValueError, text2num, "sessenta quinze", "ptbr")
        self.assertRaises(ValueError, text2num, "sessenta cem", "ptbr")

    def test_text2num_zeroes(self):
        self.assertEqual(text2num("zero", "ptbr"), 0)
        self.assertEqual(text2num("zero oito", "ptbr"), 8)
        self.assertEqual(text2num("zero zero cento vinte e cinco", "ptbr"), 125)
        self.assertRaises(ValueError, text2num, "cinco zero", "ptbr")
        self.assertRaises(ValueError, text2num, "cinquenta zero três", "ptbr")
        self.assertRaises(ValueError, text2num, "cinquenta e três zero", "ptbr")

    def test_alpha2digit_integers(self):
        source = "vinte cinco vacas, doze galinhas e cento vinte e cinco kg de batatas."
        expected = "25 vacas, 12 galinhas e 125 kg de batatas."
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        source = "mil duzentos sessenta e seis dólares."
        expected = "1266 dólares."
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        source = "um dois três quatro vinte quinze"
        expected = "1 2 3 4 20 15"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        source = "vinte e um, trinta e um."
        expected = "21, 31."
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

    def test_relaxed(self):
        source = "um dois três quatro trinta e cinco."
        expected = "1 2 3 4 35."
        self.assertEqual(alpha2digit(source, "ptbr", relaxed=True), expected)

        source = "um dois três quatro vinte, cinco."
        expected = "1 2 3 4 20, 5."
        self.assertEqual(alpha2digit(source, "ptbr", relaxed=True), expected)

        source = "trinta e quatro = trinta quatro"
        expected = "34 = 34"
        self.assertEqual(alpha2digit(source, "ptbr", relaxed=True), expected)

    def test_alpha2digit_formal(self):
        source = "mais trinta e três nove sessenta zero seis doze vinte e um"
        expected = "+33 9 60 06 12 21"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        source = "zero nove sessenta zero seis doze vinte e um"
        expected = "09 60 06 12 21"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

    def test_and(self):
        source = "cinquenta sessenta trinta onze"
        expected = "50 60 30 11"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

    def test_pt_conjunction(self):
        source = "duzentos e quarenta e quatro"
        expected = "244"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        source = "dois mil e vinte"
        expected = "2020"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        source = "mil novecentos e oitenta e quatro"
        expected = "1984"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        source = "mil e novecentos"
        expected = "1900"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        source = "dois mil cento e vinte cinco"
        expected = "2125"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        source = "Trezentos e setenta e oito milhões vinte e sete mil trezentos e doze"
        expected = "378027312"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

    def test_alpha2digit_zero(self):
        source = "treze mil zero noventa"
        expected = "13000 090"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        self.assertEqual(alpha2digit("zero", "ptbr"), "0")

    def test_alpha2digit_decimals(self):
        source = (
            "doze vírgula noventa e nove, cento e vinte vírgula zero cinco, "
            "um vírgula duzentos e trinta e seis, um vírgula dois três seis."
        )
        expected = "12,99, 120,05, 1,236, 1,2 3 6."
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

        self.assertEqual(alpha2digit("vírgula quinze", "ptbr"), "0,15")
        # self.assertEqual(alpha2digit("zero vírgula quinze", "ptbr"), "0,15") # TODO

    def test_alpha2digit_signed(self):
        source = "Temos mais vinte graus dentro e menos quinze fora."
        expected = "Temos +20 graus dentro e -15 fora."
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

    def test_one_as_noun_or_article(self):
        source = "Um momento por favor! trinta e um gatos. Um dois três quatro!"
        expected = "Um momento por favor! 31 gatos. 1 2 3 4!"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)
        # End of segment
        source = "Nem um. Um um. Trinta e um"
        expected = "Nem um. 1 1. 31"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

    def test_accent(self):
        self.assertEqual(text2num("um milhao", "ptbr"), 1000000)
        self.assertEqual(text2num("um milhão", "ptbr"), 1000000)
        self.assertEqual(alpha2digit("Um milhao", "ptbr"), "1000000")
        self.assertEqual(alpha2digit("Um milhão", "ptbr"), "1000000")

    def test_second_as_time_unit_vs_ordinal(self):
        source = "Um segundo por favor! Vigésimo segundo é diferente de vinte segundos."
        expected = "Um segundo por favor! 22º é diferente de 20 segundos."
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

    def test_alpha2digit_ordinals(self):
        source = "Ordinais: primeiro, quinto, terceiro, vigésima, vigésimo primeiro, centésimo quadragésimo quinto"
        expected = "Ordinais: primeiro, 5º, terceiro, 20ª, 21º, 145º"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)

    def test_alpha2digit_ordinals_more(self):
        source = "A décima quarta brigada do exército português, juntamento com o nonagésimo sexto regimento britânico, bateu o centésimo vigésimo sétimo regimento de infantaria de Napoleão"
        expected = "A 14ª brigada do exército português, juntamento com o 96º regimento britânico, bateu o 127º regimento de infantaria de Napoleão"
        self.assertEqual(alpha2digit(source, "ptbr"), expected)
