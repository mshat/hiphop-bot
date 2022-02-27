import telebot
from hiphop_bot.dialog_bot.sentence_analyzer.sentence_parser import SentenceParser
from hiphop_bot.dialog_bot.query_solving.query_solver import QuerySolver
from hiphop_bot.dialog_bot.query_solving.user import User
from hiphop_bot.dialog_bot.query_solving.dialog import DialogState
from hiphop_bot.dialog_bot.config import DEBUG
from hiphop_bot.dialog_bot.data.const import LINE_LEN

TOKEN = '5168804721:AAGBSsgGVMV5JQ258fnm6O6N96EXKwwkL3I'

bot = telebot.TeleBot(TOKEN)

user = User()
query_solver = QuerySolver(user)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(f'[DEBUG] {message.text}')
    if message.text == "/start":
        msg = (f'{"=" * LINE_LEN}\n'
               'Вас приветствует разговорный бот.\n'
               'Я кое-что знаю о русском хип-хопе и готов ответить на ваши вопросы по этой теме.\n'
               'Вы можете узнать о моих возможностях, спросив меня об этом.\n'
               f'{"=" * LINE_LEN}'
               )
        bot.send_message(message.from_user.id, msg)
    elif message.text == '':
        bot.send_message(message.from_user.id, 'Вы что-то хотели?..')
    else:
        reply = solve_message(message.text + '\n')
        bot.send_message(message.from_user.id, reply)


def solve_message(sentence: str) -> str:
    query = SentenceParser(sentence).parse(query_solver.state)
    query_solver.solve(query)
    if DEBUG: print('[CURRENT STATE]', query_solver.state)
    return query_solver.dialog.query_result


bot.polling(none_stop=True, interval=0)
