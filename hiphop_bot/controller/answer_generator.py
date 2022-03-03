from typing import Iterable, List
from hiphop_bot.dialog_bot.recommender_system import filter
from hiphop_bot.dialog_bot.config import ENABLE_FILTERS
from hiphop_bot.dialog_bot.recommender_system.tree.genre_node import GenreVisualNode
from hiphop_bot.dialog_bot.query_solving.dialog import Dialog
from hiphop_bot.dialog_bot.query_solving.user import User
from hiphop_bot.dialog_bot.config import DEBUG
from hiphop_bot.controller.output_message import OutputMessage


def trunc_output(output: Iterable, output_len=None) -> List:
    output = list(output)
    if output_len is None:
        output_len = 100000
    return output[:output_len]


def get_after_search_message():
    if ENABLE_FILTERS:
        msg = (f'Вы находитесь в режиме ФИЛЬТРАЦИИ. Вы можете добавить фильтры к полученному результату поиска.\n'
               'Чтобы задать новый вопрос, скажите мне начать сначала\n'
               )
        return msg
    return ''


def filter_search_result(user: User, dialog: Dialog) -> List[GenreVisualNode]:
    if dialog.search_result:
        return filter.filter_artists(
            dialog.search_result,
            group_type=user.group_type_filter.value,
            sex=user.sex_filter.value,
            younger=user.younger_filter,
            older=user.older_filter,
        )


def generate_used_filters_str(user: User):
    out_msg = ''
    if user.dislikes:
        out_msg += f'Список дизлайков: {", ".join(user.dislikes)}\n'
    if user.str_filters != '':
        out_msg += f'Установлены фильтры: {user.str_filters}\n'
    return out_msg


def generate_recommendations_message(user: User, recommended_artists: List[GenreVisualNode]) -> str:
    out_msg = ''

    recommended_artists = trunc_output(recommended_artists, user.output_len)
    if recommended_artists:
        out_msg += generate_used_filters_str(user)

        for artist in recommended_artists:
            out_msg += f'{artist.name}\n'
    return out_msg


def generate_genres_message(user: User, dialog: Dialog) -> str:
    out_msg = ''
    genres = dialog.output_genres
    genres = trunc_output(genres, user.output_len)
    if genres:
        for genre in genres:
            out_msg += f'{genre}\n'
    return out_msg


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

    def generate_answer(self) -> str:
        out_msg = OutputMessage()
        if DEBUG and self.dialog.debug_message is not None:
            out_msg.msg += f'DEBUG {self.dialog.debug_message}'

        if self.dialog.output_genres is not None:
            if not self.dialog.output_genres:
                out_msg.msg += 'Ничего не найдено'
            else:
                out_msg.msg += generate_genres_message(self.user, self.dialog)

        if self.dialog.output_message is not None:
            if not self.dialog.output_message:
                out_msg.msg += 'Я не смог найти ответ'
            else:
                out_msg.msg += self.dialog.output_message

        if self.dialog.search_result is not None:
            if not self.dialog.search_result:
                out_msg.msg += 'Ничего не найдено'
            else:
                filtered = filter_search_result(self.user, self.dialog)
                if filtered:
                    out_msg.msg += generate_recommendations_message(self.user, filtered)
                    out_msg.msg += get_after_search_message()
                else:
                    out_msg.msg += 'Не найдено результатов, подходящих под фильтры'

        self.dialog.reset_output()

        if len(out_msg.msg) > 1 and out_msg.msg[-1] == '\n':
            out_msg.msg = out_msg.msg[:-1]

        return out_msg.msg