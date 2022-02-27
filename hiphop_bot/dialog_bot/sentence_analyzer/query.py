from typing import List
from hiphop_bot.dialog_bot.sentence_analyzer.word import Word, Placeholder
from hiphop_bot.dialog_bot.sentence_analyzer.argument import Argument


class Query:
    _raw_sentence: str
    _words: List[Word]
    _arguments: List[Argument]
    is_question: bool

    def __init__(self, raw_sentence: str, words: List[Word], arguments: List[Argument] = None, is_question=True):
        self._raw_sentence = raw_sentence
        self._words = words
        self._arguments = [] if arguments is None else arguments
        self.is_question = is_question

    def remove_word(self, word: Word):
        if word in self._words:
            self._words.remove(word)
        # else:  # TODO вложенные мультиусловия пытаются несколько раз удалить одно и то же ключевое слово
        #     raise Exception('Попытка удалить слово, отсутствующее в self._words')

    def remove_argument(self, arg: Argument):
        self._arguments.remove(arg)

    @property
    def raw_sentence(self):
        return self._raw_sentence

    @property
    def keywords(self):
        return [word for word in self._words if isinstance(word, Placeholder) or word.tag]

    @property
    def words(self):
        return self._words

    @property
    def arguments(self) -> dict:
        arguments = {}
        for arg in self._arguments:
            key = type(arg).__name__
            if key not in arguments:
                arguments[key] = [arg]
            else:
                arguments[key].append(arg)
        return arguments

    @property
    def query_tag_structure(self) -> dict:
        query_structure = {}
        for keyword in self.keywords:
            if not isinstance(keyword, Placeholder):
                if keyword.tag not in query_structure:
                    query_structure[keyword.tag] = [keyword]
                else:
                    query_structure[keyword.tag].append(keyword)
        return query_structure

    def __str__(self):
        res = 'Предложение:\n' if not self.is_question else 'Вопросительное предложение:\n'
        res += f"\tRaw: {self._raw_sentence}\n"
        res += "\tParsed: "
        if len(self._words) > 30:
            res += f"cодержит {len(self.keywords)} ключевых слов"
        else:
            res += ' '.join([str(word) for word in self.keywords])
        res += f"\n\tArguments: {self._arguments}"
        return res