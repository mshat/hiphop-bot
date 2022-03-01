from hiphop_bot.dialog_bot.sentence_analyzer.sentence_parser import SentenceParser
from hiphop_bot.dialog_bot.query_solving.query_solver import QuerySolver, SOLVED, UNSOLVED
from hiphop_bot.dialog_bot.query_solving.user import User
from hiphop_bot.dialog_bot.query_solving.dialog import DialogState
from hiphop_bot.dialog_bot.config import DEBUG
from hiphop_bot.dialog_bot.data.const import LINE_LEN
from hiphop_bot.console_interface.view import ConsolePrinter


def main():
    user = User()
    query_solver = QuerySolver(user)
    console_printer = ConsolePrinter()
    print(f'{"="*LINE_LEN}\n'
          'Вас приветствует разговорный бот.\n'
          'Я кое-что знаю о русском хип-хопе и готов ответить на ваши вопросы по этой теме.\n'
          'Вы можете узнать о моих возможностях, спросив меня об этом.\n'
          f'{"=" * LINE_LEN}'
          )
    while True:
        if query_solver.state in (DialogState.search, DialogState.filter):
            input_prompt = 'ФИЛЬТР -> '
        else:
            input_prompt = 'ЗАПРОС -> '
        sentence = input(input_prompt)
        if sentence == '':
            print('Вы что-то хотели?..')
            continue
        query = SentenceParser(sentence).parse(query_solver.state)
        res = query_solver.solve(query)
        if res == SOLVED:
            console_printer.dialog = query_solver.dialog
            console_printer.user = query_solver.user
            console_printer.print()
        elif res == UNSOLVED:
            print('Я вас не понял :(')

        if DEBUG: print('[CURRENT STATE]', query_solver.state)
        print()


if __name__ == '__main__':
    main()
