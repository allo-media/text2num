import re

from .parsers import WordStreamValueParser, WordToDigitParser


def look_ahead(sequence):
    """Look-ahead iterator"""
    maxi = len(sequence) - 1
    for i, val in enumerate(sequence):
        ahead = sequence[i + 1] if i < maxi else None
        yield val, ahead


def text2num(text, relaxed=False):
    """Convert the ``text`` string containing an integer number written in french
    into an integer value.

    Set ``relaxed`` to True if you want to accept "quatre vingt(s)" as "quatre-vingt".

    Raises an AssertionError if ``text`` does not describe a valid number.
    Return an int.
    """

    num_parser = WordStreamValueParser(relaxed=relaxed)
    tokens = text.split()
    assert all(num_parser.push(word, ahead) for word, ahead in look_ahead(tokens))
    return num_parser.value


def alpha2digit(text, relaxed=False):
    """Return the text of ``text`` with all the french spelled numbers converted to digits.
    Takes care of punctuation.
    Set ``relaxed`` to True if you want to accept "quatre vingt(s)" as "quatre-vingt".
    """
    segments = re.split(r'\s*[\.,;\(\)…\[\]:!\?]+\s*', text)
    punct = re.findall(r'\s*[\.,;\(\)…\[\]:!\?]+\s*', text)
    if len(punct) < len(segments):
        punct.append('')
    out_segments = []
    for segment, sep in zip(segments, punct):
        tokens = segment.split()
        num_builder = WordToDigitParser(relaxed=relaxed)
        in_number = False
        out_tokens = []
        for word, ahead in look_ahead(tokens):
            if num_builder.push(word.lower(), ahead):
                in_number = True
            elif in_number:
                out_tokens.append(num_builder.value)
                num_builder = WordToDigitParser(relaxed=relaxed)
                in_number = num_builder.push(word.lower(), ahead)
            if not in_number:
                out_tokens.append(word)
        # End of segment
        num_builder.close()
        if num_builder.value:
            out_tokens.append(num_builder.value)
        out_segments.append(' '.join(out_tokens))
        out_segments.append(sep)
    return ''.join(out_segments)


if __name__ == '__main__':

    test1 = "cinquante trois mille millions deux cent quarante trois mille sept cent vingt quatre"
    assert text2num(test1) == 53_000_243_724

    test2 = "cinquante et un million cinq cent soixante dix-huit mille trois cent deux"
    assert text2num(test2) == 51_578_302

    test3 = "quatre-vingt un"
    assert text2num(test3) == 81

    #
    sentence = (
        "Huit cent quarante-deux pommes, vingt-cinq chiens, mille trois chevaux, "
        "douze mille six cent quatre-vingt-dix-huit clous.\n"
        "Quatre-vingt-quinze vaut nonante-cinq. On tolère l'absence de tirets avant les unités : "
        "soixante seize vaut septante six.\n"
        "Nombres en série : douze quinze zéro zéro quatre vingt cinquante-deux cent trois cinquante deux "
        "trente et un.\n"
        "Ordinaux: cinquième troisième vingt et unième centième mille deux cent trentième.\n"
        "Décimaux: douze virgule quatre-vingt dix-neuf, cent vingt virgule zéro cinq ; "
        "mais soixante zéro deux."
    )

    print(sentence)
    print()
    print(alpha2digit(sentence))
