import os
import telebot
from typing import Tuple, Dict
from hiphop_bot.dialog_bot.services.query_solving.query_solver import QuerySolvingState
from hiphop_bot.dialog_bot.view.answer_generator import AnswerGenerator
from hiphop_bot.dialog_bot.controller.controller import UserInterfaceController
from hiphop_bot.dialog_bot.models.tg_user import TelegramUserModel
from dotenv import dotenv_values

if 'MODE' in os.environ and os.environ['MODE'] == 'heroku':
    TG_TOKEN = os.environ['TG_TOKEN']
else:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ENV = dotenv_values(f"{current_dir}/../../../env")
    TG_TOKEN = ENV['TG_TOKEN']

bot = telebot.TeleBot(TG_TOKEN)
answer_generator = AnswerGenerator()
tg_user_model = TelegramUserModel()
user_interface_controllers: Dict[int, UserInterfaceController] = {}


def get_tg_user(from_user: telebot.types.User):
    # create new db record if user is new
    tg_user = tg_user_model.get_by_user_id(from_user.id)
    if not tg_user:
        tg_user_model.add_record(from_user.id, from_user.first_name, from_user.last_name, from_user.username)
    return tg_user


def get_controller(from_user: telebot.types.User) -> UserInterfaceController:
    tg_user = get_tg_user(from_user)
    if tg_user.user_id in user_interface_controllers:
        controller = user_interface_controllers[tg_user.user_id]
    else:
        controller = UserInterfaceController(tg_user.full_name)
        user_interface_controllers[tg_user.user_id] = controller
    return controller


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    controller = get_controller(message.from_user)

    print(f'[MESSAGE FROM {message.from_user.id}] {message.text}')

    if message.text == "/start":
        bot.send_message(message.from_user.id, start_answer(controller))
    elif message.text == '':
        bot.send_message(message.from_user.id, blank_answer(controller))
    else:
        reply, additional_message = solve_message(message.text, controller)  # additional_message - костыль
        if reply != '':
            bot.send_message(message.from_user.id, reply)
        if additional_message != '':
            bot.send_message(message.from_user.id, additional_message)


def start_answer(controller: UserInterfaceController):
    msg = controller.hello_message
    return msg


def blank_answer(controller: UserInterfaceController):
    msg = controller.blank_query_answer
    return msg


def solve_message(sentence: str, controller: UserInterfaceController) -> Tuple[str, str]:
    res = controller.solve_query(sentence)
    if res == QuerySolvingState.SOLVED:
        answer_generator.user = controller.user
        answer_generator.dialog = controller.dialog
        answer, additional_message = answer_generator.generate_answer()
        return answer, additional_message
    elif res == QuerySolvingState.UNSOLVED:
        print(f'[ANSWER] UNSOLVED')
        return controller.unresolved_answer, ''
    else:
        raise Exception('Unknown query_solver result')


bot.polling(none_stop=True, interval=0)
