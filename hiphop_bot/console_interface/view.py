from typing import Iterable, List
from hiphop_bot.dialog_bot.query_solving.dialog import Dialog
from hiphop_bot.dialog_bot.query_solving.user import User
from hiphop_bot.dialog_bot.recommender_system import filter
from hiphop_bot.dialog_bot.config import DEBUG, ENABLE_FILTERS
from hiphop_bot.dialog_bot.data.const import LINE_LEN
from hiphop_bot.dialog_bot.recommender_system.tree.genre_node import GenreVisualNode


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


def filter_search_result(user: User, dialog: Dialog) -> List[GenreVisualNode]:
    if dialog.search_result:
        return filter.filter_artists(
            dialog.search_result,
            group_type=user.group_type_filter.value,
            sex=user.sex_filter.value,
            younger=user.younger_filter,
            older=user.older_filter,
        )


def print_used_filters(user: User):
    if user.dislikes:
        print(f'Список дизлайков: {", ".join(user.dislikes)}')
    if user.str_filters != '':
        print(f'Установлены фильтры: {user.str_filters}')


def print_artists(user: User, artists: List[GenreVisualNode]):
    artists = trunc_output(artists, user.output_len)
    if artists:
        print_used_filters(user)

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
        if DEBUG and self.dialog.debug_message is not None:
            print(f'DEBUG {self.dialog.debug_message}')

        if self.dialog.output_genres is not None:
            if not self.dialog.output_genres:
                print('Ничего не найдено')
            else:
                print_genres(self.user, self.dialog)

        if self.dialog.output_message is not None:
            if not self.dialog.output_message:
                print('Я не смог найти ответ')
            else:
                print(self.dialog.output_message)

        if self.dialog.search_result is not None:
            if not self.dialog.search_result:
                print('Ничего не найдено')
            else:
                filtered = filter_search_result(self.user, self.dialog)
                if filtered:
                    print_artists(self.user, filtered)
                    print_after_search_message()
                else:
                    print('Не найдено результатов, подходящих под фильтры')
                    return

        self.dialog.reset_output()