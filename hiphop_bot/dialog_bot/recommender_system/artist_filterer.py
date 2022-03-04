from typing import List
from collections import OrderedDict
from hiphop_bot.dialog_bot.recommender_system.tree.genre_node import GenreVisualNode
from hiphop_bot.dialog_bot.recommender_system.interface import find_artist

EXCLUDE = ['sex', 'group_type', 'older', 'younger']


def filter_artists(
        artists: List[str] | List[GenreVisualNode],
        group_type: str = 'any',
        sex: str = 'anysex',
        younger: int = None,
        older: int = None,
        exclude=None) -> List[GenreVisualNode]:
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


def parse_filters(values) -> dict:
    filters = {}
    for sex in ['_male_', '_female_', '_any_sex_']:
        if values[sex]:
            filters['sex'] = sex.replace('_', '')
            break

    for group_type in ['_solo_', '_duet_', '_group_', '_any_']:
        if values[group_type]:
            filters['group_type'] = group_type.replace('_', '')
            break

    filters['older'] = values['_older_']
    filters['younger'] = values['_younger_']

    return filters


def trunc_result(recommendations: OrderedDict, max_result_len: int):
    if max_result_len:
        limited_recommendations = OrderedDict()
        i = 0
        for key, val in recommendations.items():
            if i >= max_result_len:
                break
            i += 1
            limited_recommendations.update({key: val})
        return limited_recommendations