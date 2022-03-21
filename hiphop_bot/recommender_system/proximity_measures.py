from hiphop_bot.recommender_system.pow_distance import calc_distance_in_pow_multi_attributes, calc_distance_in_pow
from hiphop_bot.recommender_system.tree.artist_node import ArtistNode
from hiphop_bot.recommender_system.tree.node import Node
from hiphop_bot.recommender_system.tree.tree_tools import (
    calc_distance_between_nodes, get_leafs_values, calc_max_distance_between_nodes_optimized)
from hiphop_bot.recommender_system.tree.tree_tools import calc_distance_between_all_nodes
from hiphop_bot.recommender_system import config


def calc_euclidean_measure_for_all_attributes(leaf_1: ArtistNode, leaf_2: ArtistNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items()]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items()]
    return calc_distance_in_pow_multi_attributes(attributes1, attributes2, 2)


def calc_manhattan_measure_for_all_attributes(leaf_1: ArtistNode, leaf_2: ArtistNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items()]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items()]
    return calc_distance_in_pow_multi_attributes(attributes1, attributes2, 1)


def calc_manhattan_measure(attribute1: float, attribute2: float):
    return calc_distance_in_pow(attribute1, attribute2, 1)


def calc_tree_distance_measure(
        tree: Node,
        leaf_1: ArtistNode,
        leaf_2: ArtistNode,
        max_distance_between_nodes: int
):
    return calc_distance_between_nodes(tree, leaf_1.name, leaf_2.name) / max_distance_between_nodes


def get_extremum(node_pairs_proximity: dict, func) -> float:
    local_extr_values = []
    for pair_artists in node_pairs_proximity.values():
        local_extr_values.append(func(pair_artists.values()))
    return func(local_extr_values)


def calc_max_general_proximity(node_pairs_proximity: dict) -> float:
    return get_extremum(node_pairs_proximity, max)


def calc_min_general_proximity(node_pairs_proximity: dict) -> float:
    return get_extremum(node_pairs_proximity, min)


def generalizing_proximity_measure(
        tree: Node,
        leaf_1: ArtistNode,
        leaf_2: ArtistNode,
        max_distance_between_nodes: int) -> float:
    attributes1 = leaf_1.countable_attributes
    attributes2 = leaf_2.countable_attributes
    gender_proximity = calc_manhattan_measure(attributes1['male_female'], attributes2['male_female'])
    theme_proximity = calc_manhattan_measure(attributes1['theme'], attributes2['theme'])
    year_of_birth_proximity = calc_manhattan_measure(attributes1['year_of_birth'], attributes2['year_of_birth'])
    members_num_proximity = calc_manhattan_measure(attributes1['solo_duet_group'], attributes2['solo_duet_group'])
    tree_distance = calc_tree_distance_measure(tree, leaf_1, leaf_2, max_distance_between_nodes)
    genre_proximity = tree_distance

    gender_proximity *= config.GENDER_PROXIMITY_MEASURE_WEIGHT
    theme_proximity *= config.THEME_PROXIMITY_MEASURE_WEIGHT
    year_of_birth_proximity *= config.YEAR_OF_BIRTH_PROXIMITY_MEASURE_WEIGHT
    members_num_proximity *= config.MEMBERS_NUM_PROXIMITY_MEASURE_WEIGHT
    genre_proximity *= config.GENRE_PROXIMITY_MEASURE_WEIGHT

    generalizing_proximity = gender_proximity + theme_proximity + year_of_birth_proximity + \
                             members_num_proximity + genre_proximity
    return generalizing_proximity


def normalize_value(value, min_value: float, max_value: float) -> float:
    if value < min_value:
        return 0
    value -= min_value
    value /= (max_value - min_value)
    return value


def normalize_proximities(leafs_pairs_proximity: dict, min_proximity: float, max_proximity: float):
    for artist1_name, pair_artists in leafs_pairs_proximity.items():
        for pair_name in pair_artists.keys():
            leafs_pairs_proximity[artist1_name][pair_name] = normalize_value(
                leafs_pairs_proximity[artist1_name][pair_name],
                min_proximity,
                max_proximity
            )


def calc_generalizing_proximity_measure_for_all_leafs(tree: Node) -> dict:
    leafs = []
    get_leafs_values(tree, leafs)

    distances_between_nodes = calc_distance_between_all_nodes(tree, leafs)
    max_distance_between_nodes = calc_max_distance_between_nodes_optimized(distances_between_nodes)

    leafs_pairs_proximity = {}
    i = 0
    for leaf1 in leafs:
        for leaf2 in leafs:
            if leaf1 != leaf2:
                proximity = generalizing_proximity_measure(tree, leaf1, leaf2, max_distance_between_nodes)
                if leaf1.name not in leafs_pairs_proximity:
                    leafs_pairs_proximity.update({leaf1.name: {}})
                leafs_pairs_proximity[leaf1.name].update(
                    {leaf2.name: proximity}
                )
                i += 1

    # нормализация близости
    max_proximity = calc_max_general_proximity(leafs_pairs_proximity)
    min_proximity = calc_min_general_proximity(leafs_pairs_proximity)
    normalize_proximities(leafs_pairs_proximity, min_proximity, max_proximity)
    return leafs_pairs_proximity


def calc_generalizing_proximity_measure(artist_name: str, tree: Node):
    pass
