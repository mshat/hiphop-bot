from hiphop_bot.recommender_system.tree.node import Node
from hiphop_bot.recommender_system.models.artist import _Artist  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.artist import ArtistModel
from hiphop_bot.recommender_system.models.theme import ThemeModel

THEMES = ThemeModel().get_theme_names()
ARTISTS = ArtistModel().get_artist_names()


class ArtistNode(Node):
    def __init__(self, artist: _Artist):
        self._artist = artist
        super().__init__(val=self._artist.name)

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
    def theme(self) -> str:
        return self._artist.theme

    @property
    def gender(self) -> str:
        return self._artist.gender

    @property
    def genre(self) -> str:
        return self._artist.genre

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
        attributes.append(self.genre.upper())
        male_female = self.gender
        attributes.append(male_female)
        attributes.append(self.name)
        attributes.append(self.theme)
        attributes.append(str(self.year_of_birth))
        attributes.append(self.solo_duet_group)
        return ' '.join(attributes)

    @property
    def countable_attributes(self) -> dict:
        attributes = {}
        male_female = 1 if self.gender == 'male' else 2
        attributes.update({'male_female': male_female})
        assert self.theme in THEMES
        theme = THEMES.index(self.theme)
        attributes.update({'theme': theme})
        year_of_birth = self.year_of_birth
        attributes.update({'year_of_birth': year_of_birth})
        attributes.update({'group_members_num': self.group_members_number})
        return attributes

    def __str__(self):
        return f'ArtistVisualNode: NodeVal={self.value} Artist={self._artist.__str__()}'

    def __repr__(self):
        return self.__str__()