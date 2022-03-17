import telebot
from hiphop_bot.dialog_bot.view.base_view import View
from hiphop_bot.dialog_bot.models.tg_user import _TelegramUser  # Импортирутеся для аннотаций
from hiphop_bot.dialog_bot.models import const
from hiphop_bot.dialog_bot.view.markdown_formatter import MarkdownFormatter


class TelegramView(View):
    _bot: telebot.TeleBot
    _tg_user: _TelegramUser

    def __init__(self, bot: telebot.TeleBot, user: _TelegramUser):
        super().__init__()
        self._bot = bot
        self._tg_user = user
        self.md_formatter = MarkdownFormatter()

        self._hello_message = f'Здравствуйте, {self._tg_user.first_name}!\n' + self._hello_message

    def _send_message(self, msg: str, markdown=False):
        if markdown:
            self._bot.send_message(self._tg_user.user_id, msg, parse_mode='MarkdownV2')
        else:
            self._bot.send_message(self._tg_user.user_id, msg)

    def view_hello_message(self):
        self.md_formatter.raw_text = self._hello_message
        self.md_formatter.make_bold_lines([-3])
        self._send_message(self.md_formatter.formatted_text, markdown=True)

    def view_blank_query_answer(self):
        self._send_message(self._blank_query_answer)

    def view_opportunities_message(self):
        msg = const.BOT_OPPORTUNITIES + "\nВы можете узнать о моих возможностях ещё раз позже, спросив меня об этом.\n"
        self.md_formatter.raw_text = msg
        self.md_formatter.make_bold_lines([1, 2, 3, 4, 5, -4])
        self._send_message(self.md_formatter.formatted_text, markdown=True)
