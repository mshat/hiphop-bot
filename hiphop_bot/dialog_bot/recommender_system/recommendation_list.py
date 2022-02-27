import os
import json
from collections import OrderedDict
from hiphop_bot.dialog_bot.recommender_system.tree.visual_node import Node
from hiphop_bot.dialog_bot.recommender_system.tree.tree_tools import calc_max_distance_between_nodes
from hiphop_bot.dialog_bot.recommender_system.tree.tree_loader import create_tree_from_json
from hiphop_bot.dialog_bot.recommender_system.tree.genre_node import GenreVisualNode
from hiphop_bot.dialog_bot.recommender_system.proximity_measures import (
    calc_generalizing_proximity_measure_for_all_leafs,
    calc_max_general_proximity,
    calc_min_general_proximity,
    normalize_proximities
)
from hiphop_bot.dialog_bot.recommender_system.tools import format_print
from hiphop_bot.dialog_bot.recommender_system.config import MIN_SIMILARITY_PROXIMITY

dir_path = os.path.dirname(os.path.realpath(__file__))


def create_artist_pairs_proximity_json(tree):
    artist_pairs_proximity = calc_generalizing_proximity_measure_for_all_leafs(tree)

    with open('data/artist_pairs_proximity.json', 'w') as file:
        json.dump(artist_pairs_proximity, file)


def load_artist_pairs_proximity_json(filename: str = f'{dir_path}/data/artist_pairs_proximity.json') -> dict:
    with open(filename, 'r') as file:
        return json.load(file)


def print_all_artist_pairs_proximity(artist_pairs_proximity: dict):
    for artist1_name, pair_artists in artist_pairs_proximity.items():
        for pair_name, pair_proximity in pair_artists.items():
            print(f'{artist1_name} - {pair_name} = {pair_proximity}')


def get_recommendations(
        seed_object: GenreVisualNode,
        artist_pairs_proximity: dict) -> OrderedDict:
    artist_pairs = artist_pairs_proximity[seed_object.name]
    artist_pairs_sorted_by_proximity = OrderedDict(sorted(artist_pairs.items(), key=lambda item: item[1]))

    recommendations = OrderedDict()
    for artist_name, proximity in artist_pairs_sorted_by_proximity.items():
        if proximity <= MIN_SIMILARITY_PROXIMITY:
            if artist_name not in recommendations:
                recommendations[artist_name] = proximity
    return recommendations


def show_recommendations(
        seed_object: GenreVisualNode,
        artist_pairs_proximity: dict,
        show_proximity=False) -> None:
    recommendations = get_recommendations(seed_object, artist_pairs_proximity)
    # print(f'seed_object: {seed_object.name}')
    for recommendation_name, proximity in recommendations.items():
        if show_proximity:
            format_print([recommendation_name, proximity], [20, 5])
        else:
            print(recommendation_name)


def main():
    tree = create_tree_from_json('data/genres.json')
    create_artist_pairs_proximity_json(tree)
    artist_pairs_proximity = load_artist_pairs_proximity_json()
    max_general_proximity = calc_max_general_proximity(artist_pairs_proximity)
    min_general_proximity = calc_min_general_proximity(artist_pairs_proximity)
    normalize_proximities(artist_pairs_proximity, min_general_proximity, max_general_proximity)
    max_distance_between_nodes = calc_max_distance_between_nodes(tree)

    # values = []
    # for artist, pair in artist_pairs_proximity.items():
    #     print(artist, pair)
    #     values += list(pair.values())
    # print('SORTED PROXIMITIES', sorted(values))

    print_all_artist_pairs_proximity(artist_pairs_proximity)

    ## ноды для мер близости
    atl = Node.get_child_by_name(tree, 'atl')
    marlow = Node.get_child_by_name(tree, 'slava marlow')
    max_korj = Node.get_child_by_name(tree, 'макс корж')
    lsp = Node.get_child_by_name(tree, 'лсп')
    mukka = Node.get_child_by_name(tree, 'мукка')
    krovostok = Node.get_child_by_name(tree, 'кровосток')
    liga = Node.get_child_by_name(tree, 'лигалайз')
    jah = Node.get_child_by_name(tree, 'jah khalib')
    krec= Node.get_child_by_name(tree, 'krec')
    mnogotochie = Node.get_child_by_name(tree, 'многоточие')

    # proximity = generalizing_proximity_measure(
    #     tree, atl, atl, max_distance_between_nodes, min_general_proximity, max_general_proximity
    # )
    # print(proximity)

    ## сравнение
    # artist_pairs = [(marlow, max_korj), (lsp, marlow), (lsp, max_korj), (lsp, atl), (lsp, mukka), (lsp, krovostok),
    #                 (krovostok, mukka), (liga, jah)]
    # compare_measures(tree, artist_pairs, min_general_proximity, max_general_proximity)
    #
    # show_recommendations(atl, artist_pairs_proximity, show_proximity=True)


if __name__ == '__main__':
    main()