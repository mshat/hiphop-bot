from typing import List
from hiphop_bot.recommender_system.tree.artist_node import ArtistNode


def filter_artists(
        artists: List[ArtistNode],
        group_type: str = 'any',
        sex: str = 'anysex',
        younger: int = None,
        older: int = None) -> List[ArtistNode]:
    filtered = []
    for artist in artists:
        if group_type != 'any' and artist.solo_duet_group != group_type:
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
