from typing import List, Tuple
from hiphop_bot.dialog_bot.query_handling import handlers
from hiphop_bot.dialog_bot.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.config import DEBUG, ENABLE_FILTERS
from hiphop_bot.dialog_bot.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.query_solving.user import User
import hiphop_bot.dialog_bot.query_handling.handling_functions as handling_functions


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

    def unknown(self, query: Query):
        print('Я не понял вопрос')
        if DEBUG:
            print(f'[UNRECOGNIZED SENTENCE] {query.arguments} {query.keywords} {query.words}')

    def match_patterns(self, handlers_: List[QueryHandler], query: Query, show=True) -> Tuple[DialogState, str | None]:
        for handler in handlers_:
            if handler.match_pattern(query):
                next_state = handler.handle(query, self._user, self.dialog, show)
                handler.remove_used_keywords_and_args(query)
                return next_state, handler.handle.__name__
        return self.state, None

    def match_restart_patterns(self, query: Query) -> Tuple[DialogState, str | None]:
        restart_handler = handlers.restart_handler
        return self.match_patterns([restart_handler], query)

    def match_like_dislike_patterns(self, query: Query) -> Tuple[DialogState, str | None]:
        like_dislike_handlers = [
            handlers.exclude_dislike_handler,
            handlers.exclude_like_handler,
            handlers.like_handler,
            handlers.dislike_handler
        ]
        return self.match_patterns(like_dislike_handlers, query)

    def match_number_query_patterns(self, query: Query) -> Tuple[DialogState, str | None]:
        number_query_handlers = [
            handlers.number_with_sex_handler,
            handlers.number_with_age_range_handler,
            handlers.number_with_age_handler,
            handlers.number_handler,
        ]
        return self.match_patterns(number_query_handlers, query)

    def match_search_patterns(self, query: Query) -> Tuple[DialogState, str | None]:
        search_handler = handlers.search_by_artist_handler
        if search_handler.match_pattern(query):
            next_state = search_handler.handle(query, self._user, self.dialog)
            search_handler.remove_used_keywords_and_args(query)
            self.solve_multi_filters(query)
            handling_functions.show_recommendations(self._user, self.dialog)
            return next_state, search_handler.handle.__name__

        search_handlers = [
            handlers.recommendation_handler,
            handlers.search_by_sex_handler,
            handlers.search_by_age_range_handler,
            handlers.search_by_age_handler,
            handlers.search_by_genre_handler,
            handlers.show_all_artists_handler,
            handlers.show_all_genres_handler,
        ]
        return self.match_patterns(search_handlers, query)

    def match_info_patterns(self, query: Query) -> Tuple[DialogState, str | None]:
        info_handlers = [
            handlers.info_handler,
            handlers.info_about_bot_algorithm_handler,
            handlers.info_about_bot_handler,
            handlers.info_about_bot_opportunities_handler,
        ]
        return self.match_patterns(info_handlers, query)

    def match_filter_patterns(self, query: Query, show=True) -> Tuple[DialogState, str | None]:
        filter_handlers = [
            handlers.filter_by_sex_exclude_handler,
            handlers.filter_by_sex_include_handler,
            handlers.filter_by_age_range_handler,
            handlers.filter_by_age_exclude_handler,
            handlers.filter_by_age_include_handler,
            handlers.filter_by_members_count_handler,
            handlers.filter_output_len_handler,
            handlers.remove_filters_handler,
            handlers.remove_result_len_filter_handler,
        ]
        return self.match_patterns(filter_handlers, query, show=show)

    def solve_multi_filters(self, query: Query) -> None:
        while True:
            next_state, debug_res = self.match_filter_patterns(query, show=False)
            if debug_res is None:
                break

    def solve(self, query: Query):
        # restart
        next_state, debug_res = self.match_restart_patterns(query)
        if debug_res:
            self.state = next_state
            return debug_res

        # filters
        if self.state in (DialogState.search, DialogState.filter):
            next_state, debug_res = self.match_filter_patterns(query)
            if debug_res:
                self.state = next_state
                return debug_res
            else:
                self.state = DialogState.start

        # like/dislike, number query, search, info
        if self.state in (DialogState.start, DialogState.number, DialogState.like, DialogState.dislike, DialogState.info):
            next_state, debug_res = self.match_like_dislike_patterns(query)
            if debug_res:
                self.state = next_state
                return debug_res

            next_state, debug_res = self.match_number_query_patterns(query)
            if debug_res:
                self.state = next_state
                return debug_res

            next_state, debug_res = self.match_search_patterns(query)
            if debug_res:
                self.state = next_state
                return debug_res

            # set output len
            next_state, debug_res = self.match_patterns([handlers.set_output_len_handler], query)
            if debug_res:
                self.state = next_state
                return debug_res

            next_state, debug_res = self.match_info_patterns(query)
            if debug_res:
                self.state = next_state
                return debug_res

        self.unknown(query)





