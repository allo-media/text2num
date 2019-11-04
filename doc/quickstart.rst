Quickstart
==========

Installation
------------

``text2num`` does not depend on any other third party package.

To install text2num in your (virtual) environment::

    pip install text2num

That's all folks!

Usage
-----

Parse and convert
~~~~~~~~~~~~~~~~~

Integers only.

.. code-block:: python

    >>> from text_to_num import text2num

    >>> text2num("fifty-one million five hundred seventy-eight thousand three hundred two", "en")
    51578302

    >>> text2num("eighty-one", "en")
    81

    >>> text2num('quatre-vingt-quinze')
    95

    >>> text2num('nonante-cinq')
    95

    >>> text2num('mille neuf cent quatre-vingt dix-neuf')
    1999

    >>> text2num('dix-neuf cent quatre-vingt dix-neuf')
    1999

    >>> text2num("cinquante et un million cinq cent soixante dix-huit mille trois cent deux")
    51578302

    >>> text2num('mille mille deux cents')
    ValueError: invalid literal for text2num: 'mille mille deux cent'


Find and transcribe
~~~~~~~~~~~~~~~~~~~

Any number, even ordinals.

.. code-block:: python

    >>> from text_to_num import alpha2digit

    >>> text = "On May twenty-third, I bought twenty-five cows, twelve chickens and one hundred twenty five point forty kg of potatoes."
    >>> alpha2digit(text, "en")
    'On May 23rd, I bought 25 cows, 12 chickens and 125.40 kg of potatoes.'


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

    >>> print(alpha2digit("on distingue aussi l'article (un chat) du nombre: un deux trois."))
    on distingue aussi l'article (un chat) du nombre: 1 2 3.

