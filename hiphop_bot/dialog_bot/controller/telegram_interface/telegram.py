import os
import telebot
from typing import Dict
from dotenv import dotenv_values
from hiphop_bot.dialog_bot.services.query_solving.query_solver import QuerySolvingState
from hiphop_bot.dialog_bot.controller.controller import UserInterfaceController
from hiphop_bot.dialog_bot.models.tg_user import TelegramUserModel
from hiphop_bot.dialog_bot.view.telegram_view import TelegramView
from hiphop_bot.dialog_bot.models.tg_user import _TelegramUser  # Импортирутеся для аннотаций
from hiphop_bot.dialog_bot.models.user_query_history import UserQueryHistoryModel
from hiphop_bot.dialog_bot.services.tools.debug_print import debug_print
from hiphop_bot.dialog_bot.config import DEBUG_TG_INTERFACE


if 'MODE' in os.environ and os.environ['MODE'] == 'heroku':
    TG_TOKEN = os.environ['TG_TOKEN']
else:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ENV = dotenv_values(f"{current_dir}/../../../env")
    TG_TOKEN = ENV['TG_TOKEN']


class TgBot:
    bot = telebot.TeleBot(TG_TOKEN)
    tg_user_model = TelegramUserModel()
    user_interface_controllers: Dict[int, UserInterfaceController] = {}
    user_views: Dict[int, TelegramView] = {}
    user_query_history_model = UserQueryHistoryModel()

    def __init__(self):
        @self.bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            self._solve_message(message)

    def _solve_message(self, message: telebot.types.Message):
        tg_user = self._get_tg_user(message.from_user)
        user_controller = self._get_controller(tg_user)
        user_view = self._get_view(message.from_user)

        debug_print(
            DEBUG_TG_INTERFACE,
            f'[TG] Got message from {message.from_user.full_name} {message.from_user.id}: {message.text}'
        )

        if message.text == "/start":
            user_view.view_hello_message()
            user_view.view_opportunities_message()
            # добавление записи в историю запросов юзера
            self.user_query_history_model.add_record(tg_user, QuerySolvingState.SOLVED, message.text, None)
        elif message.text == '':
            user_view.view_blank_query_answer()
        else:
            query_solving_res = user_controller.solve_query(message.text)
            matched_handler_name = user_controller.dialog.matched_handler_name

            user_view.view(query_solving_res, user_controller.dialog, user_controller.user)

            if query_solving_res == QuerySolvingState.UNSOLVED:
                debug_print(
                    DEBUG_TG_INTERFACE,
                    f'[TG UNRESOLVED] Message from '
                    f'{message.from_user.full_name} {message.from_user.id} ({message.text}) was not recognized'
                )

            # добавление записи в историю запросов юзера
            self.user_query_history_model.add_record(tg_user, query_solving_res, message.text, matched_handler_name)

    def _get_tg_user(self, from_user: telebot.types.User) -> _TelegramUser:
        # create new db record if user is new
        tg_user = self.tg_user_model.get_by_user_id(from_user.id)
        if not tg_user:
            self.tg_user_model.add_record(from_user.id, from_user.first_name, from_user.last_name, from_user.username)
            tg_user = self.tg_user_model.get_by_user_id(from_user.id)
        return tg_user

    def _get_controller(self, tg_user: _TelegramUser) -> UserInterfaceController:
        if tg_user.user_id in self.user_interface_controllers:
            controller = self.user_interface_controllers[tg_user.user_id]
        else:
            controller = UserInterfaceController(tg_user.full_name)
            self.user_interface_controllers[tg_user.user_id] = controller
        return controller

    def _get_view(self, from_user: telebot.types.User) -> TelegramView:
        tg_user = self._get_tg_user(from_user)
        if tg_user.user_id in self.user_views:
            view = self.user_views[tg_user.user_id]
        else:
            view = TelegramView(self.bot, tg_user)
            self.user_views[tg_user.user_id] = view
        return view


if __name__ == '__main__':
    tg_bot = TgBot()
    tg_bot.bot.polling(none_stop=True, interval=0)


