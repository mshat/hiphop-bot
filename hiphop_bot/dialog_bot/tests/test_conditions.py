import unittest
from unittest.mock import Mock
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (AndTagCondition, OrTagCondition,
                                                                         AndMultiTagCondition)
from hiphop_bot.dialog_bot.services.query_handling.pattern_matcher import PatternMatcher


class TestTagSimpleCondition(unittest.TestCase):
    tags = {'search': ''}

    def test_tag_condition_pos(self):
        condition = AndTagCondition('search')

        res = condition.solve(self.tags)[0]

        self.assertTrue(res)

    def test_tag_condition_neg(self):
        condition = AndTagCondition('artist')

        res = condition.solve(self.tags)[0]

        self.assertFalse(res)


class TestQueryPatternWithSimpleConditions(unittest.TestCase):
    query_mock = Mock(query_tag_structure={'search': ''}, arguments={'ArtistArgument': ''})

    def test_one_AND_condition(self):
        condition = AndTagCondition('search')
        pattern_matcher = PatternMatcher(conditions=[condition])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertTrue(res)

    def test_one_OR_condition(self):
        condition = OrTagCondition('search')
        pattern_matcher = PatternMatcher(conditions=[condition])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertTrue(res)

    def test_two_AND_conditions_pos(self):
        condition1 = AndTagCondition('search')
        condition2 = AndTagCondition('artist')
        self.query_mock.query_tag_structure = {'search': '', 'artist': ''}
        pattern_matcher = PatternMatcher(conditions=[condition1, condition2])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertTrue(res)

    def test_two_AND_conditions_neg_no_tag_artist_in_query(self):
        """ Паттерн не подойдёт, тк условие 2 будет ложным (в запросе нет тэга artist)"""
        condition1 = AndTagCondition('search')
        condition2 = AndTagCondition('artist')
        self.query_mock.query_tag_structure = {'search': ''}
        pattern_matcher = PatternMatcher(conditions=[condition1, condition2])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertFalse(res)

    def test_two_AND_conditions_neg_empty_query(self):
        """ Паттерн не подойдёт, тк тэгов search и artist нет в структуре запроса"""
        condition1 = AndTagCondition('search')
        condition2 = AndTagCondition('artist')
        self.query_mock.query_tag_structure = {}
        pattern_matcher = PatternMatcher(conditions=[condition1, condition2])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertFalse(res)

    def test_AND_and_OR_conditions_pos(self):
        """ Паттерн подойдёт, несмотря на то, что условие 2 будет ложным. Так как условие 2 - ИЛИ"""
        condition1 = AndTagCondition('search')
        condition2 = OrTagCondition('artist')
        self.query_mock.query_tag_structure = {'search': ''}
        pattern_matcher = PatternMatcher(conditions=[condition1, condition2])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertTrue(res)

    def test_two_OR_conditions_pos(self):
        """ Паттерн подойдёт, несмотря на то, что условие 2 будет ложным. Так как оба условия - ИЛИ"""
        condition1 = OrTagCondition('search')
        condition2 = OrTagCondition('artist')
        self.query_mock.query_tag_structure = {'search': ''}
        pattern_matcher = PatternMatcher(conditions=[condition1, condition2])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertTrue(res)

    def test_two_OR_conditions_neg(self):
        """ Паттерн не подойдёт, тк тэгов search и artist нет в структуре запроса"""
        condition1 = OrTagCondition('search')
        condition2 = OrTagCondition('artist')
        self.query_mock.query_tag_structure = {}
        pattern_matcher = PatternMatcher(conditions=[condition1, condition2])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertFalse(res)


class TestQueryPatternWithMultiConditions(unittest.TestCase):
    query_mock = Mock(query_tag_structure={'search': '', 'artist': ''}, arguments={'ArtistArgument': ''})

    def test_one_multicondition_pos(self):
        condition1 = AndTagCondition('search')
        condition2 = AndTagCondition('artist')
        multicondition = AndMultiTagCondition(conditions=[condition1, condition2])
        pattern_matcher = PatternMatcher(conditions=[multicondition])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertTrue(res)

    def test_one_multicondition_neg(self):
        condition1 = AndTagCondition('search')
        condition2 = AndTagCondition('genre')
        multicondition = AndMultiTagCondition(conditions=[condition1, condition2])
        pattern_matcher = PatternMatcher(conditions=[multicondition])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertFalse(res)

    def test_two_AND_multiconditions_pos(self):
        condition1 = AndTagCondition('search')
        condition2 = AndTagCondition('artist')
        multicondition1 = AndMultiTagCondition(conditions=[condition1, condition2])
        multicondition2 = AndMultiTagCondition(conditions=[condition1, condition2])

        self.query_mock.query_tag_structure = {'search': '', 'artist': ''}
        pattern_matcher = PatternMatcher(conditions=[multicondition1, multicondition2])

        res = pattern_matcher.match_pattern(self.query_mock.query_tag_structure)[0]

        self.assertTrue(res)
