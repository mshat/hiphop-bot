import os
from typing import List, Iterable
from collections import OrderedDict
from hiphop_bot.dialog_bot.recommender_system.recommendation_list import get_recommendations
from hiphop_bot.dialog_bot.recommender_system.recommendation_list import (
    Node, create_tree_from_json, load_artist_pairs_proximity_json, calc_max_general_proximity,
    calc_min_general_proximity, normalize_proximities)
from hiphop_bot.dialog_bot.recommender_system.tree.tree_tools import calc_max_distance_between_nodes, get_leafs_values
from hiphop_bot.dialog_bot.recommender_system.tree.genre_node import GenreVisualNode, VisualNode

dir_path = os.path.dirname(os.path.realpath(__file__))
TREE = create_tree_from_json(f'{dir_path}/data/genres.json')
ARTIST_PAIRS_PROXIMITY = load_artist_pairs_proximity_json()
max_proximity = calc_max_general_proximity(ARTIST_PAIRS_PROXIMITY)
min_proximity = calc_min_general_proximity(ARTIST_PAIRS_PROXIMITY)
max_distance_between_nodes = calc_max_distance_between_nodes(TREE)
normalize_proximities(ARTIST_PAIRS_PROXIMITY, min_proximity, max_proximity)


class ParseError(Exception): pass
class ArgumentError(Exception): pass


def print_recommendations(recommendations, output_len=None, debug=False):
    if output_len is None:
        output_len = 100000
    for i, artist_name in enumerate(recommendations):
        if i < output_len:
            if debug:
                print(artist_name, recommendations[artist_name])
            else:
                print(artist_name)


def print_artists(artists: List[GenreVisualNode], max_output_len=None, debug=False):
    if max_output_len is None:
        max_output_len = 100000
    for i, artist in enumerate(artists):
        if i < max_output_len:
            if debug:
                print(artist.name, artist.genre)
            else:
                print(artist.name)


def print_strings(strings: Iterable[str], max_output_len=None):
    if max_output_len is None:
        max_output_len = 100000
    for i, item in enumerate(strings):
        if i < max_output_len:
            print(item)


def find_artist(name: str) -> GenreVisualNode:
    artist = Node.get_child_by_name(TREE, name)
    if not artist:
        raise ArgumentError(f'Артиста "{name}" нет в базе')
    return artist


def split_artists(artists: str):
    artists.strip()
    artists = artists.replace('  ', ' ')
    artists = artists.replace('   ', ' ')
    res = list(map(str.strip, artists.split(',')))
    return res


def recommend_by_seed(seed_artist: str, disliked_artists: [str], debug=False):
    seed = find_artist(seed_artist)

    recommendations = get_recommendations(seed, ARTIST_PAIRS_PROXIMITY)
    for dislike in disliked_artists:
        if dislike in recommendations:
            recommendations.pop(dislike)
            if debug:
                print(f'Артист {dislike} удалён из выборки')

    return recommendations


def recommend_by_liked(liked_artist_names: List[str] = None):
    liked_artists = {find_artist(artist.lower()) for artist in liked_artist_names}

    artist_recommendations = OrderedDict()
    for artist in liked_artists:
        recommendations = get_recommendations(
            artist,
            ARTIST_PAIRS_PROXIMITY
        )
        artist_recommendations[artist.name] = \
            [(artist_name, proximity) for artist_name, proximity in recommendations.items()]

    final_recommendations = {}
    max_recommendation_len = max(map(len, artist_recommendations.values()))
    for i in range(max_recommendation_len):
        for artist, recommendations in artist_recommendations.items():
            if len(recommendations) > i:
                name = recommendations[i][0]
                proximity = recommendations[i][1]
                if name not in final_recommendations and name not in liked_artist_names:
                    final_recommendations[name] = proximity

    final_recommendation_artists = list(final_recommendations.keys())
    final_dict = OrderedDict({artist: final_recommendations[artist] for artist in final_recommendation_artists})

    return final_dict


def recommend_by_liked_with_disliked(
        disliked_artists_list: List[str] = None,
        liked_artists_list: List[str] = None,
        debug=False):
    recommendations_by_liked = recommend_by_liked(liked_artists_list)
    for dislike in disliked_artists_list:
        if dislike in recommendations_by_liked:
            recommendations_by_liked.pop(dislike)
            if debug:
                print(f'Артист {dislike} удалён из выборки')
    return recommendations_by_liked


def get_artist_by_name(name: str):
    artist = Node.get_child_by_name(TREE, name)
    return artist


def get_all_artists():
    artists = []
    get_leafs_values(TREE, artists)
    return artists


def get_artists_by_genre(genre: str):
    artists = []
    genre_node = Node.get_child_by_name(TREE, genre)
    if genre_node:
        get_leafs_values(genre_node, artists)

    all_artists = get_all_artists()
    for artist in all_artists:
        if artist.genre == genre:
            artists.append(artist)

    if artists is None: artists = []
    artists = list(set(artists))
    return artists

