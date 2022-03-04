from typing import List, Tuple
from hiphop_bot.dialog_bot.sentence_analyzer.word import Word
from hiphop_bot.dialog_bot.query_handling.tag_condition import TagCondition, NotTagCondition, And, Or, MultiTagCondition


class PatternMatcher:
    def __init__(
            self,
            conditions: List[TagCondition | NotTagCondition | MultiTagCondition],
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
