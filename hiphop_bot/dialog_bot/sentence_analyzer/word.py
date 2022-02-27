from __future__ import annotations


class BaseWord:
    word: str

    def __init__(self, word: str):
        self.word = word

    def __str__(self):
        return f'{self.word}'


class Placeholder(BaseWord):
    def __str__(self):
        return 'Placeholder'

    def __repr__(self):
        return self.__str__()


class Word(BaseWord):
    word: str
    normal: str
    morph_speech_part: str
    tag: str

    def __init__(self, word: str, normal_word: str, morph_speech_part: str, tag: str):
        super().__init__(word)
        self.normal = normal_word
        self.morph_speech_part = morph_speech_part
        self.tag = tag

    def __str__(self):
        return f'{self.normal}[{self.tag} {self.morph_speech_part}]'

    def __repr__(self):
        return self.__str__()


