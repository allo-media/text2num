text2num
========

|docs|


``text2num`` is a python package that provides functions and parser classes for:

- parsing numbers expressed as words in French, English and Spanish and convert them to integer values;
- detect ordinal, cardinal and decimal numbers in a stream of French, English or Spanish words and get their decimal digit representations. Spanish does not support ordinal numbers yet.

Compatibility
-------------

Tested on python 3.7. Requires Python >= 3.6.

License
-------

This sofware is distributed under the MIT license of which you should have received a copy (see LICENSE file in this repository).

Installation
------------

``text2num`` does not depend on any other third party package.

To install text2num in your (virtual) environment::

    pip install text2num

That's all folks!

Usage examples
--------------

Parse and convert
~~~~~~~~~~~~~~~~~


French examples:

.. code-block:: python

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
    ValueError: invalid literal for text2num: 'mille mille deux cent'


English examples:

.. code-block:: python

    >>> from text_to_num import text2num

    >>> text2num("fifty-one million five hundred seventy-eight thousand three hundred two", "en")
    51578302

    >>> text2num("eighty-one", "en")
    81

Spanish examples:

.. code-block:: python

    >>> from text_to_num import text2num
    >>> text2num("ochenta y uno", "es")
    81

    >>> text2num("nueve mil novecientos noventa y nueve", "es")
    9999

    >>> text2num("cincuenta y tres millones doscientos cuarenta y tres mil setecientos veinticuatro", "es")
    53243724


Find and transcribe
~~~~~~~~~~~~~~~~~~~

Any numbers, even ordinals.

French:

.. code-block:: python

    >>> from text_to_num import alpha2digit
    >>> sentence = (
    ...         "Huit cent quarante-deux pommes, vingt-cinq chiens, mille trois chevaux, "
    ...         "douze mille six cent quatre-vingt-dix-huit clous.\n"
    ...         "Quatre-vingt-quinze vaut nonante-cinq. On tolère l'absence de tirets avant les unités : "
    ...         "soixante seize vaut septante six.\n"
    ...         "Nombres en série : douze quinze zéro zéro quatre vingt cinquante-deux cent trois cinquante deux "
    ...         "trente et un.\n"
    ...         "Ordinaux: cinquième troisième vingt et unième centième mille deux cent trentième.\n"
    ...         "Décimaux: douze virgule quatre-vingt dix-neuf, cent vingt virgule zéro cinq ; "
    ...         "mais soixante zéro deux."
    ...     )
    >>> print(alpha2digit(sentence))
    842 pommes, 25 chiens, 1003 chevaux, 12698 clous.
    95 vaut 95. On tolère l'absence de tirets avant les unités : 76 vaut 76.
    Nombres en série : 12 15 004 20 52 103 52 31.
    Ordinaux: 5ème 3ème 21ème 100ème 1230ème.
    Décimaux: 12,99, 120,05 ; mais 60 02.


English:

.. code-block:: python

    >>> from text_to_num import alpha2digit

    >>> text = "On May twenty-third, I bought twenty-five cows, twelve chickens and one hundred twenty five point forty kg of potatoes."
    >>> alpha2digit(text, "en")
    'On May 23rd, I bought 25 cows, 12 chickens and 125.40 kg of potatoes.'


Spanish (ordinals not supported):

.. code-block:: python

    >>> from text_to_num import alpha2digit

    >>> text = "Compramos veinticinco vacas, doce gallinas y ciento veinticinco coma cuarenta kg de patatas."
    >>> alpha2digit(text, "es")
    'Compramos 25 vacas, 12 gallinas y 125.40 kg de patatas.'

    >>> text = "Tenemos mas veinte grados dentro y menos quince fuera."
    >>> alpha2digit(text, "es")
    'Tenemos +20 grados dentro y -15 fuera.'

Read the complete documentation on `ReadTheDocs <http://text2num.readthedocs.io/>`_.

Contribute
----------

Join us on https://github.com/allo-media/text2num


.. |docs| image:: https://readthedocs.org/projects/text2num/badge/?version=latest
    :target: https://text2num.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
