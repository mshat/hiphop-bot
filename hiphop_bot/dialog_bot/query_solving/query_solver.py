from typing import List, Tuple
from hiphop_bot.dialog_bot.query_handling import handlers
from hiphop_bot.dialog_bot.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.config import DEBUG, ENABLE_FILTERS
from hiphop_bot.dialog_bot.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.query_solving.user import User

SOLVED, UNSOLVED = 1, 2


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
        if val == DialogState.start:
            self.dialog.search_result = []
        if val in (DialogState.search, DialogState.filter) and not ENABLE_FILTERS:
            self.dialog.state = DialogState.start

    @property
    def user(self):
        return self._user

    def unknown(self, query: Query):
        if DEBUG:
            print(f'[UNRECOGNIZED SENTENCE] {query.arguments} {query.keywords} {query.words}')
        return UNSOLVED

    def match_patterns(self, handlers_: List[QueryHandler], query: Query) -> DialogState | None:
        for handler in handlers_:
            if handler.match_pattern(query):
                next_state = handler.handle(query, self._user, self.dialog)
                handler.remove_used_keywords_and_args(query)
                return next_state
        return None

    def match_restart_patterns(self, query: Query) -> DialogState | None:
        restart_handler = handlers.RestartHandler()
        return self.match_patterns([restart_handler], query)

    def match_like_dislike_patterns(self, query: Query) -> DialogState | None:
        like_dislike_handlers = [
            handlers.ExcludeDislikeHandler(),
            handlers.ExcludeLikeHandler(),
            handlers.LikeHandler(),
            handlers.DislikeHandler(),
        ]
        return self.match_patterns(like_dislike_handlers, query)

    def match_number_query_patterns(self, query: Query) -> DialogState | None:
        number_query_handlers = [
            handlers.NumberWithSexHandler(),
            handlers.NumberWithAgeRangeHandler(),
            handlers.NumberWithAgeHandler(),
            handlers.NumberHandler(),
        ]
        return self.match_patterns(number_query_handlers, query)

    def match_search_patterns(self, query: Query) -> DialogState | None:
        search_handler = handlers.SearchByArtistHandler()
        if search_handler.match_pattern(query):
            next_state = search_handler.handle(query, self._user, self.dialog)
            search_handler.remove_used_keywords_and_args(query)
            self.solve_multi_filters(query)
            return next_state

        search_handlers = [
            handlers.RecommendationHandler(),
            handlers.SearchBySexHandler(),
            handlers.SearchByAgeRangeHandler(),
            handlers.SearchByAgeHandler(),
            handlers.SearchByGenreHandler(),
            handlers.ShowAllArtistsHandler(),
            handlers.ShowAllGenresHandler(),
        ]
        return self.match_patterns(search_handlers, query)

    def match_info_patterns(self, query: Query) -> DialogState | None:
        info_handlers = [
            handlers.InfoHandler(),
            handlers.InfoAboutBotAlgorithmHandler(),
            handlers.InfoAboutBotHandler(),
            handlers.InfoAboutBotOpportunitiesHandler(),
        ]
        return self.match_patterns(info_handlers, query)

    def match_filter_patterns(self, query: Query) -> DialogState | None:
        filter_handlers = [
            handlers.FilterBySexExcludeHandler(),
            handlers.FilterBySexIncludeHandler(),
            handlers.FilterByAgeRangeHandler(),
            handlers.FilterByAgeExcludeHandler(),
            handlers.FilterByAgeIncludeHandler(),
            handlers.FilterByMembersCountHandler(),
            handlers.FilterOutputLenHandler(),
            handlers.RemoveFiltersHandler(),
            handlers.RemoveResultLenFilterHandler(),
        ]
        return self.match_patterns(filter_handlers, query)

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
            return SOLVED

        # filters
        if self.state in (DialogState.search, DialogState.filter):
            next_state = self.match_filter_patterns(query)
            if next_state:
                self.state = next_state
                return SOLVED
            else:
                self.state = DialogState.start

        # like/dislike, number query, search, info
        if self.state in (DialogState.start, DialogState.number, DialogState.like, DialogState.dislike, DialogState.info):
            next_state = self.match_like_dislike_patterns(query)
            if next_state:
                self.state = next_state
                return SOLVED

            next_state = self.match_number_query_patterns(query)
            if next_state:
                self.state = next_state
                return SOLVED

            next_state = self.match_search_patterns(query)
            if next_state:
                self.state = next_state
                return SOLVED

            # set output len
            next_state = self.match_patterns([handlers.SetOutputLenHandler()], query)
            if next_state:
                self.state = next_state
                return SOLVED

            next_state = self.match_info_patterns(query)
            if next_state:
                self.state = next_state
                return SOLVED

        return self.unknown(query)





