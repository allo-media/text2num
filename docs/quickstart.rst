Quickstart
==========

Installation
------------

``text2num`` is available as precompiled wheel for Linux, MacOS and Windows operating systems, and Python
versions 3.8 up to 3.13 (included).

To install text2num in your (virtual) environment::

    pip install text2num

Or if you manage your projects with `uv`::

    uv add text2num


That's all folks!

Usage
-----

by example.

Parse and convert
~~~~~~~~~~~~~~~~~

Integers only.

.. code-block:: python

    >>> from text_to_num import text2num

    >>> text2num("fifty-one million five hundred seventy-eight thousand three hundred two", "en")
    51578302

    >>> text2num("eighty-one", "en")
    81

    >>> text2num("ochenta y uno", "es")
    81

    >>> text2num("nueve mil novecientos noventa y nueve", "es")
    9999

    >>> text2num('quatre-vingt-quinze', "fr")
    95

    >>> text2num("cinquante et un million cinq cent soixante dix-huit mille trois cent deux", "fr")
    51578302

    >>> text2num('thousand thousand and two hundreds', 'en')
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for text2num: 'thousand thousand and two hundreds'


Find and transcribe
~~~~~~~~~~~~~~~~~~~

Any number, even ordinals.

.. code-block:: python

    >>> from text_to_num import alpha2digit

    >>> text = "On May twenty-third, I bought twenty-five cows, twelve chickens and one hundred twenty five point five kg of potatoes."
    >>> alpha2digit(text, "en")
    'On May 23rd, I bought 25 cows, 12 chickens and 125.5 kg of potatoes.'

    >>> alpha2digit("I finished the race in the twelfth position!", "en")
    'I finished the race in the 12th position!'

    Both 'coma' and 'punto' are supported for Spanish:

    >>> text = "Compramos veinticinco vacas, doce gallinas y ciento veinticinco coma cuarenta kg de patatas."
    >>> alpha2digit(text, "es")
    'Compramos 25 vacas, 12 gallinas y 125,40 kg de patatas.'

    >>> text = "Compramos veinticinco vacas, doce gallinas y ciento veinticinco punto cuarenta kg de patatas."
    >>> alpha2digit(text, "es")
    'Compramos 25 vacas, 12 gallinas y 125.40 kg de patatas.'

    >>> sentence = (
    ...         "Huit cent quarante-deux pommes, vingt-cinq chiens, mille trois chevaux, "
    ...         "douze mille six cent quatre-vingt-dix-huit clous.\n"
    ...         "Quatre-vingt-quinze vaut nonante-cinq. On tolère l'absence de tirets avant les unités : "
    ...         "soixante seize vaut septante six.\n"
    ...         "Nombres en série : douze, quinze, zéro zéro quatre, vingt, cinquante-deux, cent trois, cinquante deux, "
    ...         "trente et un.\n"
    ...         "Ordinaux: cinquième troisième vingt et unième centième mille deux cent trentième.\n"
    ...         "Décimaux: douze virgule quatre-vingt dix-neuf, cent vingt virgule zéro cinq ; "
    ...         "mais soixante zéro deux."
    ...     )
    >>> print(alpha2digit(sentence, "fr"))
    842 pommes, 25 chiens, 1003 chevaux, 12698 clous.
    95 vaut 95. On tolère l'absence de tirets avant les unités : 76 vaut 76.
    Nombres en série : 12, 15, 004, 20, 52, 103, 52, 31.
    Ordinaux: 5ème 3ème 21ème 100ème 1230ème.
    Décimaux: 12,99, 120,05 ; mais 60 02.

    >>> print(alpha2digit("on distingue aussi l'article (un chat) du nombre: un deux trois.", "fr"))
    on distingue aussi l'article (un chat) du nombre: 1 2 3.


Working with tokens
~~~~~~~~~~~~~~~~~~~

Imagine that we have an ASR application that returns a transcript as a list of tokens (text, start timestamp, end timestamp)
where the timestamps are intergers reprensenting milliseconds relative to the beginning of the speech.

.. code-block:: python

    from text_to_num import (Token, find_numbers)


    class DecodedWord(Token):
        def __init__(self, text, start, end):
            self._text = text
            self.start = start
            self.end = end

        def text(self):
            return self._text

        def nt_separated(self, previous):
            # we consider a voice gap of more that 100 ms as significant
            return self.start - previous.end > 100


    # Let's simulate ASR output

    stream = [
        DecodedWord("We", 0, 100),
        DecodedWord("have", 100, 200),
        DecodedWord("respectively", 200, 400),
        DecodedWord("twenty", 400, 500),
        DecodedWord("nine", 610, 700),
        DecodedWord("and", 700, 800),
        DecodedWord("thirty", 800, 900),
        DecodedWord("four", 950, 1000),
        DecodedWord("dollars", 1010, 1410)
    ]

    occurences = find_numbers(stream, "en")

    for num in occurences:
        print(f"found number {num.text} ({num.value}) at range [{num.start}, {num.end}] in the stream")


When executed, that code snippet prints::

    found number 20 (20.0) at range [3, 4] in the stream
    found number 9 (9.0) at range [4, 5] in the stream
    found number 34 (34.0) at range [6, 8] in the stream
