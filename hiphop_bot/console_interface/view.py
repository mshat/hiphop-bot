from typing import Iterable, List
from hiphop_bot.dialog_bot.query_solving.dialog import Dialog
from hiphop_bot.dialog_bot.query_solving.user import User
from hiphop_bot.dialog_bot.recommender_system import filter
from hiphop_bot.dialog_bot.config import DEBUG, ENABLE_FILTERS
from hiphop_bot.dialog_bot.data.const import LINE_LEN


def trunc_output(output: Iterable, output_len=None) -> List:
    output = list(output)
    if output_len is None:
        output_len = 100000
    return output[:output_len]


def print_after_search_message():
    if ENABLE_FILTERS:
        print(f'{"="*LINE_LEN}\n'
              f'Вы находитесь в режиме ФИЛЬТРАЦИИ. Вы можете добавить фильтры к полученному результату поиска.\n'
              'Чтобы задать новый вопрос, скажите мне начать сначала\n'
              f'{"=" * LINE_LEN}'
              )


def filter_search_result(user: User, dialog: Dialog):
    if dialog.search_result:
        return filter.filter_recommendations(
            dialog.search_result,
            group_type=user.group_type_filter.value,
            sex=user.sex_filter.value,
            younger=user.younger_filter,
            older=user.older_filter,
        )


def print_recommendations(user: User, dialog: Dialog):
    filtered = filter_search_result(user, dialog)
    if filtered:
        recommended_artists = filtered
    else:
        recommended_artists = dialog.search_result

    if recommended_artists:
        if user.dislikes:
            print(f'Список дизлайков: {", ".join(user.dislikes)}')
        if user.str_filters != '':
            print(f'Установлены фильтры: {user.str_filters}')

        recommended_artists = trunc_output(recommended_artists, user.output_len)

        for artist_name in recommended_artists:
            if DEBUG:
                print(artist_name, recommended_artists[artist_name])
            else:
                print(artist_name)


def print_artists(user: User, dialog: Dialog):
    artists = dialog.output_artists
    artists = trunc_output(artists, user.output_len)
    if artists:
        for i, artist in enumerate(artists):
            if DEBUG:
                print(artist.name, artist.genre)
            else:
                print(artist.name)


def print_genres(user: User, dialog: Dialog):
    genres = dialog.output_genres
    genres = trunc_output(genres, user.output_len)
    if genres:
        for genre in genres:
            print(genre)


class ConsolePrinter:
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

    def print(self):
        if self.dialog.debug_message:
            print(f'DEBUG {self.dialog.debug_message}')
            self.dialog.debug_message = ''

        if self.dialog.search_result:
            print_recommendations(self.user, self.dialog)
            self.dialog.search_result = []
            print_after_search_message()

        if self.dialog.output_artists:
            print_artists(self.user, self.dialog)
            self.dialog.output_artists = []

        if self.dialog.output_genres:
            print_genres(self.user, self.dialog)
            self.dialog.output_genres = []

        if self.dialog.output_message:
            print(self.dialog.output_message)
            self.dialog.output_message = ''
