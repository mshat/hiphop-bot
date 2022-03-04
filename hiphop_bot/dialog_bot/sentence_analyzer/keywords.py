from hiphop_bot.dialog_bot.data.data import keywords as raw_keywords

KEYWORDS = raw_keywords


class Keyword:
    def __init__(self, keyword: str, query_type, speech_part):
        self.keyword = keyword
        self.query_type = query_type
        self.speech_part = speech_part

    def __str__(self):
        return f'Keyword: {self.keyword} [{self.query_type} {self.speech_part}]'

    def __repr__(self):
        return self.__str__()


