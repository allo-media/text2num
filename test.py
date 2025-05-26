import text_to_num

class Token:
    def __init__(self, text):
        self.content = text

    def text(self):
        return self.content

    def nt_separated(self, _):
        return False


def tokenize(text):
    """Poor man's tokenizer."""
    return [Token(piece) for piece in text.split()]


text = "Vingt-cinq vaches, douze poulets et cent vingt-cinq kg de pommes de terre."

assert text_to_num.alpha2digit(text, "fr") == "25 vaches, 12 poulets et 125 kg de pommes de terre."
assert text_to_num.text2num("deux cent vingt-cinq", "fr") == 225
# raises ValueError
#text_to_num.text2num("trente et onze", "fr")

occurences = text_to_num.find_numbers(tokenize(text), "fr")
assert len(occurences) == 3
assert occurences[0].value == 25.0
assert occurences[0].start == 0
assert occurences[0].end == 1
assert occurences[1].value == 12.0
assert occurences[1].start == 2
assert occurences[1].end == 3
assert occurences[2].value == 125.0
assert occurences[2].start == 5
assert occurences[2].end == 7
assert occurences[2].text == "125"

print("all tests OK.")
