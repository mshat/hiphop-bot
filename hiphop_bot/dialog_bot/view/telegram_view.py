import telebot
from typing import List
from hiphop_bot.dialog_bot.view.base_view import View
from hiphop_bot.dialog_bot.models.tg_user import _TelegramUser  # Импортирутеся для аннотаций
from hiphop_bot.dialog_bot.models import const


class TelegramView(View):
    _bot: telebot.TeleBot
    _tg_user: _TelegramUser

    def __init__(self, bot: telebot.TeleBot, user: _TelegramUser):
        super().__init__()
        self._bot = bot
        self._tg_user = user

        self._hello_message = f'Здравствуйте, {self._tg_user.first_name}!\n' + self._hello_message

    def _send_message(self, msg: str):
        self._bot.send_message(self._tg_user.user_id, msg)

    def _send_markdown_message(self, msg: str):
        self._bot.send_message(self._tg_user.user_id, msg, parse_mode='MarkdownV2')

    def view_hello_message(self):
        self._send_message(self._hello_message)

    def view_blank_query_answer(self):
        self._send_message(self._blank_query_answer)

    def view_opportunities_message(self):
        msg = const.BOT_OPPORTUNITIES + "\nВы можете узнать о моих возможностях ещё раз позже, спросив меня об этом.\n"
        msg = self._escape_markdown_reserved_characters(msg)
        msg = self._bold_lines(msg, [1, 2, 3, 4, 5, -4])
        self._send_markdown_message(msg)

    def _bold_lines(self, msg: str, line_nums: List[int]) -> str:
        msg_lines = msg.split('\n')
        for line_num in line_nums:
            msg_lines[line_num] = f'*{msg_lines[line_num]}*'
        return '\n'.join(msg_lines)

    def _escape_markdown_reserved_characters(self, msg: str) -> str:
        markdown_reserved = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in markdown_reserved:
            msg = msg.replace(char, f'\{char}')
        return msg
