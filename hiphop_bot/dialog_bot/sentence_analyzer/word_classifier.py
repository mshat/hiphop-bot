from typing import List
from hiphop_bot.dialog_bot.sentence_analyzer.keywords import KEYWORDS
from hiphop_bot.dialog_bot.query_solving.query_solver import DialogState


class WordClassifier:
    def __init__(self):
        self._keywords = KEYWORDS

    @property
    def keywords(self):
        return {alias: keyword for keyword in self._keywords.keys() for alias in self._keywords[keyword]}

    def _exclude_keywords_by_query_type(self, excluded_query_types: List[str]):
        return {keyword.keyword: keyword for keyword in self._keywords if
                keyword.query_type not in excluded_query_types}

    def _get_keywords_by_dialog_state(self, dialog_state):
        if dialog_state == DialogState.search:
            return self._exclude_keywords_by_query_type(['search', 'info', 'like', 'dislike', 'number'])
        else:
            return self._exclude_keywords_by_query_type(['filter'])

    def assign_tags(self, word: str):
        # keywords = self._get_keywords_by_dialog_state(dialog_state)
        if word not in self.keywords:
            return None
        return self.keywords[word]


WORD_CLASSIFIER = WordClassifier()
