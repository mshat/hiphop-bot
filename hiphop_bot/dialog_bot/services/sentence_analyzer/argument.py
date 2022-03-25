from hiphop_bot.dialog_bot.models.data import ARTISTS, GENRES, GENDERS


class ArgumentError(Exception): pass
class ArtistArgumentError(ArgumentError): pass
class GenreArgumentError(ArgumentError): pass


class Argument:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'Argument: {self.value}'

    def __repr__(self):
        return self.__str__()


class NumArgument(Argument):
    def __init__(self, value: str):
        super().__init__(value)
        if not value.isdigit():
            raise ArgumentError('Wrong value type')


class StrArgument(Argument):
    def __init__(self, value: str):
        super().__init__(value)


class SexArgument(StrArgument):
    def __init__(self, value: str):
        super().__init__(value)
        if self.value not in GENDERS.values():
            raise ArtistArgumentError('This sex is not found ')


class ArtistArgument(StrArgument):
    def __init__(self, value: str):
        super().__init__(value)
        if self.value.lower() not in ARTISTS.values():
            raise ArtistArgumentError('This artist is not found ')


class GenreArgument(StrArgument):
    def __init__(self, value: str):
        super().__init__(value)
        if self.value.lower() not in GENRES.values():
            raise GenreArgumentError('This genre is not found ')
