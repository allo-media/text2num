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


class TestTextToNumEN(TestCase):
    def test_text2num(self):
        test1 = "fifty-three billion two hundred forty-three thousand seven hundred twenty-four"
        self.assertEqual(text2num(test1, "en"), 53_000_243_724)

        test2 = (
            "fifty-one million five hundred seventy-eight thousand three hundred two"
        )
        self.assertEqual(text2num(test2, "en"), 51_578_302)

        test3 = "eighty-five"
        self.assertEqual(text2num(test3, "en"), 85)

        test4 = "eighty-one"
        self.assertEqual(text2num(test4, "en"), 81)

        self.assertEqual(text2num("fifteen", "en"), 15)
        self.assertEqual(text2num("hundred fifteen", "en"), 115)
        self.assertEqual(text2num("one hundred fifteen", "en"), 115)
        self.assertEqual(text2num("seventy-five thousands", "en"), 75000)
        self.assertEqual(text2num("thousand nine hundred twenty", "en"), 1920)
        self.assertEqual(text2num("one billion twenty-five millions", "en"), 1_025_000_000)

    def test_text2num_exc(self):
        self.assertRaises(ValueError, text2num, "thousand thousand two hundreds", "en")
        self.assertRaises(ValueError, text2num, "sixty fifteen", "en")
        self.assertRaises(ValueError, text2num, "hundred hundreds", "en")

    def test_text2num_zeroes(self):
        self.assertEqual(text2num("zero", "en"), 0)
        self.assertEqual(text2num("zero eight", "en"), 8)
        self.assertEqual(text2num("zero zero hundred twenty five", "en"), 125)
        self.assertRaises(ValueError, text2num, "five zero", "en")
        self.assertRaises(ValueError, text2num, "fifty zero three", "en")
        self.assertRaises(ValueError, text2num, "fifty three zero", "en")

    def test_text2num_hundreds(self):
        source = "forty five hundred thirty eight"
        expected = 4538
        self.assertEqual(text2num(source, "en"), expected)
        self.assertEqual(text2num("nineteen hundred seventy-three", "en"), 1973)
        self.assertEqual(text2num("sixty hundred", "en"), 6000)

    def test_alpha2digit_integers(self):
        source = "twenty-five cows, twelve chickens and one hundred twenty five kg of potatoes."
        expected = "25 cows, 12 chickens and 125 kg of potatoes."
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "one thousand two hundred sixty-six dollars."
        expected = "1266 dollars."
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "one two three four twenty fifteen"
        expected = "1 2 3 4 20 15"
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "twenty-one, thirty-one."
        expected = "21, 31."
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_relaxed(self):
        source = "one two three four twenty five."
        expected = "1 2 3 4 25."
        self.assertEqual(alpha2digit(source, "en", relaxed=True), expected)

        source = "one two three four twenty, five."
        expected = "1 2 3 4 20, 5."
        self.assertEqual(alpha2digit(source, "en", relaxed=True), expected)

        source = "thirty-four = thirty four"
        expected = "34 = 34"
        self.assertEqual(alpha2digit(source, "en", relaxed=True), expected)

    def test_alpha2digit_hundreds(self):
        source = "forty five hundred thirty eight dollars and eighteen cents"
        expected = "4538 dollars and 18 cents"
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_alpha2digit_formal(self):
        source = "plus thirty-three nine sixty zero six twelve twenty-one"
        expected = "+33 9 60 06 12 21"
        self.assertEqual(alpha2digit(source, "en"), expected)
        source = "plus thirty-three nine sixty o six twelve twenty-one"
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "zero nine sixty zero six twelve twenty-one"
        expected = "09 60 06 12 21"
        self.assertEqual(alpha2digit(source, "en"), expected)
        source = "o nine sixty o six twelve twenty-one"
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "My name is o s c a r."
        self.assertEqual(alpha2digit(source, "en"), source)

    def test_and(self):
        source = "fifty sixty thirty and eleven"
        expected = "50 60 30 and 11"
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_alpha2digit_zero(self):
        source = "thirteen thousand zero ninety"
        expected = "13000 090"
        self.assertEqual(alpha2digit(source, "en"), expected)
        source = "thirteen thousand o ninety"
        self.assertEqual(alpha2digit(source, "en"), expected)

        self.assertEqual(alpha2digit("zero", "en"), "0")
        self.assertEqual(alpha2digit("zero love", "en"), "0 love")

    def test_alpha2digit_ordinals(self):
        source = (
            "Fifth third second twenty-first hundredth one thousand two hundred thirtieth twenty-fifth thirty-eighth forty-ninth."
        )
        expected = "5th third second 21st 100th 1230th 25th 38th 49th."
        self.assertEqual(alpha2digit(source, "en"), expected)
        source = (
            "first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth."
        )
        expected = "first, second, third, 4th, 5th, 6th, 7th, 8th, 9th, 10th."
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "twenty second position at the twenty first event lost after the first second"
        expected = "22nd position at the 21st event lost after the first second"
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_alpha2digit_ordinals_force(self):
        source = (
            "first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth."
        )
        expected = "1st, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, 9th, 10th."
        self.assertEqual(alpha2digit(source, "en", ordinal_threshold=0), expected)

    def test_alpha2digit_decimals(self):
        source = (
            "twelve point ninety-nine, one hundred twenty point zero five,"
            " one hundred twenty point o five, one point two hundred thirty-six."
        )
        expected = "12.99, 120.05, 120.05, 1.236."
        self.assertEqual(alpha2digit(source, "en"), expected)

        self.assertEqual(alpha2digit("point fifteen", "en"), "0.15")

        self.assertEqual(alpha2digit("The average density is zero point five", "en"), "The average density is 0.5")

    def test_alpha2digit_signed(self):
        source = "We have plus twenty degrees inside and minus fifteen outside."
        expected = "We have +20 degrees inside and -15 outside."
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_one_as_noun_or_article(self):
        source = "This is the one I'm looking for. One moment please! Twenty one cats. One two three four!"
        expected = "This is the one I'm looking for. One moment please! 21 cats. 1 2 3 4!"
        self.assertEqual(alpha2digit(source, "en"), expected)
        source = "No one is innocent. Another one bites the dust."
        self.assertEqual(alpha2digit(source, "en"), source)
        source = "one cannot know"
        self.assertEqual(alpha2digit(source, "en"), source)
        # Following an ordinal
        source = "the sixth one"
        expected = "the 6th one"
        self.assertEqual(alpha2digit(source, "en"), expected)
        # End of segment
        source = "No one. Another one. One one. Twenty one"
        expected = "No one. Another one. 1 1. 21"
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_second_as_time_unit_vs_ordinal(self):
        source = "One second please! twenty second is parsed as twenty-second and is different from twenty seconds."
        expected = "One second please! 22nd is parsed as 22nd and is different from 20 seconds."
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_uppercase(self):
        source = "FIFTEEN ONE TEN ONE"
        expected = "15 1 10 1"
        self.assertEqual(alpha2digit(source, "en"), expected)
