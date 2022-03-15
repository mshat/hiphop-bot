from typing import List, Dict
from abc import ABC, abstractmethod
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import TagCondition, NotTagCondition, MultiTagCondition
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.config import DEBUG_QUERY_HANDLER
from hiphop_bot.dialog_bot.services.tools.debug_print import debug_print
from hiphop_bot.dialog_bot.services.query_handling.query_pattern import QueryPattern
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState


class QueryHandler(ABC):
    conditions: List[TagCondition | NotTagCondition | MultiTagCondition]
    required_argument_type: str | None
    required_arguments: Dict[str, int] | None
    debug_msg: str

    @abstractmethod
    def __init__(self):
        self.conditions = []
        self.required_argument_type = None
        self.required_arguments = None
        self.debug_msg = ''

        self.used_keywords = []
        self.used_args = []

    @property
    def pattern(self):
        return QueryPattern(self.conditions, self.required_argument_type, self.required_arguments)

    @abstractmethod
    def handle(self, query: Query, user: User, dialog: Dialog) -> DialogState:
        pass

    def match_pattern(self, query: Query):
        res, self.used_keywords, self.used_args = self.pattern.match(query)
        if res:
            debug_print(DEBUG_QUERY_HANDLER, f'[QUERY_HANDLER] распознал запрос: {self.debug_msg}')
        return res

    def remove_used_keywords_and_args(self, query: Query):
        for word in self.used_keywords:
            query.remove_word(word)
        for arg in self.used_args:
            query.remove_argument(arg)

    def __str__(self):
        return f'Запрос: {self.debug_msg.ljust(46)} | Паттерн: {self.pattern}'
