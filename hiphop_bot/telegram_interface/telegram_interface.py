import telebot
from hiphop_bot.dialog_bot.query_solving.query_solver import QuerySolvingState
from hiphop_bot.base_user_interface.view import AnswerGenerator
from hiphop_bot.base_user_interface.user_interface import UserInterface
from hiphop_bot.dialog_bot.config import DEBUG


TOKEN = '5168804721:AAGBSsgGVMV5JQ258fnm6O6N96EXKwwkL3I'

bot = telebot.TeleBot(TOKEN)

interface = UserInterface()
answer_generator = AnswerGenerator()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(f'[USER MESSAGE] {message.text}')
    if DEBUG: print('[CURRENT STATE]', interface.state)

    if message.text == "/start":
        bot.send_message(message.from_user.id, start_answer())
    elif message.text == '':
        bot.send_message(message.from_user.id, blank_answer())
    else:
        reply = solve_message(message.text)
        if reply != '':
            bot.send_message(message.from_user.id, reply)


def start_answer():
    msg = interface.hello_message
    return msg


def blank_answer():
    msg = interface.blank_query_answer
    return msg


def solve_message(sentence: str) -> str:
    res = interface.solve_query(sentence)
    if res == QuerySolvingState.solved:
        answer_generator.user = interface.user
        answer_generator.dialog = interface.dialog
        return answer_generator.generate_answer()
    elif res == QuerySolvingState.unsolved:
        return interface.unresolved_answer
    else:
        raise Exception('Unknown query_solver result')


bot.polling(none_stop=True, interval=0)
