from __future__ import annotations
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.services.query_handling.query_pattern import ALL
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (AndTagCondition as And)
from hiphop_bot.dialog_bot.services.query_handling.handling_tools import get_arguments_by_type


class ExcludeDislikeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('dislike'), And('exclude')]
        self.required_arguments = {'ArtistArgument': ALL}
        self.debug_msg = 'Лайк'

    def handle(self, query: Query, user: User, dialog: Dialog):
        liked_artists = get_arguments_by_type(query, 'ArtistArgument')
        liked_artists = [artist.value for artist in liked_artists]
        for artist in liked_artists:
            user.add_like(artist)
        dialog.output_message = f'Поставлен лайк: {", ".join(liked_artists)}'
        return DialogState.LIKE


class LikeHandler(ExcludeDislikeHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('like')]
        self.required_arguments = {'ArtistArgument': ALL}
        self.debug_msg = 'Лайк'


class ExcludeLikeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('like'), And('exclude')]
        self.required_arguments = {'ArtistArgument': ALL}
        self.debug_msg = 'Дизлайк'

    def handle(self, query: Query, user: User, dialog: Dialog):
        disliked_artists = get_arguments_by_type(query, 'ArtistArgument')
        disliked_artists = [artist.value for artist in disliked_artists]
        for artist in disliked_artists:
            user.add_dislike(artist)
        dialog.output_message = f'Поставлен дизлайк: {", ".join(disliked_artists)}'
        return DialogState.DISLIKE


class DislikeHandler(ExcludeLikeHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('dislike')]
        self.required_arguments = {'ArtistArgument': ALL}
        self.debug_msg = 'Дизлайк'