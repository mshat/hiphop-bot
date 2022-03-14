import pymorphy2

MorphAnalyzer = pymorphy2.MorphAnalyzer()

if __name__ == '__main__':
    word = 'сбрось'
    parsed_word = MorphAnalyzer.parse(word)[0]
    print(parsed_word)

