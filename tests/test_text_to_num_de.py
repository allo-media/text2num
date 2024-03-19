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

# TODO: we need to improve tests to use 'relaxed=True' explicitly.
# without 'relaxed' some things should fail, e.g.: text2num("ein und zwanzig", "de")


class TestTextToNumDE(TestCase):
    def test_text2num(self):
        self.assertEqual(text2num("null", "de"), 0)

        test1 = "dreiundfünfzig Milliarden zweihundertdreiundvierzigtausendsiebenhundertvierundzwanzig"
        self.assertEqual(text2num(test1, "de"), 53_000_243_724)

        test2 = "einundfünfzig Millionen fünfhundertachtundsiebzigtausenddreihundertzwei"
        self.assertEqual(text2num(test2, "de"), 51_578_302)

        test3 = "fünfundachtzig"
        self.assertEqual(text2num(test3, "de"), 85)

        test4 = "einundachtzig"
        self.assertEqual(text2num(test4, "de"), 81)

        self.assertEqual(text2num("fünfzehn", "de"), 15)
        self.assertEqual(text2num("zwei und vierzig", "de"), 42)
        self.assertEqual(text2num("einhundertfünfzehn", "de"), 115)
        self.assertEqual(text2num("einhundert fünfzehn", "de"), 115)
        self.assertEqual(text2num("ein hundert fünfzehn", "de"), 115)
        self.assertEqual(text2num("hundertfünfzehn", "de"), 115)
        self.assertEqual(text2num("hundert fünfzehn", "de"), 115)
        self.assertEqual(text2num("fünfundsiebzigtausend", "de"), 75000)
        self.assertEqual(text2num("eintausendneunhundertzwanzig", "de"), 1920)

    def test_text2num_centuries(self):
        self.assertEqual(text2num("neunzehnhundertdreiundsiebzig", "de"), 1973)

    def test_text2num_exc(self):
        # Expected to fail:
        self.assertRaises(ValueError, text2num, "tausendtausendzweihundert", "de")
        self.assertRaises(ValueError, text2num, "sechzigfünfzehn", "de")
        self.assertRaises(ValueError, text2num, "sechzighundert", "de")
        self.assertRaises(ValueError, text2num, "zwei und vierzig und", "de")
        self.assertRaises(ValueError, text2num, "dreißig und elf", "de")
        self.assertRaises(ValueError, text2num, "ein und zehn", "de")
        self.assertRaises(ValueError, text2num, "zwei und neunzehn", "de")
        self.assertRaises(ValueError, text2num, "zwanzig zweitausend", "de")
        self.assertRaises(ValueError, text2num, "hundert und elf", "de")    # TODO: humans get this...
        self.assertRaises(ValueError, text2num, "hundert und eins", "de")   # TODO: humans get this...
        self.assertRaises(ValueError, text2num, "eins und zwanzig", "de", relaxed=True)
        self.assertRaises(ValueError, text2num, "eine und zwanzig", "de", relaxed=True)

    def test_text2num_zeroes(self):
        self.assertEqual(text2num("null", "de"), 0)
        # Expected to fail:
        self.assertRaises(ValueError, text2num, "null acht", "de")  # This is not allowed, use alpha2digit
        self.assertRaises(ValueError, text2num, "null null hundertfünfundzwanzig", "de")
        self.assertRaises(ValueError, text2num, "fünf null", "de")
        self.assertRaises(ValueError, text2num, "fünfzignullzwei", "de")
        self.assertRaises(ValueError, text2num, "fünfzigdreinull", "de")

    def test_text2num_hundred_addition(self):
        self.assertRaises(ValueError, text2num, "achtundachtzig dreihundert", "de")
        self.assertRaises(ValueError, text2num, "zwanzig dreihundert", "de")
        self.assertRaises(ValueError, text2num, "zwei zwölfhundert", "de")

    def test_alpha2digit_integers(self):
        source = "fünfundzwanzig Kühe, zwölf Hühner und einhundertfünfundzwanzig kg Kartoffeln."
        expected = "25 Kühe, 12 Hühner und 125 kg Kartoffeln."
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "Eintausendzweihundertsechsundsechzig Dollar."
        expected = "1266 Dollar."
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "eins zwei drei vier zwanzig fünfzehn"
        expected = "1 2 3 4 20 15"
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "einundzwanzig, einunddreißig."
        expected = "21, 31."
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "zweiundzwanzig zweitausendeinundzwanzig"
        expected = "22 2021"
        self.assertEqual(alpha2digit(source, "de"), expected)
        source = "zwei und zwanzig zwei tausend ein und zwanzig"
        expected = "22 2021"
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "tausend hundertzweitausend zweihunderttausend vierzehntausend"
        expected = "1000 102000 200000 14000"
        self.assertEqual(alpha2digit(source, "de"), expected)

    def test_relaxed(self):
        # TODO: relaxed is not yet supported but 'True' by default right now
        source = "eins zwei drei vier fünf und zwanzig."
        expected = "1 2 3 4 25."        # TODO: only humans can see the pattern ^^
        self.assertEqual(alpha2digit(source, "de", relaxed=True), expected)

        source = "eins zwei drei vier fünf und zuletzt zwanzig."
        expected = "1 2 3 4 5 und zuletzt 20."
        self.assertEqual(alpha2digit(source, "de", relaxed=True), expected)

        source = "eins zwei drei vier fünfundzwanzig."
        expected = "1 2 3 4 25."
        self.assertEqual(alpha2digit(source, "de", relaxed=True), expected)

        source = "eins zwei drei vier fünf zwanzig."
        expected = "1 2 3 4 5 20."
        self.assertEqual(alpha2digit(source, "de", relaxed=True), expected)

        source = "vier und dreißig = vierunddreißig"
        expected = "34 = 34"
        self.assertEqual(alpha2digit(source, "de", relaxed=True), expected)

        source = "Ein hundert ein und dreißig"
        expected = "131"
        self.assertEqual(alpha2digit(source, "de", relaxed=True), expected)

        source = "Einhundert und drei"  # TODO: actually this is unclear
        expected = "100 und 3"
        self.assertEqual(alpha2digit(source, "de", relaxed=True), expected)

        source = "eins und zwanzig ist nicht einundzwanzig"
        expected = "1 und 20 ist nicht 21"
        self.assertEqual(alpha2digit(source, "de", relaxed=True), expected)

        source = "Einhundert und Ende"
        expected = "100 und Ende"
        self.assertEqual(alpha2digit(source, "de", relaxed=True), expected)

        source = "Einhundert und und"
        expected = "100 und und"
        self.assertEqual(alpha2digit(source, "de", relaxed=True), expected)

    def test_alpha2digit_formal(self):
        source = "plus dreiunddreißig neun sechzig null sechs zwölf einundzwanzig"
        alpha2digit(source, "de")
        expected = "+33 9 60 0 6 12 21"
        self.assertEqual(alpha2digit(source, "de"), expected)
        source = "plus dreiunddreißig neun sechzig 0 sechs zwölf einundzwanzig"
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "null neun sechzig null sechs zwölf einundzwanzig"
        expected = "0 9 60 0 6 12 21"
        self.assertEqual(alpha2digit(source, "de"), expected)

    def test_and(self):
        source = "fünfzig sechzig dreißig und elf"
        expected = "50 60 30 und 11"
        self.assertEqual(alpha2digit(source, "de"), expected)

    def test_alpha2digit_zero(self):
        source = "dreizehntausend null neunzig"
        expected = "13000 0 90"
        self.assertEqual(alpha2digit(source, "de"), expected)

        result = alpha2digit("null", "de")
        self.assertEqual(result, "0")

    def test_alpha2digit_ordinals(self):
        source = (
            "erster, zweiter, dritter, vierter, fünfter, sechster, siebter, achter, neunter."
        )
        expected = "1., 2., 3., 4., 5., 6., 7., 8., 9.."
        self.assertEqual(alpha2digit(source, "de", ordinal_threshold=0), expected)

        source = (
            "zehnter, zwanzigster, einundzwanzigster, fünfundzwanzigster, achtunddreißigster, "
            "neunundvierzigster, hundertster, eintausendzweihundertdreißigster."
        )
        expected = "10., 20., 21., 25., 38., 49., 100., 1230.."
        self.assertEqual(alpha2digit(source, "de", ordinal_threshold=0), expected)

        source = "zwei tausend zweite"
        expected = "2002."
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "zweitausendzweite"
        expected = "2002."
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "der zweiundzwanzigste erste zweitausendzweiundzwanzig"
        expected = "der 22. 1. 2022"
        self.assertEqual(alpha2digit(source, "de", ordinal_threshold=0), expected)

        source = "der zwei und zwanzigste erste zwei tausend zwei und zwanzig"
        expected = "der 22. 1. 2022"
        self.assertEqual(alpha2digit(source, "de", ordinal_threshold=0), expected)

        source = "zweiundzwanzigster zweiter und zwei und zwanzigster zweiter"
        expected = "zweiundzwanzigster zweiter und zwei und zwanzigster zweiter"
        self.assertEqual(alpha2digit(source, "de", ordinal_threshold=22), expected)
        source = "zweiundzwanzigster zweiter und zwei und zwanzigster zweiter"
        expected = "22. 2. und 22. 2."
        self.assertEqual(alpha2digit(source, "de", ordinal_threshold=1), expected)

        source = "das erste lustigste hundertste dreißigste beste"
        expected = "das 1. lustigste 100. 30. beste"
        self.assertEqual(alpha2digit(source, "de", ordinal_threshold=0), expected)

        source = "zwanzig erste Versuche"
        expected = "20 erste Versuche"
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "der dritte und dreißig"
        expected = "der 3. und 30"
        self.assertEqual(alpha2digit(source, "de", ordinal_threshold=0), expected)

        source = "Es ist ein Buch mit dreitausend Seiten aber nicht das erste."
        expected = "Es ist ein Buch mit 3000 Seiten aber nicht das 1.."
        self.assertEqual(alpha2digit(source, "de", ordinal_threshold=0), expected)

    def test_alpha2digit_decimals(self):
        source = (
            "Die Testreihe ist zwölf komma neunundneunzig, zwölf komma neun, einhundertzwanzig komma null fünf,"
            " eins komma zwei drei sechs."
        )
        expected = "Die Testreihe ist 12 komma 99, 12,9, 120,05, 1,236."
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "null komma fünfzehn geht nicht, aber null komma eins fünf"
        expected = "0 komma 15 geht nicht, aber 0,15"
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "Pi ist drei Komma eins vier und so weiter"
        expected = "Pi ist 3,14 und so weiter"
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "komma eins vier"
        expected = "komma 1 4"
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "drei komma"
        expected = "3 komma"
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "eins komma erste geht, aber nur mit threshold null"
        expected = "1,1 geht, aber nur mit threshold 0"
        self.assertEqual(alpha2digit(source, "de", ordinal_threshold=0), expected)

    def test_alpha2digit_signed(self):
        source = "Es ist drinnen plus zwanzig Grad und draußen minus fünfzehn Grad."
        expected = "Es ist drinnen +20 Grad und draußen -15 Grad."
        self.assertEqual(alpha2digit(source, "de"), expected)

    def test_one_as_noun_or_article(self):
        source = "Ich nehme eins. Eins passt nicht!"
        expected = "Ich nehme 1. 1 passt nicht!"    # TODO: this is ambiguous - acceptable?
        self.assertEqual(alpha2digit(source, "de"), expected)
        source = "Velma hat eine Spur"
        self.assertEqual(alpha2digit(source, "de"), source)
        source = "Er sieht eine Zwei"
        expected = "Er sieht eine 2"
        self.assertEqual(alpha2digit(source, "de"), expected)
        source = "Ich suche ein Buch"
        self.assertEqual(alpha2digit(source, "de"), source)
        source = "Er sieht es nicht ein"
        self.assertEqual(alpha2digit(source, "de"), source)
        source = "Eine Eins und eine Zwei"
        expected = "Eine 1 und eine 2"
        self.assertEqual(alpha2digit(source, "de"), expected)
        # TODO: fails:
        # source = "Ein Millionen Deal"
        # expected = "Ein 1000000 Deal"
        # self.assertEqual(alpha2digit(source, "de"), expected)

    def test_second_as_time_unit_vs_ordinal(self):
        # Not yet applicable to German language
        # source = "One second please! twenty second is parsed as twenty-second and is different from twenty seconds."
        # expected = "One second please! 22nd is parsed as 22nd and is different from 20 seconds."
        # self.assertEqual(alpha2digit(source, "de"), expected)
        return

    def test_uppercase(self):
        source = "FÜNFZEHN EINS ZEHN EINS"
        expected = "15 1 10 1"
        self.assertEqual(alpha2digit(source, "de"), expected)

    def test_ordinals_false_positives(self):
        source = "In zehnten Jahrzehnten. Und einmal mit den Vereinten."
        expected = "In 10. Jahrzehnten. Und einmal mit den Vereinten."
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "Dies ist eine Liste oder die Einkaufsliste."
        expected = source
        self.assertEqual(alpha2digit(source, "de"), expected)

    def test_hundred_addition(self):
        source = "Zahlen wie vierzig fünfhundert Tausend zweiundzwanzig hundert sind gut."
        expected = "Zahlen wie 40 500022 100 sind gut."
        self.assertEqual(alpha2digit(source, "de"), expected)

        source = "achtundachtzig sieben hundert, acht und achtzig siebenhundert, achtundachtzig sieben hundert, acht und achtzig sieben hundert"
        expected = "88 700, 88 700, 88 700, 88 700"
        self.assertEqual(alpha2digit(source, "de"), expected)
