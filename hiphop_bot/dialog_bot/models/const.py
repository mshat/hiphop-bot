import enum


class SexFilter(enum.Enum):
    ANY = 'anysex'
    FEMALE = 'female'
    MALE = 'male'


class GroupTypeFilter(enum.Enum):
    ANY = 'any'
    SOLO = 'solo'
    DUET = 'duet'
    GROUP = 'group'
