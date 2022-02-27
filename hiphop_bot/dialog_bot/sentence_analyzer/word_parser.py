from hiphop_bot.dialog_bot.sentence_analyzer.morph_analyzer import MorphAnalyzer
from hiphop_bot.dialog_bot.sentence_analyzer.word import Word
from hiphop_bot.dialog_bot.sentence_analyzer.word_classifier import WORD_CLASSIFIER


class WordParsingError(Exception): pass


class WordParser:
    _tag: str

    def __init__(self, word: str):
        if word == '':
            raise WordParsingError('Empty input')
        self._word = word

    def parse(self, dialog_state) -> Word:
        parsed_word = MorphAnalyzer.parse(self._word)[0]  # TODO не обязательно первый вариант правильный
        return Word(
            word=self._word,
            normal_word=parsed_word.normal_form,
            morph_speech_part=parsed_word.tag.POS,
            tag=WORD_CLASSIFIER.assign_tags(parsed_word.normal_form, dialog_state),
        )