import os
import json
from collections import OrderedDict
from hiphop_bot.dialog_bot.recommender_system.tree.genre_node import GenreVisualNode
from hiphop_bot.dialog_bot.recommender_system.proximity_measures import \
    calc_generalizing_proximity_measure_for_all_leafs
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

    for recommendation_name, proximity in recommendations.items():
        if show_proximity:
            format_print([recommendation_name, proximity], [20, 5])
        else:
            print(recommendation_name)
