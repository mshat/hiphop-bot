from typing import Callable
from hiphop_bot.dialog_bot.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.config import SHOW_QUERY_PATTERNS, DEBUG
from hiphop_bot.dialog_bot.query_handling.query_pattern import QueryPattern

QUERY_PATTERN_STRINGS = []


def log_query_pattern_strings():
    with open('../query_pattern_strings.txt', 'w', encoding='utf-8') as f:
        for line in QUERY_PATTERN_STRINGS:
            f.write(f'{line}\n')


class QueryHandler:
    pattern: QueryPattern
    handle: Callable

    def __init__(self, pattern: QueryPattern, handle_func: Callable, debug_msg: str = '', debug_res: str = ''):
        self.pattern = pattern
        self.handle = handle_func
        self.debug_msg = debug_msg
        self.debug_res = debug_res

        self.used_keywords = []
        self.used_args = []

        QUERY_PATTERN_STRINGS.append(self.__str__())
        if SHOW_QUERY_PATTERNS:
            print(self.__str__())

    def match_pattern(self, query: Query):
        res, self.used_keywords, self.used_args = self.pattern.match(query)
        if res:
            if DEBUG:
                print(f'Запрос: {self.debug_msg}')
        return res

    def remove_used_keywords_and_args(self, query: Query):
        for word in self.used_keywords:
            query.remove_word(word)
        for arg in self.used_args:
            query.remove_argument(arg)

    def __str__(self):
        return f'Запрос: {self.debug_msg.ljust(46)} | Паттерн: {self.pattern}'