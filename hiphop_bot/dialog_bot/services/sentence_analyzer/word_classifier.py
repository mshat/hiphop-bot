from hiphop_bot.dialog_bot.services.sentence_analyzer.keywords import KEYWORDS


class WordClassifier:
    def __init__(self):
        self._keywords = KEYWORDS

    @property
    def keywords(self):
        return {alias: keyword for keyword, aliases in self._keywords.items() for alias in aliases}

    def assign_tags(self, word: str):
        if word not in self.keywords:
            return None
        return self.keywords[word]


WORD_CLASSIFIER = WordClassifier()
