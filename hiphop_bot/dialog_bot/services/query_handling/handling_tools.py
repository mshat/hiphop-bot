from typing import List
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.services.sentence_analyzer.argument import (ArtistArgument, NumArgument, SexArgument,
                                                                       GenreArgument)


def get_arguments_by_type(query: Query, argument_type: str) \
        -> List[ArtistArgument | NumArgument | SexArgument | GenreArgument]:
    return [arg for type_, arguments in query.arguments.items() for arg in arguments if type_ == argument_type]




