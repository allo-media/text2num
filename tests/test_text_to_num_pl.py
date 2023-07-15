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
from text_to_num import alpha2digit


class TestTextToNumES(TestCase):
    def test_alpha2digit_integers(self):
        source = "Do dziesięciu"
        expected = "Do 10"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do jedenastu"
        expected = "Do 11"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do dwunastu"
        expected = "Do 12"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do trzynastu "
        expected = "Do 13"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do czternastu"
        expected = "Do 14"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do piętnastu"
        expected = "Do 15"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do szesnastu"
        expected = "Do 16"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do siedemnastu"
        expected = "Do 17"

        source = "Do osiemnastu"
        expected = "Do 18"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do dziewiętnastu"
        expected = "Do 19"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do dwudziestu"
        expected = "Do 20"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do trzydziestu"
        expected = "Do 30"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do czterdziestu"
        expected = "Do 40"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do pięćdziesięciu"
        expected = "Do 50"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do sześćdziesieciu"
        expected = "Do 60"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do siedemdziesieciu"
        expected = "Do 70"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do osiemdziesieciu"
        expected = "Do 80"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do dziewięćdziesięciu"
        expected = "Do 90"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do setki"
        expected = "Do 100"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do stu"
        expected = "Do 100"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do dwustu"
        expected = "Do 200"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do trzystu"
        expected = "Do 300"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do czterystu"
        expected = "Do 400"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do pięciuset"
        expected = "Do 500"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do sześciuset"
        expected = "Do 600"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do siedmiuset"
        expected = "Do 700"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do ośmiuset"
        expected = "Do 800"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do dziewięciuset"
        expected = "Do 900"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "sto"
        expected = "100"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "dwieście"
        expected = "200"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "trzysta"
        expected = "300"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "czterysta"
        expected = "400"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "pięćset"
        expected = "500"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "sześćset"
        expected = "600"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "siedemset"
        expected = "700"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "osiemset"
        expected = "800"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "dziewięćset"
        expected = "900"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Mamy jeden tysiąc"
        expected = "Mamy 1000"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do jednego tysiąca"
        expected = "Do 1000"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Do pięćdziesięciu dwóch tysięcy"
        expected = "Do 52000"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Mamy dwadzieścia dwa tysiące"
        expected = "Mamy 22000"
        self.assertEqual(alpha2digit(source, "pl"), expected)

        source = "Trzeba dwudziestu dwóch tysięcy"
        expected = "Trzeba 22000"
        self.assertEqual(alpha2digit(source, "pl"), expected)