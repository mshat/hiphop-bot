from __future__ import annotations
from abc import ABC
from typing import List, Dict, Tuple
from hiphop_bot.dialog_bot.data.data import keywords
from hiphop_bot.dialog_bot.sentence_analyzer.word import Word


class PatternMatcher:  # TODO как-то вынести в отдельный модуль, разрешив циклический импорт
    def __init__(
            self,
            conditions: List[TagCondition, NotTagCondition, MultiTagCondition],
    ):
        self.conditions = conditions

    def match_pattern(self, query_tag_structure: dict) -> Tuple[bool, List[Word]]:
        match_res = None
        all_used_words = []

        for condition in self.conditions:
            res, used_words = condition.solve(query_tag_structure)
            if res:
                all_used_words += used_words
            if isinstance(condition, And):
                if match_res is None:
                    match_res = res
                else:
                    match_res *= res
            elif isinstance(condition, Or):
                if match_res is None:
                    match_res = res
                else:
                    match_res += res
            else:
                raise Exception('Unknown condition!')

        if match_res is None:
            match_res = True
        return match_res, all_used_words


class TagCondition(ABC):
    """
    Условие - составная часть паттерна запроса.
    Инициализируется тэгом, который должен быть найден в запросе, чтобы паттерн подошел к запросу
    """

    def __init__(self, tag: str):
        assert tag in keywords
        self.tag = tag

    def solve(self, query_tag_structure: Dict) -> Tuple[bool, List[Word]]:
        if self.tag in query_tag_structure:
            return True, query_tag_structure[self.tag]
        else:
            return False, []


class NotTagCondition(ABC):
    """
    Условие - составная часть паттерна запроса.
    Инициализируется тэгом, которого не должно быть в запросе, чтобы паттерн подошел к запросу
    """

    def __init__(self, tag: str):
        assert tag in keywords
        self.tag = tag

    def solve(self, query_tag_structure: Dict) -> Tuple[bool, List[Word]]:
        if self.tag not in query_tag_structure:
            return True, []
        else:
            return False, []


class And: pass


class Or: pass


class AndTagCondition(And, TagCondition):
    """
    Условие "И"
    Такое условие должно обязательно выполняться для запроса, чтобы паттерн подошел к нему
    """
    def __str__(self):
        return f'AND {self.tag}'

    def __repr__(self):
        return self.__str__()


class OrTagCondition(Or, TagCondition):
    """
    Условие "ИЛИ"
    Результат проверки такого условия будет учитываться как логическое СЛОЖЕНИЕ при сопоставлении паттерна с запросом
    """
    def __str__(self):
        return f'OR {self.tag}'

    def __repr__(self):
        return self.__str__()


class AndNotTagCondition(And, NotTagCondition):
    """
    Условие "И"
    Такое условие должно обязательно выполняться для запроса, чтобы паттерн подошел к нему
    """
    def __str__(self):
        return f'AND NOT {self.tag}'

    def __repr__(self):
        return self.__str__()


class OrNotTagCondition(Or, NotTagCondition):
    """
    Условие "ИЛИ"
    Результат проверки такого условия будет учитываться как логическое СЛОЖЕНИЕ при сопоставлении паттерна с запросом
    """
    def __str__(self):
        return f'OR NOT {self.tag}'

    def __repr__(self):
        return self.__str__()


class MultiTagCondition(ABC):
    """
    Составное условие - составная часть паттерна запроса.
    При инициализации получает объекты-условия.
    Результатом вызова метода solve будет результат вычисления условий self.conditions
    """

    def __init__(self, conditions: List[TagCondition | NotTagCondition | MultiTagCondition]):
        self.pattern_matcher = PatternMatcher(conditions)
        self.conditions = conditions

    def solve(self, query_tag_structure: Dict) -> Tuple[bool, List[Word]]:
        res = self.pattern_matcher.match_pattern(query_tag_structure)
        return res

    def __str__(self):
        conditions = ' '.join([str(condition) for condition in self.conditions])
        conditions_without_first_word = conditions.split()[1:]
        conditions = ' '.join(conditions_without_first_word)
        return conditions


class AndMultiTagCondition(And, MultiTagCondition):
    """
    Мультиусловиеусловие "И"
    Такое условие должно обязательно выполняться для запроса, чтобы паттерн подошел к нему
    """
    def __str__(self):
        conditions = super(AndMultiTagCondition, self).__str__()
        return f'AND ({conditions})'

    def __repr__(self):
        return self.__str__()


class OrMultiTagCondition(Or, MultiTagCondition):
    """
    Мультиусловие "ИЛИ"
    Результат проверки такого условия будет учитываться как логическое СЛОЖЕНИЕ при сопоставлении паттерна с запросом
    """
    def __str__(self):
        conditions = super(OrMultiTagCondition, self).__str__()
        return f'OR ({conditions})'

    def __repr__(self):
        return self.__str__()
