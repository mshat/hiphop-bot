from typing import List
from hiphop_bot.recommender_system.models.artist import _Artist


def filter_artists(
        artists: List[_Artist],
        group_type: str = 'any',
        sex: str = 'anysex',
        younger: int = None,
        older: int = None) -> List[_Artist]:
    filtered = []
    for artist in artists:
        if artist.group_members_number == 1:
            solo_duet_group = 'solo'
        elif artist.group_members_number == 2:
            solo_duet_group = 'duet'
        else:
            solo_duet_group = 'group'
        if group_type != 'any' and solo_duet_group != group_type:
            continue

        if sex != 'anysex' and artist.gender != sex:
            continue
        if not (older is None) and artist.age < older:
            continue
        if not (younger is None) and artist.age > younger:
            continue
        if artist not in filtered:
            filtered.append(artist)
    return filtered
