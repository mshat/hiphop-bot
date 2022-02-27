from tree.tree_tools import get_leafs_values, calc_max_distance_between_nodes_optimized, calc_distance_between_all_nodes
from proximity_measures import calc_euclidean_measure, calc_manhattan_measure, generalizing_proximity_measure
from proximity_measures import calc_tree_distance_measure
from tools import format_print


def compare_measures(tree, artist_pairs, min_general_proximity: float = None, max_general_proximity: float = None):
    euclidean_proximity = []
    manhattan_proximity = []
    tree_distance_proximity = []
    generalizing_proximity = []

    leafs = []
    get_leafs_values(tree, leafs)

    distances_between_nodes = calc_distance_between_all_nodes(tree, leafs)
    max_distance_between_artists = calc_max_distance_between_nodes_optimized(distances_between_nodes)
    for artist1, artist2 in artist_pairs:
        euclidean_proximity.append(calc_euclidean_measure(artist1, artist2))
        manhattan_proximity.append(calc_manhattan_measure(artist1, artist2))
        tree_distance_proximity.append(calc_tree_distance_measure(tree, artist1, artist2, max_distance_between_artists))
        generalizing_proximity.append(
            generalizing_proximity_measure(
                tree, artist1, artist2, max_distance_between_artists, min_general_proximity, max_general_proximity
            )
        )

    artist_names = [(artist1.name + ' - ' + artist2.name) for artist1, artist2 in artist_pairs]
    format_print(['artists', 'generalizing', 'euclidean', 'manhattan', 'tree distance'], [25, 15])
    for i in range(len(artist_names)):
        format_print(
            [artist_names[i], generalizing_proximity[i], euclidean_proximity[i], manhattan_proximity[i],
             tree_distance_proximity[i]],
            column_width=[25, 15],
            number_symbols_after_comma=5
        )