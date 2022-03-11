from typing import List
from hiphop_bot.dialog_bot.recommender_system.tree.artist_node import ArtistVisualNode
from hiphop_bot.dialog_bot.recommender_system.interface import find_artist

EXCLUDE = ['sex', 'group_type', 'older', 'younger']


def filter_artists(
        artists: List[str] | List[ArtistVisualNode],
        group_type: str = 'any',
        sex: str = 'anysex',
        younger: int = None,
        older: int = None,
        exclude=None) -> List[ArtistVisualNode]:
    exclude = exclude if exclude else []
    filtered = []
    for artist in artists:
        if isinstance(artist, str):
            artist = find_artist(artist)
        if group_type != 'any' and artist.solo_duet_group != group_type and 'group_type' not in exclude:
            continue
        if sex != 'anysex' and artist.sex != sex and 'sex' not in exclude:
            continue
        if not (older is None) and artist.age < older and 'older' not in exclude:
            continue
        if not (younger is None) and artist.age > younger and 'younger' not in exclude:
            continue
        if artist not in filtered:
            filtered.append(artist)
    return filtered
