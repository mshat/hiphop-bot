from hiphop_bot.dialog_bot.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.query_solving.user import User
from hiphop_bot.dialog_bot.recommender_system import filter
from hiphop_bot.dialog_bot.recommender_system import interface
from hiphop_bot.dialog_bot.config import DEBUG, ENABLE_FILTERS
from hiphop_bot.dialog_bot.data.const import LINE_LEN


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


def show_recommendations(user: User, dialog: Dialog):
    filtered = filter_search_result(user, dialog)
    if filtered:
        artists = filtered
    else:
        artists = dialog.search_result

    if artists:
        if user.dislikes:
            print(f'Список дизлайков: {", ".join(user.dislikes)}')
        if user.str_filters != '':
            print(f'Установлены фильтры: {user.str_filters}')

        interface.print_recommendations(artists, output_len=user.output_len, debug=DEBUG)

        if dialog.state in (DialogState.search, DialogState.filter):
            print_after_search_message()


def show_artists(user: User, dialog: Dialog):
    artists = dialog.output_artists
    if artists:
        interface.print_artists(artists, max_output_len=user.output_len, debug=DEBUG)


def show_genres(user: User, dialog: Dialog):
    messages = dialog.output_genres
    if messages:
        interface.print_messages(messages, max_output_len=user.output_len)


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
            show_recommendations(self.user, self.dialog)
            self.dialog.search_result = []
        if self.dialog.output_artists:
            show_artists(self.user, self.dialog)
            self.dialog.output_artists = []
        if self.dialog.output_genres:
            show_genres(self.user, self.dialog)
            self.dialog.output_genres = []
        if self.dialog.output_message:
            print(self.dialog.output_message)
            self.dialog.output_message = ''
