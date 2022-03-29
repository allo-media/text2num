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
import sys

"""
Test the ``text_to_num`` library.
"""
from unittest import TestCase
from text_to_num import alpha2digit, text2num


class TestTextToNumRU(TestCase):
    def test_text2num(self):
        test1 = "пятьдесят три миллиарда двести сорок три тысячи семьсот двадцать четыре"
        self.assertEqual(text2num(test1, 'ru'), 53_000_243_724)

        test2 = (
            "пятьдесят один миллион пятьсот семьдесят восемь тысяч триста два"
        )
        self.assertEqual(text2num(test2, 'ru'), 51_578_302)

        test3 = "восемьдесят пять"
        self.assertEqual(text2num(test3, 'ru'), 85)

        test4 = "восемьдесят один"
        self.assertEqual(text2num(test4, 'ru'), 81)

        self.assertEqual(text2num("пятьнадцать", 'ru'), 15)
        self.assertEqual(text2num("сто пятьнадцать", 'ru'), 115)
        self.assertEqual(text2num("сто пятнадцать", 'ru'), 115)
        self.assertEqual(text2num("семьдесят пять тысяч", 'ru'), 75000)
        self.assertEqual(text2num("тысяча девятьсот двадцать", 'ru'), 1920)
        self.assertEqual(text2num("одна тысяча девятьсот двадцать", 'ru'), 1920)

    def test_text2num_centuries(self):
        self.assertEqual(text2num("тысяча девятьсот семьдесят три", 'ru'), 1973)

    def test_text2num_exc(self):
        self.assertRaises(ValueError, text2num, "тысяча тысяча двести", 'ru')
        self.assertRaises(ValueError, text2num, "шестьдесят пятьдесят", 'ru')
        self.assertRaises(ValueError, text2num, "шестьдесят сто", 'ru')

    def test_text2num_zeroes(self):
        self.assertEqual(0, text2num("ноль", 'ru'))
        self.assertEqual(8, text2num("ноль восемь", 'ru'), 8)
        self.assertEqual(125, text2num("ноль ноль сто двадцать пять", 'ru'))
        self.assertRaises(ValueError, text2num, "пять ноль", 'ru')
        self.assertRaises(ValueError, text2num, "пять ноль три", 'ru')
        self.assertRaises(ValueError, text2num, "пятьдесят три ноль", 'ru')

    def test_alpha2digit_phones(self):
        source = "восемь девятьсот два сто один ноль один ноль один"
        expected = "8 902 101 01 01"
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        source = "плюс семь восемьсот пятьдесят девять сто один ноль сто один"
        expected = "+7 859 101 0101"
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        source = "Телефон восемь девятьсот шестьдесят два пятьсот девятнадцать семьдесят ноль ноль"
        expected = "Телефон 8 962 519 70 00"
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        source = "три сто пять сто один ноль один ноль один"
        expected = "3 105 101 01 01"
        self.assertEqual(expected, alpha2digit(source, 'ru'))

    def test_alpha2digit_integers(self):
        source = "Двадцать пять коров, двенадцать сотен цыплят и сто двадцать пять точка сорок кг картофеля."
        expected = "25 коров, 1200 цыплят и 125.40 кг картофеля."
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        source = "Одна сотня огурцов, две сотни помидор, пять сотен рублей."
        expected = "100 огурцов, 200 помидор, 500 рублей."
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        source = "одна тысяча двести шестьдесят шесть рублей."
        expected = "1266 рублей."
        self.assertEqual(expected, alpha2digit(source, 'ru'))
        source = "тысяча двести шестьдесят шесть рублей."
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        source = "один, два, три, четыре, двадцать, пятьнадцать"
        expected = "1, 2, 3, 4, 20, 15"
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        source = "двадцать один, тридцать один."
        expected = "21, 31."
        self.assertEqual(expected, alpha2digit(source, 'ru'))

    def test_relaxed(self):
        source = "один два три четыре двадцать пять."
        expected = "1 2 3 4 25."
        self.assertEqual(expected, alpha2digit(source, 'ru', relaxed=True))

        source = "один два три четыре двадцать, пять."
        expected = "1 2 3 4 20, 5."
        self.assertEqual(expected, alpha2digit(source, 'ru', relaxed=True))

    def test_alpha2digit_formal(self):
        source = "плюс тридцать три, девять, шестьдесят, ноль шесть, двенадцать, двадцать один"
        expected = "+33, 9, 60, 06, 12, 21"
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        source = "ноль девять, шестьдесят, ноль шесть, двенадцать, двадцать один"
        expected = "09, 60, 06, 12, 21"
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        source = "Сам по себе я одиночка"
        self.assertEqual(source, alpha2digit(source, 'ru'))

    def test_and(self):
        source = "пятьдесят, шестьдесят, тридцать и одиннадцать"
        expected = "50, 60, 30 и 11"
        self.assertEqual(expected, alpha2digit(source, 'ru'))

    def test_alpha2digit_zero(self):
        source = "тринадцать тысяч, ноль девяносто"
        expected = "13000, 090"
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        self.assertEqual("0", alpha2digit("ноль", 'ru'))

    def test_alpha2digit_ordinals_force(self):
        source = (
            "Пятый, третий, второй, двадцать первый, сотый, тысяча двести тридцатый, двадцать пятый, тридцать восьмой, сорок девятый."
        )
        expected = "5ый, 3ий, 2ой, 21ый, 100ый, 1230ый, 25ый, 38ой, 49ый."
        self.assertEqual(expected, alpha2digit(source, 'ru', ordinal_threshold=0))
        source = (
            "первый, второй, третий, четвёртый, четвертый, пятый, шестой, седьмой, восьмой, девятый, десятый."
        )
        expected = "1ый, 2ой, 3ий, 4ый, 4ый, 5ый, 6ой, 7ой, 8ой, 9ый, 10ый."
        self.assertEqual(expected, alpha2digit(source, 'ru', ordinal_threshold=0))

        source = "двадцать второе место на двадцать первой олимпиаде занял первый и второй"
        expected = "22ое место на 21ой олимпиаде занял 1ый и 2ой"
        self.assertEqual(expected, alpha2digit(source, 'ru', ordinal_threshold=0))

        source = "каждый пятый на первый второй расчитайсь!"
        expected = "каждый 5ый на 1ый 2ой расчитайсь!"
        self.assertEqual(expected, alpha2digit(source, 'ru', ordinal_threshold=0))

    def test_alpha2digit_decimals(self):
        source = (
            "двенадцать точка девяносто девять, сто двадцать точка ноль пять,"
            " сто двадцать целых ноль пять, одна целая двести тридцать шесть."
        )
        expected = "12.99, 120.05, 120.05, 1.236."
        self.assertEqual(expected, alpha2digit(source, 'ru'))

        self.assertEqual("0.15", alpha2digit("точка пятьнадцать", 'ru'))
        self.assertEqual("0.15", alpha2digit("ноль целых пятьнадцать", 'ru'))

    def test_alpha2digit_signed(self):
        source = "В комнате плюс двадцать градусов, тогда как на улице минус пятьдесят."
        expected = "В комнате +20 градусов, тогда как на улице -50."
        self.assertEqual(expected, alpha2digit(source, 'ru'))

    def test_uppercase(self):
        source = "ПЯТЬНАДЦАТЬ ОДИН ДЕСЯТЬ ОДИН"
        expected = "15 1 10 1"
        self.assertEqual(expected, alpha2digit(source, 'ru'))

    def test_hundreds(self):
        source = "пятьдесят один миллион пятьсот семьдесят восемь тысяч триста два"
        expected = 51578302
        self.assertEqual(expected, text2num(source, 'ru'))

        source = "восемьдесят один"
        expected = 81
        self.assertEqual(expected, text2num(source, 'ru'))

        source = "восемьсот"
        expected = 800
        self.assertEqual(expected, text2num(source, 'ru'))

        source = "сто"
        expected = 100
        self.assertEqual(expected, text2num(source, 'ru'))

        source = "сто двадцать"
        expected = 120
        self.assertEqual(expected, text2num(source, 'ru'))

        source = "сто два"
        expected = 102
        self.assertEqual(expected, text2num(source, 'ru'))

        source = "семьсот один"
        expected = 701

        self.assertEqual(expected, text2num(source, 'ru'))
        source = "восемьсот миллионов"
        expected = 800_000_000
        self.assertEqual(expected, text2num(source, 'ru'))


    def test_big_numbers(self):
        source = "триллион миллиард миллион тысяча один"
        expected = 1_001_001_001_001
        self.assertEqual(expected, text2num(source, 'ru'))

        source = "один триллион один миллиард один миллион одна тысяча один"
        expected = 1_001_001_001_001
        self.assertEqual(expected, text2num(source, 'ru'))

        source = "одиннадцать триллионов одиннадцать миллиардов одиннадцать миллионов одиннадцать тысяч одиннадцать"
        expected = 11_011_011_011_011
        self.assertEqual(expected, text2num(source, 'ru'))

        source = "сто одиннадцать триллионов сто одиннадцать миллиардов сто одиннадцать миллионов сто одиннадцать тысяч сто одиннадцать"
        expected = 111_111_111_111_111
        self.assertEqual(expected, text2num(source, 'ru'))

        source = "сто десять триллионов сто десять миллиардов сто десять миллионов сто десять тысяч сто десять"
        expected = 110_110_110_110_110
        self.assertEqual(expected, text2num(source, 'ru'))


