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
        self.assertEqual(text2num("zero", "pt"), 0)
        self.assertEqual(text2num("um", "pt"), 1)
        self.assertEqual(text2num("oito", "pt"), 8)
        self.assertEqual(text2num("dez", "pt"), 10)
        self.assertEqual(text2num("onze", "pt"), 11)
        self.assertEqual(text2num("dezanove", "pt"), 19)
        self.assertEqual(text2num("vinte", "pt"), 20)
        self.assertEqual(text2num("vinte e um", "pt"), 21)
        self.assertEqual(text2num("trinta", "pt"), 30)
        self.assertEqual(text2num("trinta e um", "pt"), 31)
        self.assertEqual(text2num("trinta e dois", "pt"), 32)
        self.assertEqual(text2num("trinta e três", "pt"), 33)
        self.assertEqual(text2num("trinta e nove", "pt"), 39)
        self.assertEqual(text2num("noventa e nove", "pt"), 99)
        self.assertEqual(text2num("cem", "pt"), 100)
        self.assertEqual(text2num("cento e um", "pt"), 101)
        self.assertEqual(text2num("duzentos", "pt"), 200)
        self.assertEqual(text2num("duzentos e um", "pt"), 201)
        self.assertEqual(text2num("mil", "pt"), 1000)
        self.assertEqual(text2num("mil e um", "pt"), 1001)
        self.assertEqual(text2num("dois mil", "pt"), 2000)
        self.assertEqual(text2num("dois mil noventa e nove", "pt"), 2099)
        self.assertEqual(
            text2num("nove mil novecentos noventa e nove", "pt"), 9999)
        self.assertEqual(text2num(
            "novecentos noventa e nove mil novecentos noventa e nove", "pt"), 999999)


    #     test1 = "cincuenta y tres mil veinte millones doscientos cuarenta y tres mil setecientos veinticuatro"
    #     self.assertEqual(text2num(test1, "pt"), 53_020_243_724)

    #     test2 = (
    #         "cincuenta y un millones quinientos setenta y ocho mil trescientos dos"
    #     )
    #     self.assertEqual(text2num(test2, "pt"), 51_578_302)

        test3 = "oitenta e cinco"
        self.assertEqual(text2num(test3, "pt"), 85)

        test4 = "oitenta e um"
        self.assertEqual(text2num(test4, "pt"), 81)

        self.assertEqual(text2num("quinze", "pt"), 15)
        self.assertEqual(text2num("cento quinze", "pt"), 115)
        self.assertEqual(text2num("setenta e cinco mil", "pt"), 75000)
        self.assertEqual(text2num("mil novecentos vinte", "pt"), 1920)

    def test_text2num_exc(self):
        self.assertRaises(ValueError, text2num, "mil mil duzentos", "pt")
        self.assertRaises(ValueError, text2num, "sessenta quinze", "pt")
        self.assertRaises(ValueError, text2num, "sessenta cem", "pt")
        # self.assertRaises(ValueError, text2num, "cem e um", "pt")


    def test_text2num_zeroes(self):
        self.assertEqual(text2num("zero", "pt"), 0)
        self.assertEqual(text2num("zero oito", "pt"), 8)
        self.assertEqual(text2num("zero zero cento vinte e cinco", "pt"), 125)
        self.assertRaises(ValueError, text2num, "cinco zero", "pt")
        self.assertRaises(ValueError, text2num, "cinquenta zero três", "pt")
        self.assertRaises(ValueError, text2num, "cinquenta e três zero", "pt")

    def test_alpha2digit_integers(self):
        source = "vinte cinco vacas, doze galinhas e cento vinte e cinco kg de batatas."
        expected = "25 vacas, 12 galinhas e 125 kg de batatas."
        self.assertEqual(alpha2digit(source, "pt"), expected)

        source = "mil duzentos sessenta e seis dólares."
        expected = "1266 dólares."
        self.assertEqual(alpha2digit(source, "pt"), expected)

        source = "um dois três quatro vinte quinze"
        expected = "1 2 3 4 20 15"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        source = "vinte e um, trinta e um."
        expected = "21, 31."
        self.assertEqual(alpha2digit(source, "pt"), expected)

    def test_relaxed(self):
        source = "um dois três quatro trinta e cinco."
        expected = "1 2 3 4 35."
        self.assertEqual(alpha2digit(source, "pt", relaxed=True), expected)

        source = "um dois três quatro vinte, cinco."
        expected = "1 2 3 4 20, 5."
        self.assertEqual(alpha2digit(source, "pt", relaxed=True), expected)

        source = "trinta e quatro = trinta quatro"
        expected = "34 = 34"
        self.assertEqual(alpha2digit(source, "pt", relaxed=True), expected)

        # source = "cem e dois"
        # expected = "100 e 2"
        # self.assertEqual(alpha2digit(source, "pt", relaxed=True), expected)

    def test_alpha2digit_formal(self):
        source = "mais trinta e três nove sessenta zero seis doze vinte e um"
        expected = "+33 9 60 06 12 21"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        source = "zero nove sessenta zero seis doze vinte e um"
        expected = "09 60 06 12 21"
        self.assertEqual(alpha2digit(source, "pt"), expected)

    def test_and(self):
        source = "cinquenta sessenta trinta onze"
        expected = "50 60 30 11"
        self.assertEqual(alpha2digit(source, "pt"), expected)

    def test_pt_conjunction(self):
        source = "duzentos e quarenta e quatro"
        expected = "244"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        source = "dois mil e vinte"
        expected = "2020"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        source = "mil novecentos e oitenta e quatro"
        expected = "1984"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        source = "mil e novecentos"
        expected = "1900"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        source = "dois mil cento e vinte cinco"
        expected = "2125"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        source = "Trezentos e setenta e oito milhões vinte e sete mil trezentos e doze"
        expected = "378027312"
        self.assertEqual(alpha2digit(source, "pt"), expected)

    def test_alpha2digit_zero(self):
        source = "treze mil zero noventa"
        expected = "13000 090"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        self.assertEqual(alpha2digit("zero", "pt"), "0")

    def test_alpha2digit_decimals(self):
        source = (
            "doze vírgula noventa e nove, cento e vinte vírgula zero cinco, "
            "um vírgula duzentos e trinta e seis, um vírgula dois três seis."
        )
        expected = "12,99, 120,05, 1,236, 1,2 3 6."
        self.assertEqual(alpha2digit(source, "pt"), expected)

        self.assertEqual(alpha2digit("vírgula quinze", "pt"), "0,15")
        self.assertEqual(alpha2digit("zero vírgula quinze", "pt"), "0,15")
        self.assertEqual(alpha2digit("um vírgula um", "pt"), "1,1")
        self.assertEqual(alpha2digit(
            "um vírgula quatrocentos e um", "pt"), "1,401")

        self.assertEqual(alpha2digit("zero vírgula cinco", "pt"), "0,5")


    def test_alpha2digit_signed(self):
        source = "Temos mais vinte graus dentro e menos quinze fora."
        expected = "Temos +20 graus dentro e -15 fora."
        self.assertEqual(alpha2digit(source, "pt"), expected)

    def test_one_as_noun_or_article(self):
        source = "Um momento por favor! trinta e um gatos. Um dois três quatro!"
        expected = "Um momento por favor! 31 gatos. 1 2 3 4!"
        self.assertEqual(alpha2digit(source, "pt"), expected)
        # End of segment
        source = "Nem um. Um um. Trinta e um"
        expected = "Nem um. 1 1. 31"
        self.assertEqual(alpha2digit(source, "pt"), expected)

    def test_accent(self):
        self.assertEqual(text2num("um milhao", "pt"), 1000000)
        self.assertEqual(text2num("um milhão", "pt"), 1000000)
        self.assertEqual(alpha2digit("Um milhao", "pt"), "1000000")
        self.assertEqual(alpha2digit("Um milhão", "pt"), "1000000")

    def test_second_as_time_unit_vs_ordinal(self):
        source = "Um segundo por favor! Vigésimo segundo é diferente de vinte segundos."
        expected = "Um segundo por favor! 22º é diferente de 20 segundos."
        self.assertEqual(alpha2digit(source, "pt"), expected)

    def test_alpha2digit_ordinals(self):
        source = "Ordinais: primeiro, quinto, terceiro, vigésima, vigésimo primeiro, centésimo quadragésimo quinto"
        expected = "Ordinais: primeiro, 5º, terceiro, 20ª, 21º, 145º"
        self.assertEqual(alpha2digit(source, "pt"), expected)

    def test_alpha2digit_ordinals_more(self):
        source = "A décima quarta brigada do exército português, juntamento com o nonagésimo sexto regimento britânico, bateu o centésimo vigésimo sétimo regimento de infantaria de Napoleão"
        expected = "A 14ª brigada do exército português, juntamento com o 96º regimento britânico, bateu o 127º regimento de infantaria de Napoleão"
        self.assertEqual(alpha2digit(source, "pt"), expected)

    def test_brazilian_tenths(self):
        self.assertEqual(text2num("catorze", "pt"), 14)
        self.assertEqual(text2num("mil quatrocentos e catorze", "pt"), 1414)

        source = "em mil quinhentos e catorze, ela nasceu"
        expected = "em 1514, ela nasceu"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        self.assertEqual(text2num("dezesseis", "pt"), 16)
        self.assertEqual(text2num("mil seiscentos e dezesseis", "pt"), 1616)
        source = "tudo aconteceu até mil novecentos e dezesseis"
        expected = "tudo aconteceu até 1916"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        self.assertEqual(text2num("dezessete", "pt"), 17)
        self.assertEqual(text2num("mil setecentos e dezessete", "pt"), 1717)
        source = "em dezessete de janeiro de mil novecentos e noventa"
        expected = "em 17 de janeiro de 1990"
        self.assertEqual(alpha2digit(source, "pt"), expected)

        self.assertEqual(text2num("dezenove", "pt"), 19)
        self.assertEqual(text2num("mil novecentos e dezenove", "pt"), 1919)
        source = "quanto é dezenove menos três? É dezesseis"
        expected = "quanto é 19 menos 3? É 16"
        self.assertEqual(alpha2digit(source, "pt", signed=False), expected)

    def test_brazilian_multipliers(self):
        self.assertEqual(text2num("um milhão quatrocentos e trinta e três", "pt"), 1000433)
        self.assertEqual(text2num("dois milhões oitocentos e quarenta e quatro mil trezentos e trinta e três", "pt"), 2844333)

        self.assertEqual(text2num("cinquenta e três bilhões duzentos e quarenta e três mil setecentos e vinte e quatro", "pt"), 53_000_243_724)


