from abc import ABC
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.config import DEBUG_QUERY_HANDLER
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (AndTagCondition as And,
                                                                         OrTagCondition as Or,
                                                                         AndNotTagCondition as AndNot,
                                                                         AndMultiTagCondition as AndMulti,
                                                                         OrMultiTagCondition as OrMulti)
from hiphop_bot.dialog_bot.services.query_handling.handling_tools import get_arguments_by_type


class SearchQueryHandler(QueryHandler, ABC):
    NEXT_STATE = DialogState.SEARCH


class SearchBySexHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('artist'), Or('recommend'), Or('show')]
        self.required_argument_type = 'SexArgument'
        self.debug_msg = 'Вывести исполнителей указанного пола'

    def handle(self, query: Query, user: User, dialog: Dialog):
        sex = get_arguments_by_type(query, 'SexArgument')[0]
        artists = self._recommender_system.get_all_artists()
        artists = self._recommender_system.filter_artists(artists, sex=sex.value.value)
        dialog.found_artists = artists
        return DialogState.SEARCH


class SearchByAgeRangeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [
            AndMulti([Or('artist'), Or('recommend'), Or('show')]),
            AndMulti([Or('range'), OrMulti([And('older'), And('younger')])])
        ]
        self.required_arguments = {'NumArgument': 2}
        self.debug_msg = 'Вывести исполнителей в диапазоне возраста'

    def handle(self, query: Query, user: User, dialog: Dialog):
        age = get_arguments_by_type(query, 'NumArgument')
        if len(age) >= 2:
            from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
            dialog.debug_message = f'артисты в возрасте от {from_age} до {to_age} лет'

            artists = self._recommender_system.get_all_artists()
            artists = self._recommender_system.filter_artists(artists, older=from_age, younger=to_age)
            dialog.found_artists = artists
        else:
            return DialogState.START
        return DialogState.SEARCH


class SearchByAgeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [
            AndMulti([Or('artist'), Or('recommend'), Or('show')]),
            AndMulti([Or('older'), Or('younger')])
        ]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Вывести исполнителей в указанном возрасте'

    def handle(self, query: Query, user: User, dialog: Dialog):
        age = get_arguments_by_type(query, 'NumArgument')[0]
        age = int(age.value)

        artists = self._recommender_system.get_all_artists()

        if 'younger' in query.query_tag_structure:
            dialog.debug_message = f'фильтр до {age} лет'
            artists = self._recommender_system.filter_artists(artists, younger=age)
        elif 'older' in query.query_tag_structure:
            dialog.debug_message = f'фильтр от {age} лет'
            artists = self._recommender_system.filter_artists(artists, older=age)

        dialog.found_artists = artists
        return DialogState.SEARCH


class SearchByGenreHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('genre'), Or('recommend'), Or('show')]
        self.required_argument_type = 'GenreArgument'
        self.debug_msg = 'Вывести артистов в определённом жанре'

    def handle(self, query: Query, user: User, dialog: Dialog):
        genre = get_arguments_by_type(query, 'GenreArgument')[0]
        artists = self._recommender_system.get_artists_by_genre(genre.value)
        if artists:
            dialog.found_artists = artists
        else:
            dialog.info = 'Артистов в этом жанре нет в базе :('
        return DialogState.SEARCH


class SearchByArtistHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('search'), Or('like/how'), Or('recommend'), Or('show')]
        self.required_argument_type = 'ArtistArgument'
        self.debug_msg = 'Рекомендация по артисту'

    def handle(self, query: Query, user: User, dialog: Dialog):
        artist = get_arguments_by_type(query, 'ArtistArgument')[0]
        artists = self._recommender_system.recommend_by_seed(artist.value, disliked_artists=user.dislikes)
        dialog.found_artists = artists
        return DialogState.SEARCH


class RecommendationHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [
            OrMulti([
                AndMulti([Or('search'), Or('recommend'), Or('show'), Or('artist')]), AndMulti([Or('to me'), Or('like')])
            ]),
            OrMulti([And('to me'), And('like')])]
        self.debug_msg = 'Рекомендация по интересам'

    def handle(self, query: Query, user: User, dialog: Dialog):
        if len(user.likes) == 0:
            dialog.info = 'Я еще не знаю ваших предпочтений!\n' \
                                    'Чтобы поставить лайк или дизлайк, скажите что-нибудь вроде:\n' \
                                    'мне нравится нойз мс\n' \
                                    '(Можете перечислить сразу несколько артистов)'
            return DialogState.START
        dialog.found_artists = self._recommender_system.recommend_by_likes(
            user.likes, user.dislikes, DEBUG_QUERY_HANDLER
        )

        dialog.info = f'Список лайков: {", ".join(user.likes)}'
        return DialogState.SEARCH


class ShowAllArtistsHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [
            AndMulti([Or('all'), Or('like/how')]),
            AndNot('genre'),
            AndMulti([Or('include'), Or('artist'), Or('show')])
        ]
        self.debug_msg = 'Вывести всех артистов в базе'

    def handle(self, query: Query, user: User, dialog: Dialog):
        artists = self._recommender_system.get_all_artists()
        dialog.found_artists = artists
        by_the_way_msg = '\nКстати, в запросах вы можете указывать имя артиста или ' \
                         'группы на русском языке, даже если тут он записан на английском'
        if dialog.info:
            dialog.info += by_the_way_msg
        else:
            dialog.info = by_the_way_msg
        return DialogState.SEARCH
