from janome.tokenizer import Tokenizer


def extract_nouns(text: str):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text)

    nouns = []
    for token in tokens:
        if token.part_of_speech.startswith("名詞,固有名詞"):
            nouns.append(token.surface)

    return nouns
