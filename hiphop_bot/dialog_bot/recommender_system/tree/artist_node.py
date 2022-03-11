from datetime import datetime
from hiphop_bot.dialog_bot.recommender_system.tree.visual_node import VisualNode
from hiphop_bot.dialog_bot.recommender_system.data.artists import ARTISTS, THEMES


class ArtistVisualNode(VisualNode):
    def __init__(self, genre, name, year_of_birth, group_members_num, theme, is_male=True, *args, **kwargs):
        self.genre = genre
        self.male_or_female = 1 if is_male else 0
        self.name = name
        self.theme = theme
        self.year_of_birth = year_of_birth
        self.group_members_number = group_members_num
        super().__init__(val=name, *args, **kwargs)

    @property
    def age(self):
        current_year = datetime.now().year
        return current_year - self.year_of_birth

    @property
    def sex(self):
        if self.male_or_female == 1:
            return 'male'
        return 'female'

    @property
    def solo_duet_group(self) -> str:  # категорийный
        if self.group_members_number == 1:
            return 'solo'
        if self.group_members_number == 2:
            return 'duet'
        if self.group_members_number > 2:
            return 'group'

        raise ValueError('Group_members_number must be > 0')

    @property
    def values_str(self):
        attributes = []
        attributes.append(self.genre.upper())
        male_female = 'male' if self.male_or_female == 1 else 'female'
        attributes.append(male_female)
        attributes.append(self.name)
        attributes.append(self.theme)
        attributes.append(str(self.year_of_birth))
        attributes.append(self.solo_duet_group)
        return ' '.join(attributes)

    @property
    def countable_attributes(self) -> dict:
        attributes = {}
        male_female = (self.male_or_female + 1) / 2
        attributes.update({'male_female': male_female})
        if self.name not in ARTISTS:
            print(self.name)
            print(ARTISTS)
        assert self.name in ARTISTS
        name = ARTISTS.index(self.name) / len(ARTISTS)
        attributes.update({'name': name})
        assert self.theme in THEMES
        theme = THEMES.index(self.theme) / len(THEMES)
        attributes.update({'theme': theme})
        year_of_birth = self.year_of_birth / 10000
        attributes.update({'year_of_birth': year_of_birth})
        if self.group_members_number > 2:
            solo_duet_group = 3
        else:
            solo_duet_group = self.group_members_number
        solo_duet_group = solo_duet_group / 3
        attributes.update({'solo_duet_group': solo_duet_group})
        return attributes
