import re
from typing import List, Dict, Union
from hiphop_bot.dialog_bot.services.sentence_analyzer.word import BaseWord, Placeholder, Word
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.services.sentence_analyzer.argument import (ArtistArgument, SexArgument, GenreArgument, NumArgument,
                                                                       ARTISTS, GENRES)
from hiphop_bot.dialog_bot.models.data import GENDERS
from hiphop_bot.dialog_bot.services.sentence_analyzer.word_parser import WordParser

PLACEHOLDERS = {'artist': '*ARTISTNAME*', 'genre': '*GENRENAME*', 'gender': '*GENDER*', 'number': '*NUMBER*'}


class SentenceParsingError(Exception): pass


class SentenceParser:
    def __init__(self, sentence: str):
        if sentence == "":
            raise SentenceParsingError('Empty input')
        sentence = sentence.lower()
        self._raw_sentence = sentence
        self._sentence = sentence
        self._clear_sentence()
        self._is_question = self._check_is_it_question()
        self._sentence = self._sentence.replace('?', '')

    def _clear_sentence(self):
        self._sentence = self._sentence.replace(',', '')
        self._sentence = self._sentence.replace('  ', ' ')

    def _check_is_it_question(self):
        return bool(self._sentence[-1] == '?')

    def find_arguments(self, possible_arguments: Dict, placeholder='') -> List[str]:
        """ Находит в предложении все вхождения ключей словаря possible_arguments и
        возвращает список соответствующих этим ключам значений словаря.
        Найденные ключевые слова заменяются на placeholder в исходном предложении"""
        possible_keys = list(possible_arguments.keys())
        found_args = re.findall('|'.join(possible_keys), self._sentence)
        arguments = []
        for arg in found_args:
            arguments.append(possible_arguments[arg])
            self._sentence = self._sentence.replace(arg, placeholder)
        return arguments

    def find_number_arguments(self, placeholder=''):
        words = self._sentence.split()
        arguments = []
        for word in words:
            if word.isdigit():
                arguments.append(word)
                self._sentence = self._sentence.replace(word, placeholder)
        return arguments

    def _split(self) -> List[str]:
        replace_to_space_chars = ['.', ',', '-', '  ']
        for char in replace_to_space_chars:
            self._sentence = self._sentence.replace(char, ' ')

        words = self._sentence.split()
        i = 0
        while i < len(words):
            if words[i] == 'не' and i < len(words) - 1:
                words[i + 1] = words[i] + ' ' + words[i + 1]
                words.pop(i)
            i += 1
        return words

    def parse(self) -> Query:
        artist_args = [ArtistArgument(arg) for arg in self.find_arguments(ARTISTS, PLACEHOLDERS['artist'])]
        genre_args = [GenreArgument(arg) for arg in self.find_arguments(GENRES, PLACEHOLDERS['genre'])]
        gender_args = [SexArgument(arg) for arg in self.find_arguments(GENDERS, PLACEHOLDERS['gender'])]
        number_args = [NumArgument(arg) for arg in self.find_number_arguments(PLACEHOLDERS['number'])]
        arguments = [*artist_args, *genre_args, *gender_args, *number_args]

        raw_words = self._split()

        parsed_words: List[Union[BaseWord, Word]] = []
        for word in raw_words:
            if word not in PLACEHOLDERS.values():
                word_parser = WordParser(word)
                parsed_words.append(word_parser.parse())
            else:
                parsed_words.append(Placeholder(word))
        return Query(
            raw_sentence=self._raw_sentence,
            words=parsed_words,
            arguments=arguments,
            is_question=self._is_question
        )
