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


class TestTextToNumES(TestCase):
    def test_text2num(self):
        self.assertEqual(text2num("cero", "es"), 0)
        self.assertEqual(text2num("uno", "es"), 1)
        self.assertEqual(text2num("nueve", "es"), 9)
        self.assertEqual(text2num("diez", "es"), 10)
        self.assertEqual(text2num("once", "es"), 11)
        self.assertEqual(text2num("diecinueve", "es"), 19)
        self.assertEqual(text2num("veinte", "es"), 20)
        self.assertEqual(text2num("veintiuno", "es"), 21)
        self.assertEqual(text2num("veintitres", "es"), 23)
        self.assertEqual(text2num("veintitrés", "es"), 23)
        self.assertEqual(text2num("treinta", "es"), 30)
        self.assertEqual(text2num("treinta y uno", "es"), 31)
        self.assertEqual(text2num("treinta y dos", "es"), 32)
        self.assertEqual(text2num("treinta y nueve", "es"), 39)
        self.assertEqual(text2num("noventa y nueve", "es"), 99)
        self.assertEqual(text2num("cien", "es"), 100)
        self.assertEqual(text2num("ciento uno", "es"), 101)
        self.assertEqual(text2num("doscientos", "es"), 200)
        self.assertEqual(text2num("doscientos uno", "es"), 201)
        self.assertEqual(text2num("mil", "es"), 1000)
        self.assertEqual(text2num("mil uno", "es"), 1001)
        self.assertEqual(text2num("dos mil", "es"), 2000)
        self.assertEqual(text2num("dos mil noventa y nueve", "es"), 2099)
        self.assertEqual(text2num("nueve mil novecientos noventa y nueve", "es"), 9999)
        self.assertEqual(text2num("novecientos noventa y nueve mil novecientos noventa y nueve", "es"),
                         999999)
        long_text = "novecientos noventa y nueve mil novecientos noventa y nueve millones novecientos noventa y nueve mil novecientos noventa y nueve"
        self.assertEqual(text2num(long_text, "es"), 999999999999)

        self.assertEqual(alpha2digit("uno coma uno", "es"), '1.1')
        self.assertEqual(alpha2digit("uno coma cuatrocientos uno", "es"), '1.401')

        # TODO:
        # self.assertEqual(alpha2digit("cero coma cinco", "es"), '0.5')

        test1 = "cincuenta y tres mil veinte millones doscientos cuarenta y tres mil setecientos veinticuatro"
        self.assertEqual(text2num(test1, "es"), 53_020_243_724)

        test2 = (
            "cincuenta y un millones quinientos setenta y ocho mil trescientos dos"
        )
        self.assertEqual(text2num(test2, "es"), 51_578_302)

        test3 = "ochenta y cinco"
        self.assertEqual(text2num(test3, "es"), 85)

        test4 = "ochenta y uno"
        self.assertEqual(text2num(test4, "es"), 81)

        self.assertEqual(text2num("quince", "es"), 15)
        self.assertEqual(text2num("ciento quince", "es"), 115)
        self.assertEqual(text2num("setenta y cinco mil", "es"), 75000)
        self.assertEqual(text2num("mil novecientos veinte", "es"), 1920)

    def test_text2num_exc(self):
        self.assertRaises(ValueError, text2num, "mil mil doscientos", "es")
        self.assertRaises(ValueError, text2num, "sesenta quince", "es")
        self.assertRaises(ValueError, text2num, "sesenta cien", "es")

    def test_text2num_zeroes(self):
        self.assertEqual(text2num("cero", "es"), 0)
        self.assertEqual(text2num("cero ocho", "es"), 8)
        self.assertEqual(text2num("cero cero ciento veinticinco", "es"), 125)
        self.assertRaises(ValueError, text2num, "cinco cero", "es")
        self.assertRaises(ValueError, text2num, "cincuenta cero tres", "es")
        self.assertRaises(ValueError, text2num, "cincuenta y tres cero", "es")

    def test_alpha2digit_integers(self):
        source = "veinticinco vacas, doce gallinas y ciento veinticinco kg de patatas."
        expected = "25 vacas, 12 gallinas y 125 kg de patatas."
        self.assertEqual(alpha2digit(source, "es"), expected)

        source = "Habían trescientos hombres y quinientas mujeres"
        expected = "Habían 300 hombres y 500 mujeres"
        self.assertEqual(alpha2digit(source, "es"), expected)

        source = "mil doscientos sesenta y seis dolares."
        expected = "1266 dolares."
        self.assertEqual(alpha2digit(source, "es"), expected)

        source = "un dos tres cuatro veinte quince"
        expected = "1 2 3 4 20 15"
        self.assertEqual(alpha2digit(source, "es"), expected)

        source = "veintiuno, treinta y uno."
        expected = "21, 31."
        self.assertEqual(alpha2digit(source, "es"), expected)

    def test_relaxed(self):
        source = "un dos tres cuatro treinta cinco."
        expected = "1 2 3 4 35."
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

        source = "un dos tres cuatro veinte, cinco."
        expected = "1 2 3 4 20, 5."
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

        source = "treinta y cuatro = treinta cuatro"
        expected = "34 = 34"
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

    def test_female_hundreds(self):
        self.assertEqual(text2num("doscientas", "es"), 200)
        self.assertEqual(text2num("trescientas", "es"), 300)
        self.assertEqual(text2num("cuatrocientas", "es"), 400)
        self.assertEqual(text2num("quinientas", "es"), 500)
        self.assertEqual(text2num("seiscientas", "es"), 600)
        self.assertEqual(text2num("setecientas", "es"), 700)
        self.assertEqual(text2num("ochocientas", "es"), 800)
        self.assertEqual(text2num("novecientas", "es"), 900)

    def test_female_hundreds_with_subnumbers(self):
        self.assertEqual(text2num("doscientas uno", "es"), 201)
        self.assertEqual(text2num("trescientas quince", "es"), 315)
        self.assertEqual(text2num("cuatrocientas veintiocho", "es"), 428)
        self.assertEqual(text2num("quinientas treinta y tres", "es"), 533)
        self.assertEqual(text2num("seiscientas siete", "es"), 607)
        self.assertEqual(text2num("setecientas noventa y una", "es"), 791)
        self.assertEqual(text2num("novecientas noventa y nueve", "es"), 999)
    
    def test_alpha2digit_female_hundreds(self):
        source = "Había doscientas treinta y cuatro vacas en el corral"
        expected = "Había 234 vacas en el corral"
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

        source = "Había trescientas flores en el jardín"
        expected = "Había 300 flores en el jardín"
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

        source = "Teníamos cuatrocientas páginas por leer"
        expected = "Teníamos 400 páginas por leer"
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

        source = "El proyecto requiere quinientas horas de trabajo"
        expected = "El proyecto requiere 500 horas de trabajo"
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

        source = "Se vendieron seiscientas entradas para el concierto"
        expected = "Se vendieron 600 entradas para el concierto"
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

        source = "En la biblioteca hay setecientas revistas"
        expected = "En la biblioteca hay 700 revistas"
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

        source = "Había ochocientas estrellas en el cielo"
        expected = "Había 800 estrellas en el cielo"
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

        source = "El evento atrajo novecientas personas"
        expected = "El evento atrajo 900 personas"
        self.assertEqual(alpha2digit(source, "es", relaxed=True), expected)

    def test_alpha2digit_formal(self):
        source = "mas treinta y tres nueve sesenta cero seis doce veintiuno"
        expected = "+33 9 60 06 12 21"
        self.assertEqual(alpha2digit(source, "es"), expected)

        source = "cero nueve sesenta cero seis doce veintiuno"
        expected = "09 60 06 12 21"
        self.assertEqual(alpha2digit(source, "es"), expected)

    def test_and(self):
        source = "cincuenta sesenta treinta y once"
        expected = "50 60 30 y 11"
        self.assertEqual(alpha2digit(source, "es"), expected)

    def test_alpha2digit_zero(self):
        source = "trece mil cero noventa"
        expected = "13000 090"
        self.assertEqual(alpha2digit(source, "es"), expected)

        self.assertEqual(alpha2digit("cero", "es"), "0")

    def test_alpha2digit_decimals(self):
        source = (
            "doce coma noventa y nueve, ciento veinte coma cero cinco,"
            " uno coma doscientos treinta y seis, uno coma dos tres seis."
        )
        expected = "12.99, 120.05, 1.236, 1.2 3 6."
        self.assertEqual(alpha2digit(source, "es"), expected)

        self.assertEqual(alpha2digit("coma quince", "es"), "0.15")
        # self.assertEqual(alpha2digit("cero coma quince", "es"), "0.15")  # TODO

    def test_alpha2digit_signed(self):
        source = "Tenemos mas veinte grados dentro y menos quince fuera."
        expected = "Tenemos +20 grados dentro y -15 fuera."
        self.assertEqual(alpha2digit(source, "es"), expected)

    def test_one_as_noun_or_article(self):
        source = "Un momento por favor! treinta y un gatos. Uno dos tres cuatro!"
        expected = "Un momento por favor! 31 gatos. 1 2 3 4!"
        self.assertEqual(alpha2digit(source, "es"), expected)
        # End of segment
        source = "Ni uno. Uno uno. Treinta y uno"
        expected = "Ni uno. 1 1. 31"
        self.assertEqual(alpha2digit(source, "es"), expected)

    def test_accent(self):
        self.assertEqual(text2num("un millon", "es"), 1000000)
        self.assertEqual(text2num("un millón", "es"), 1000000)
        self.assertEqual(alpha2digit("Un millon", "es"), "1000000")
        self.assertEqual(alpha2digit("Un millón", "es"), "1000000")

    # ord2card NOT implemented in Spanish
    """
    def test_second_as_time_unit_vs_ordinal(self):
        source = "Un segundo por favor! Vigésimo segundo es diferente que veinte segundos."
        expected = "Un segundo por favor! 22º es diferente que 20 segundos."
        self.assertEqual(alpha2digit(source, "es"), expected)

    def test_alpha2digit_ordinals(self):
        source = (
            "Quinto tercero segundo vigesimo primero centésimo."
        )
        expected = "5º 3º segundo 21º 100º."
        self.assertEqual(alpha2digit(source, "es"), expected)

    def test_alpha2digit_ordinals_gender_and_number(self):
        source = "Él ha quedado tercero"
        expected = "Él ha quedado 3º"
        self.assertEqual(alpha2digit(source, "es"), expected)
        source = "Ella ha quedado tercera"
        expected = "Ella ha quedado 3ª"
        self.assertEqual(alpha2digit(source, "es"), expected)
        source = "Ellos han quedado terceros"
        expected = "Ellos han quedado 3º"
        self.assertEqual(alpha2digit(source, "es"), expected)
        source = "Ellas han quedado terceras"
        expected = "Ellas han quedado 3ª"
        self.assertEqual(alpha2digit(source, "es"), expected)
    """
