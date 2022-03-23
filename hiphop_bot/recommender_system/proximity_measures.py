from typing import Dict, List, Set
from hiphop_bot.recommender_system.pow_distance import calc_distance_in_pow
from hiphop_bot.recommender_system.models.recommender_system_artist import RecommenderSystemArtist
from hiphop_bot.recommender_system.tree.node import Node
from hiphop_bot.recommender_system.tree.tree_loader import load_genres_tree
from hiphop_bot.recommender_system.tree.tree_tools import calc_distance_between_nodes
from hiphop_bot.recommender_system.proximity import RawGeneralProximity


def calc_manhattan_measure(attribute1: float, attribute2: float):
    return calc_distance_in_pow(attribute1, attribute2, 1)


def calc_genre_tree_distance_measure(
        genres_tree: Node,
        genre1: str,
        genre2: str,
):
    genre_node1 = genres_tree.get_child_by_name(genres_tree, genre1)
    genre_node2 = genres_tree.get_child_by_name(genres_tree, genre2)
    return calc_distance_between_nodes(genres_tree, genre_node1, genre_node2)


def generalizing_proximity_measure(
        genres_tree: Node,
        artist1: RecommenderSystemArtist,
        artist2: RecommenderSystemArtist) -> RawGeneralProximity:
    attributes1 = artist1.countable_attributes
    attributes2 = artist2.countable_attributes
    gender_proximity = calc_manhattan_measure(attributes1['male_female'], attributes2['male_female'])
    theme_proximity = calc_manhattan_measure(attributes1['theme'], attributes2['theme'])
    year_of_birth_proximity = calc_manhattan_measure(attributes1['year_of_birth'], attributes2['year_of_birth'])
    members_num_proximity = calc_manhattan_measure(attributes1['group_members_num'], attributes2['group_members_num'])

    # TODO вычисление среднего из нескольких жанров
    tree_distance = calc_genre_tree_distance_measure(genres_tree, artist1.genre, artist2.genre)
    genre_proximity = tree_distance

    proximity = RawGeneralProximity(
        gender_proximity=gender_proximity,
        theme_proximity=theme_proximity,
        year_of_birth_proximity=year_of_birth_proximity,
        members_num_proximity=members_num_proximity,
        genre_proximity=genre_proximity
    )

    return proximity


def calc_generalizing_proximity_measure_for_all_leafs(artists: List[RecommenderSystemArtist]) \
        -> Dict[str, Dict[str, RawGeneralProximity]]:
    genres_tree = load_genres_tree()

    artists_pairs_proximity: Dict[str, Dict[str, RawGeneralProximity]] = {}
    gender_proximities: Set[float] = set()
    theme_proximities: Set[float] = set()
    year_of_birth_proximities: Set[float] = set()
    members_num_proximities: Set[float] = set()
    genre_proximities: Set[float] = set()
    for artist1 in artists:
        for artist2 in artists:
            if artist1 != artist2:
                proximity = generalizing_proximity_measure(genres_tree, artist1, artist2)
                gender_proximities.update((proximity.gender_proximity,))
                theme_proximities.update((proximity.theme_proximity,))
                year_of_birth_proximities.update((proximity.year_of_birth_proximity,))
                members_num_proximities.update((proximity.members_num_proximity,))
                genre_proximities.update((proximity.genre_proximity,))

                if artist1.name not in artists_pairs_proximity:
                    artists_pairs_proximity.update({artist1.name: {}})
                artists_pairs_proximity[artist1.name].update(
                    {artist2.name: proximity}
                )

    # нормализация значений
    min_gender_proximity = min(gender_proximities)
    max_gender_proximity = max(gender_proximities)
    min_theme_proximity = min(theme_proximities)
    max_theme_proximity = max(theme_proximities)
    min_members_num_proximity = min(members_num_proximities)
    max_members_num_proximity = max(members_num_proximities)
    min_year_of_birth_proximity = min(year_of_birth_proximities)
    max_year_of_birth_proximity = max(year_of_birth_proximities)
    min_genre_proximity = min(genre_proximities)
    max_genre_proximity = max(genre_proximities)

    for first_artist_name, pairs in artists_pairs_proximity.items():
        for pair_name, proximity_ in pairs.items():
            proximity_.normalize_gender_proximity(min_value=min_gender_proximity, max_value=max_gender_proximity)
            proximity_.normalize_theme_proximity(min_value=min_theme_proximity, max_value=max_theme_proximity)
            proximity_.normalize_members_num_proximity(
                min_value=min_members_num_proximity, max_value=max_members_num_proximity)
            proximity_.normalize_year_of_birth_proximity(
                min_value=min_year_of_birth_proximity, max_value=max_year_of_birth_proximity)
            proximity_.normalize_genre_proximity(min_value=min_genre_proximity, max_value=max_genre_proximity)

    # нормализация general_proximity
    general_proximities: Set[float] = set()
    for first_artist_name, pairs in artists_pairs_proximity.items():
        for pair_name, proximity_ in pairs.items():
            general_proximities.update((proximity_.general_proximity,))
    min_general_proximity = min(general_proximities)
    max_general_proximity = max(general_proximities)
    for first_artist_name, pairs in artists_pairs_proximity.items():
        for pair_name, proximity_ in pairs.items():
            proximity_.normalize_general_proximity(min_value=min_general_proximity, max_value=max_general_proximity)

    return artists_pairs_proximity


def calc_generalizing_proximity_measure(artist_name: str, tree: Node):

    pass
