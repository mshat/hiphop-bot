from hiphop_bot.recommender_system.pow_distance import calc_distance_in_pow
from hiphop_bot.recommender_system.tree.artist_node import ArtistNode
from hiphop_bot.recommender_system.tree.node import Node
from hiphop_bot.recommender_system.tree.tree_tools import (
    calc_distance_between_nodes, get_leafs_values, calc_max_distance_between_nodes_optimized)
from hiphop_bot.recommender_system.tree.tree_tools import calc_distance_between_all_nodes


def calc_euclidean_measure(leaf_1: ArtistNode, leaf_2: ArtistNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items() if name not in ('name', 'theme')]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items() if name not in ('name', 'theme')]
    return calc_distance_in_pow(attributes1, attributes2, 2)


def calc_manhattan_measure(leaf_1: ArtistNode, leaf_2: ArtistNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items() if name in ('name', 'theme')]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items() if name in ('name', 'theme')]
    return calc_distance_in_pow(attributes1, attributes2, 1)


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
        max_distance_between_nodes: int,
        min_general_proximity: float = None,
        max_general_proximity: float = None) -> float:
    euclidean_proximity = calc_euclidean_measure(leaf_1, leaf_2)
    manhattan_proximity = calc_manhattan_measure(leaf_1, leaf_2)
    tree_distance = calc_tree_distance_measure(tree, leaf_1, leaf_2, max_distance_between_nodes)
    generalizing_proximity = euclidean_proximity + manhattan_proximity / 10 + tree_distance
    if max_general_proximity or min_general_proximity:
        assert max_general_proximity and min_general_proximity
    if max_general_proximity and min_general_proximity:
        generalizing_proximity = normalize_value(generalizing_proximity, min_general_proximity, max_general_proximity)
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


def calc_generalizing_proximity_measure_for_all_leafs(tree) -> dict:
    leafs = []
    get_leafs_values(tree, leafs)

    distances_between_nodes = calc_distance_between_all_nodes(tree, leafs)
    max_distance_between_nodes = calc_max_distance_between_nodes_optimized(distances_between_nodes)

    leafs_pairs_proximity = {}
    max_proximity = 0
    i = 0
    for leaf1 in leafs:
        for leaf2 in leafs:
            if leaf1 != leaf2:
                proximity = generalizing_proximity_measure(tree, leaf1, leaf2, max_distance_between_nodes)
                if proximity > max_proximity:
                    max_proximity = proximity
                if leaf1.name not in leafs_pairs_proximity:
                    leafs_pairs_proximity.update({leaf1.name: {}})
                leafs_pairs_proximity[leaf1.name].update(
                    {leaf2.name: proximity}
                )
                i += 1

    return leafs_pairs_proximity
