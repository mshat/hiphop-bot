from hiphop_bot.dialog_bot.sentence_analyzer.sentence_parser import SentenceParser
from hiphop_bot.dialog_bot.query_solving.query_solver import QuerySolver
from hiphop_bot.dialog_bot.query_solving.user import User
from hiphop_bot.dialog_bot.query_solving.dialog import DialogState
from hiphop_bot.dialog_bot.config import DEBUG
from hiphop_bot.dialog_bot.data.const import LINE_LEN
from hiphop_bot.dialog_bot.query_handling.handlers import create_query_pattern_table

def test(sentences: [str]):
    user = User()
    query_solver = QuerySolver(user)
    for sentence_ in sentences:
        query_ = SentenceParser(sentence_).parse(query_solver.state)
        print(f'Вход: {query_.raw_sentence}')
        # print(query_.keywords)
        res_ = query_solver.solve(query_)
        # print(user)
        print(res_)
        print()


def main():
    create_query_pattern_table()
    user = User()
    query_solver = QuerySolver(user)
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
        query_solver.solve(query)
        if DEBUG: print('[CURRENT STATE]', query_solver.state)
        print()


if __name__ == '__main__':
    main()
