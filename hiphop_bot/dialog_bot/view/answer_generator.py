from typing import Iterable, List
from hiphop_bot.dialog_bot.config import DEBUG_QUERY_HANDLER
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.view.output_message import Output
from hiphop_bot.recommender_system.models.artist import _Artist  # Импортируется для аннотаций
from hiphop_bot.recommender_system.recommender_system import RecommenderSystem, RecommendedArtist


class AnswerGenerator:
    _dialog: Dialog
    _user: User

    @property
    def dialog(self):
        return self._dialog

    @dialog.setter
    def dialog(self, val: Dialog):
        assert isinstance(val, Dialog)
        self._dialog = val

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, val: User):
        assert isinstance(val, User)
        self._user = val

    def trunc_output(self, output: Iterable) -> List:
        output_len = self.user.max_output_len
        output = list(output)
        if output_len is None:
            output_len = 100000
        return output[:output_len]

    def _generate_info_message_str(self) -> str:
        if not self.dialog.info:
            return 'Я не смог найти ответ'
        else:
            return self.dialog.info

    def _generate_used_filters_str(self):
        out_msg = ''
        if self.user.dislikes:
            out_msg += f'Список дизлайков: {", ".join(self.user.dislikes)}\n'
        if self.user.str_filters != '':
            out_msg += f'Установлены фильтры: {self.user.str_filters}\n'
        return out_msg

    def _generate_artists_message(self, recommended_artists: List[_Artist]) -> str:
        out_msg = ''

        recommended_artists = self.trunc_output(recommended_artists)
        if recommended_artists:
            for artist in recommended_artists:
                spotify_link = artist.streaming_service_links.get_link_by_streaming_name('spotify')
                out_msg += f'\n{artist.name}\n{spotify_link}\n'
        return out_msg

    def _filter_search_result(self) -> List[_Artist]:
        recommender_system = RecommenderSystem()
        return recommender_system.filter_artists(
            self.dialog.found_artists,
            group_type=self.user.group_type_filter.value,
            sex=self.user.sex_filter.value,
            younger=self.user.younger_filter,
            older=self.user.older_filter,
        )

    def _generate_found_artists_str(self) -> str:
        found_artists = self.dialog.found_artists

        if self.user.has_filters:
            filtered_artists = self._filter_search_result()
            if filtered_artists:
                found_artists = filtered_artists
            else:
                return 'Не найдено результатов, подходящих под фильтры'

        res_str = self._generate_artists_message(found_artists)

        return res_str

    def _calc_proximity_percent(self, proximity: float):
        return round((1 - proximity) * 100)

    def _generate_found_artists_with_proximity_str(self) -> str:
        found_artists = self.dialog.found_artists_with_proximity

        if self.user.has_filters:
            return 'Активирован режим отображения proximity, фильтры сейчас не работают'

        out_msg = ''

        recommended_artists: List[RecommendedArtist] = self.trunc_output(found_artists)
        if recommended_artists:
            for artist in recommended_artists:
                proximities = artist.proximity.proximities
                proximities_percents = (f'gender: {self._calc_proximity_percent(proximities[0])}%\n'
                                        f'theme: {self._calc_proximity_percent(proximities[1])}%\n'
                                        f'year_of_birth: {self._calc_proximity_percent(proximities[2])}%\n'
                                        f'members_num: {self._calc_proximity_percent(proximities[3])}%\n'
                                        f'genre {self._calc_proximity_percent(proximities[4])}%')
                out_msg += (f'\n{artist.artist.name} '
                            f'{self._calc_proximity_percent(artist.proximity.general_proximity)}%\n'
                            f'{proximities_percents}\n')

        return out_msg

    def generate_answer(self) -> Output:
        output = Output()
        if DEBUG_QUERY_HANDLER and self.dialog.debug_message is not None:
            output.debug_msg += f'DEBUG {self.dialog.debug_message}'

        if self.dialog.found_artists is not None:
            output.filters = self._generate_used_filters_str()
            res_str = self._generate_found_artists_str()
            output.artists += res_str

        if self.dialog.found_artists_with_proximity is not None:
            output.filters = self._generate_used_filters_str()
            res_str = self._generate_found_artists_with_proximity_str()
            output.artists += res_str

        if self.dialog.info is not None:
            output.info += self._generate_info_message_str()

        self.dialog.reset()
        return output
