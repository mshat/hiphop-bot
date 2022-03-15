from typing import List
from enum import Enum
from hiphop_bot.dialog_bot.services.query_handling.handlers import filtration as filter_handlers
from hiphop_bot.dialog_bot.services.query_handling.handlers import search as search_handlers
from hiphop_bot.dialog_bot.services.query_handling.handlers import restart as restart_handlers
from hiphop_bot.dialog_bot.services.query_handling.handlers import like_dislike as like_dislike_handlers
from hiphop_bot.dialog_bot.services.query_handling.handlers import number_question as number_question_handlers
from hiphop_bot.dialog_bot.services.query_handling.handlers import info as info_handlers
from hiphop_bot.dialog_bot.services.query_handling.handlers import settings as settings_handlers
from hiphop_bot.dialog_bot.services.query_handling.handlers import genres as genres_handlers
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.tools.debug_print import debug_print, error_print
from hiphop_bot.dialog_bot.config import DEBUG_QUERY_HANDLER, DEBUG_QUERY_HANDLER_PATTERN_MATCHING


class QuerySolvingState(Enum):
    SOLVED = 1
    UNSOLVED = 2


class QuerySolver:
    dialog: Dialog

    def __init__(self, user: User):
        self.dialog = Dialog()
        self._user = user

    @property
    def state(self):
        return self.dialog.state

    @state.setter
    def state(self, val):
        self.dialog.state = val
        if val == DialogState.START:
            self.dialog.reset_search_result()

        # Если по запросу поиска ничего не было найдено, состояние диалога сбрасыватся до START, тк фильтровать нечего
        if val == DialogState.SEARCH and not self.dialog.search_result_found:
            self.dialog.state = DialogState.START
        debug_print(DEBUG_QUERY_HANDLER, f'[QUERY_HANDLER] new dialog state: {self.dialog.state}')

    @property
    def user(self):
        return self._user

    def match_patterns(self, handlers_: List[QueryHandler], query: Query) -> DialogState | None:
        for handler in handlers_:
            match_res = handler.match_pattern(query)

            debug_print(
                DEBUG_QUERY_HANDLER_PATTERN_MATCHING,
                f"MATCH_PATTERN {handler.debug_msg} [{str(handler.pattern).replace('  ', '')}] "
                f"TO [{query.raw_sentence}] RESULT {match_res}"
            )

            if match_res:
                next_state = handler.handle(query, self._user, self.dialog)
                handler.remove_used_keywords_and_args(query)
                return next_state
        return None

    def match_restart_patterns(self, query: Query) -> DialogState | None:
        restart_handler = restart_handlers.RestartHandler()
        return self.match_patterns([restart_handler], query)

    def match_like_dislike_patterns(self, query: Query) -> DialogState | None:
        handlers_ = [
            like_dislike_handlers.ExcludeDislikeHandler(),
            like_dislike_handlers.ExcludeLikeHandler(),
            like_dislike_handlers.LikeHandler(),
            like_dislike_handlers.DislikeHandler(),
        ]
        return self.match_patterns(handlers_, query)

    def match_number_query_patterns(self, query: Query) -> DialogState | None:
        handlers_ = [
            number_question_handlers.NumberWithSexHandler(),
            number_question_handlers.NumberWithAgeRangeHandler(),
            number_question_handlers.NumberWithAgeHandler(),
            number_question_handlers.NumberHandler(),
        ]
        return self.match_patterns(handlers_, query)

    def match_search_patterns(self, query: Query) -> DialogState | None:
        search_handler = search_handlers.SearchByArtistHandler()
        if search_handler.match_pattern(query):
            next_state = search_handler.handle(query, self._user, self.dialog)
            search_handler.remove_used_keywords_and_args(query)
            self.solve_multi_filters(query)
            return next_state

        handlers_ = [
            search_handlers.RecommendationHandler(),
            search_handlers.SearchBySexHandler(),
            search_handlers.SearchByAgeRangeHandler(),
            search_handlers.SearchByAgeHandler(),
            search_handlers.SearchByGenreHandler(),
            search_handlers.ShowAllArtistsHandler(),
            genres_handlers.ShowAllGenresHandler(),
        ]
        return self.match_patterns(handlers_, query)

    def match_info_patterns(self, query: Query) -> DialogState | None:
        handlers_ = [
            info_handlers.InfoHandler(),
            info_handlers.InfoAboutBotAlgorithmHandler(),
            info_handlers.InfoAboutBotHandler(),
            info_handlers.InfoAboutBotOpportunitiesHandler(),
        ]
        return self.match_patterns(handlers_, query)

    def match_filter_patterns(self, query: Query) -> DialogState | None:
        handlers_ = [
            filter_handlers.FilterBySexExcludeHandler(),
            filter_handlers.FilterBySexIncludeHandler(),
            filter_handlers.FilterByAgeRangeHandler(),
            filter_handlers.FilterByAgeExcludeHandler(),
            filter_handlers.FilterByAgeIncludeHandler(),
            filter_handlers.FilterByMembersCountHandler(),
            filter_handlers.FilterOutputLenHandler(),

            filter_handlers.RemoveResultLenFilterHandler(),
            filter_handlers.RemoveFiltersHandler(),
        ]
        return self.match_patterns(handlers_, query)

    def solve_multi_filters(self, query: Query) -> None:
        while True:
            next_state = self.match_filter_patterns(query)
            if next_state is None:
                break

    def solve(self, query: Query):
        # restart
        next_state = self.match_restart_patterns(query)
        if next_state:
            self.state = next_state
            return QuerySolvingState.SOLVED

        if self.state in (DialogState.FILTER, DialogState.SEARCH):
            # filters
            next_state = self.match_filter_patterns(query)
            if next_state:
                self.state = next_state
                return QuerySolvingState.SOLVED

        if self.state != DialogState.FILTER:
            # like / dislike,
            next_state = self.match_like_dislike_patterns(query)
            if next_state:
                self.state = next_state
                return QuerySolvingState.SOLVED

            # number query
            next_state = self.match_number_query_patterns(query)
            if next_state:
                self.state = next_state
                return QuerySolvingState.SOLVED

            # search
            next_state = self.match_search_patterns(query)
            if next_state:
                self.state = next_state
                return QuerySolvingState.SOLVED

            # set output len
            next_state = self.match_patterns([settings_handlers.SetOutputLenHandler()], query)
            if next_state:
                self.state = next_state
                return QuerySolvingState.SOLVED

            # info
            next_state = self.match_info_patterns(query)
            if next_state:
                self.state = next_state
                return QuerySolvingState.SOLVED

        error_print(f'[UNRECOGNIZED SENTENCE] {query.arguments} {query.keywords} {query.words}')
        return QuerySolvingState.UNSOLVED
