import telebot
from hiphop_bot.dialog_bot.sentence_analyzer.sentence_parser import SentenceParser
from hiphop_bot.dialog_bot.query_solving.query_solver import QuerySolver, SOLVED, UNSOLVED
from hiphop_bot.dialog_bot.query_solving.user import User
from hiphop_bot.dialog_bot.data.const import LINE_LEN
from hiphop_bot.telegram_interface.view import AnswerGenerator

TOKEN = '5168804721:AAGBSsgGVMV5JQ258fnm6O6N96EXKwwkL3I'

bot = telebot.TeleBot(TOKEN)

user = User()
query_solver = QuerySolver(user)
answer_generator = AnswerGenerator()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(f'[USER MESSAGE] {message.text}')
    if message.text == "/start":
        bot.send_message(message.from_user.id, start_answer())
    elif message.text == '':
        bot.send_message(message.from_user.id, blank_answer())
    else:
        reply = solve_message(message.text)
        if reply != '':
            bot.send_message(message.from_user.id, reply)


def start_answer():
    msg = (f'{"=" * LINE_LEN}\n'
           'Вас приветствует разговорный бот.\n'
           'Я кое-что знаю о русском хип-хопе и готов ответить на ваши вопросы по этой теме.\n'
           'Вы можете узнать о моих возможностях, спросив меня об этом.\n'
           f'{"=" * LINE_LEN}'
           )
    return msg


def blank_answer():
    msg = 'Вы что-то хотели?..'
    return msg


def solve_message(sentence: str) -> str:
    query = SentenceParser(sentence).parse(query_solver.state)
    res = query_solver.solve(query)

    if res == SOLVED:
        answer_generator.user = query_solver.user
        answer_generator.dialog = query_solver.dialog

        return answer_generator.generate_answer()
    elif res == UNSOLVED:
        return 'Я вас не понял :('
    else:
        raise Exception('Unknown query_solver result')

bot.polling(none_stop=True, interval=0)
