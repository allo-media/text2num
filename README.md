# text2num

A fast and robust text2num converter library a library for recognizing, parsing and transcribing into digits (base 10) numbers expressed in natural language. It works on strings as well as on custom token lists.

No IA involved: it is low on resources (and energy!) consumption as the latency are very small.

[![Documentation status](https://readthedocs.org/projects/text2num/badge/?version=latest)](https://text2num.readthedocs.io/en/latest/?badge=latest)

`text2num` is a python package that provides functions and parser classes for:

- Parsing of numbers expressed as natural language words convert them to integer values.
- Detection of ordinal, cardinal and decimal numbers in a stream of natural language words and get their decimal digit representations.

Supported natural languages (in alphabetical order):

* Dutch;
* English;
* French;
* German;
* Italian;
* European and Brazilian Portuguese;
* and Spanish.

## Versions 3.X vs 2.X

This new generation of `text2num` relies on a [new and improved algorithm implemented in Rust](https://crates.io/crates/text2num) whereas the 2.X branch
is in pure python and uses a less capable algorithm and has now been retired.

**You don't need Rust to install and run text2num!** as we provide precompiled wheels.

### Backward incompatible changes:

- dropped support for signed number — the feature was broken anyway;
- parsing mode is relaxed by default (i.e. "_greedy_") — you can use punctuation (e.g. commas) to separate groups in text, or voice pause if processing Speech-to-Text token streams;
- the `threshold` optional parameter to `alpha2digits` now applies to both ordinals and cardinals.
  As a consequence the signature of `alpha2digits` has changed.
- the Russian and Catalan languages have not been ported yet.


## Installation

We provide pre-compiled wheels for Linux, MacOS and Windows and for python 3.8 up to and including 3.13.

So all you need to do is this:

```
pip install text2num
# or, if using an `uv` project:
uv add text2num
```

## Quickstart

No every supported language is covered in these examples, here, but it gives you an idea.

### Parse and convert

French examples:

```python

    >>> from text_to_num import text2num
    >>> text2num('quatre-vingt-quinze', "fr")
    95

    >>> text2num('nonante-cinq', "fr")
    95

    >>> text2num('mille neuf cent quatre-vingt dix-neuf', "fr")
    1999

    >>> text2num('dix-neuf cent quatre-vingt dix-neuf', "fr")
    1999

    >>> text2num("cinquante et un million cinq cent soixante dix-huit mille trois cent deux", "fr")
    51578302

    >>> text2num('mille mille deux cents', "fr")
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for text2num: 'mille mille deux cents'

```

English examples:

```python

    >>> from text_to_num import text2num

    >>> text2num("fifty-one million five hundred seventy-eight thousand three hundred two", "en")
    51578302

    >>> text2num("eighty-one", "en")
    81

```

Spanish examples:

```python

    >>> from text_to_num import text2num
    >>> text2num("ochenta y uno", "es")
    81

    >>> text2num("nueve mil novecientos noventa y nueve", "es")
    9999

    >>> text2num("cincuenta y tres millones doscientos cuarenta y tres mil setecientos veinticuatro", "es")
    53243724

```

Portuguese examples:

```python

    >>> from text_to_num import text2num
    >>> text2num("trinta e dois", "pt")
    32

    >>> text2num("mil novecentos e seis", "pt")
    1906

    >>> text2num("vinte e quatro milhões duzentos mil quarenta e sete", "pt")
    24200047

```

German examples:

```python

    >>> from text_to_num import text2num

    >>> text2num("einundfünfzigmillionenfünfhundertachtundsiebzigtausenddreihundertzwei", "de")
    51578302

    >>> text2num("ein und achtzig", "de")
    81

```

### Find and transcribe

Any numbers, even ordinals.

French:

```python

    >>> from text_to_num import alpha2digit
    >>> sentence = (
    ...     "Huit cent quarante-deux pommes, vingt-cinq chiens, mille trois chevaux, "
    ...     "douze mille six cent quatre-vingt-dix-huit clous.\n"
    ...     "Quatre-vingt-quinze vaut nonante-cinq. On tolère l'absence de tirets avant les unités : "
    ...     "soixante seize vaut septante six.\n"
    ...     "Nombres en série : douze, quinze, zéro zéro quatre, vingt, cinquante-deux, cent trois, cinquante deux, "
    ...     "trente et un.\n"
    ...     "Ordinaux: cinquième troisième vingt et unième centième mille deux cent trentième.\n"
    ...     "Décimaux: douze virgule quatre-vingt dix-neuf, cent vingt virgule zéro cinq ; "
    ...     "mais soixante zéro deux."
    ... )
    >>> print(alpha2digit(sentence, "fr"))
    842 pommes, 25 chiens, 1003 chevaux, 12698 clous.
    95 vaut 95. On tolère l'absence de tirets avant les unités : 76 vaut 76.
    Nombres en série : 12, 15, 004, 20, 52, 103, 52, 31.
    Ordinaux: 5ème 3ème 21ème 100ème 1230ème.
    Décimaux: 12,99, 120,05 ; mais 60 02.

    >>> sentence = "Cinquième premier deuxième troisième vingt et unième centième mille deux cent trentième."
    >>> print(alpha2digit(sentence, "fr"))
    5ème 1er 2ème 3ème 21ème 100ème 1230ème.

```

English:

```python

    >>> from text_to_num import alpha2digit

    >>> text = "On May twenty-third, I bought twenty-five cows, twelve chickens and one hundred twenty five point four zero kg of potatoes."
    >>> alpha2digit(text, "en")
    'On May 23rd, I bought 25 cows, 12 chickens and 125.40 kg of potatoes.'

    >>> alpha2digit("I finished the race in the twelfth position!", "en")
    'I finished the race in the 12th position!'

```

Spanish:

```python

    >>> from text_to_num import alpha2digit

    >>> text = "Compramos veinticinco vacas, doce gallinas y ciento veinticinco coma cuarenta kg de patatas."
    >>> alpha2digit(text, "es")
    'Compramos 25 vacas, 12 gallinas y 125,40 kg de patatas.'

    >>> text = "Compramos veinticinco vacas, doce gallinas y ciento veinticinco punto cuarenta kg de patatas."
    >>> alpha2digit(text, "es")
    'Compramos 25 vacas, 12 gallinas y 125.40 kg de patatas.'

    >>> text = "Ella ha quedado tercera"
    >>> alpha2digit(text, "es", threshold=0)
    'Ella ha quedado 3ª'

```

Portuguese:

```python

    >>> from text_to_num import alpha2digit

    >>> text = "Comprámos vinte e cinco vacas, doze galinhas e cento e vinte e cinco vírgula quarenta kg de batatas."
    >>> alpha2digit(text, "pt")
    'Comprámos 25 vacas, 12 galinhas e 125,40 kg de batatas.'

    >>> text = "Ordinais: quinto, terceiro, vigésima, vigésimo primeiro, centésimo quarto"
    >>> alpha2digit(text, "pt")
    'Ordinais: 5º, 3º, 20ª, 21º, 104º'

```

German:

```python

    >>> from text_to_num import alpha2digit

    >>> text = "Ich habe fünfundzwanzig Kühe, zwölf Hühner und einhundertfünfundzwanzig kg Kartoffeln gekauft."
    >>> alpha2digit(text, "de")
    'Ich habe 25 Kühe, 12 Hühner und 125 kg Kartoffeln gekauft.'

    >>> text = "Die Telefonnummer lautet dreiunddreißig neun sechzig null sechs zwölf einundzwanzig."
    >>> alpha2digit(text, "de")
    'Die Telefonnummer lautet 33 9 60 06 12 21.'

    >>> text = "Der zweiundzwanzigste Januar zweitausendzweiundzwanzig."
    >>> alpha2digit(text, "de")
    'Der 22. Januar 2022.'

    >>> text = "Es ist ein Buch mit dreitausend Seiten aber nicht das erste."
    >>> alpha2digit(text, "de", threshold=0)
    'Es ist 1 Buch mit 3000 Seiten aber nicht das 1..'

    >>> text = "Pi ist drei Komma eins vier und so weiter, aber nicht drei Komma vierzehn :-p"
    >>> alpha2digit(text, "de", threshold=0)
    'Pi ist 3,14 und so weiter, aber nicht 3 Komma 14 :-p'

```

Read the complete documentation on `ReadTheDocs <http://text2num.readthedocs.io/>`.

## Contribute

Join us on https://github.com/allo-media/text2num
