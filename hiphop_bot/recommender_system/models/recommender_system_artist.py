from typing import List
from hiphop_bot.recommender_system.models.artist import _Artist  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.theme import ThemeModel

THEMES = ThemeModel().get_theme_names()


class RecommenderSystemArtist:
    """
    Класс артиста для рекомендательной системы. Поля класса _Artist пересчитываются в числовые значения
    """
    def __init__(self, artist: _Artist):
        self._artist = artist

    @property
    def artist(self) -> _Artist:
        return self._artist

    @property
    def name(self) -> str:
        return self._artist.name

    @property
    def year_of_birth(self) -> int:
        return self._artist.year_of_birth

    @property
    def group_members_number(self) -> int:
        return self._artist.group_members_number

    @property
    def themes(self) -> List[str]:
        return [theme.name for theme in self._artist.themes]

    @property
    def gender(self) -> str:
        return self._artist.gender

    @property
    def genres(self) -> List[str]:
        return [genre.name for genre in self._artist.genres]

    @property
    def age(self) -> int:
        return self._artist.age

    @property
    def solo_duet_group(self) -> str:
        if self.group_members_number == 1:
            return 'solo'
        if self.group_members_number == 2:
            return 'duet'
        if self.group_members_number > 2:
            return 'group'

        raise ValueError('Group_members_number must be > 0')

    @property
    def values_str(self) -> str:
        attributes = []
        attributes.append(self.genres)
        male_female = self.gender
        attributes.append(male_female)
        attributes.append(self.name)
        attributes.append(self.themes)
        attributes.append(str(self.year_of_birth))
        attributes.append(self.solo_duet_group)
        return ' '.join(attributes)

    @property
    def countable_gender(self) -> int:
        return 1 if self.gender == 'male' else 2

    @property
    def countable_themes(self) -> List[float]:
        return [THEMES.index(theme) for theme in self.themes]

    def __str__(self):
        return f'RecommenderSystemArtist: {self._artist.__str__()}'

    def __repr__(self):
        return self.__str__()