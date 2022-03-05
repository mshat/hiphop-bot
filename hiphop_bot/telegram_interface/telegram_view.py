import os
import telebot
from hiphop_bot.dialog_bot.query_solving.query_solver import QuerySolvingState
from hiphop_bot.controller.answer_generator import AnswerGenerator
from hiphop_bot.controller.controller import UserInterfaceController
from hiphop_bot.dialog_bot.config import DEBUG
from dotenv import dotenv_values

current_dir = os.path.dirname(os.path.realpath(__file__))
ENV = dotenv_values(f"{current_dir}/../env")

bot = telebot.TeleBot(ENV['TG_TOKEN'])

controller = UserInterfaceController()
answer_generator = AnswerGenerator()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(f'[USER MESSAGE] {message.text}')
    if DEBUG: print('[CURRENT STATE]', controller.state)

    if message.text == "/start":
        bot.send_message(message.from_user.id, start_answer())
    elif message.text == '':
        bot.send_message(message.from_user.id, blank_answer())
    else:
        reply = solve_message(message.text)
        if reply != '':
            bot.send_message(message.from_user.id, reply)


def start_answer():
    msg = controller.hello_message
    return msg


def blank_answer():
    msg = controller.blank_query_answer
    return msg


def solve_message(sentence: str) -> str:
    res = controller.solve_query(sentence)
    if res == QuerySolvingState.SOLVED:
        answer_generator.user = controller.user
        answer_generator.dialog = controller.dialog
        return answer_generator.generate_answer()
    elif res == QuerySolvingState.UNSOLVED:
        return controller.unresolved_answer
    else:
        raise Exception('Unknown query_solver result')


bot.polling(none_stop=True, interval=0)
