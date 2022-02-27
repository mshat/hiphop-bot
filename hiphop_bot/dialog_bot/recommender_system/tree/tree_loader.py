import os
import json
from .visual_node import VisualNode
from .genre_node import GenreVisualNode

dir_path = os.path.dirname(os.path.realpath(__file__))


def load_tree_dict(filename='genres.json'):
    with open(filename, 'r') as file:
        genres = json.load(file)
    return genres


def get_artists(genre):
    with open(f'{dir_path}\\..\\data\\artists.json', 'r', encoding='utf-8') as file:
        genres_with_artists = json.load(file)
    artists = genres_with_artists[genre] if genre in genres_with_artists.keys() else None
    return artists


def create_node(node_name, children_dict):
    if not children_dict:  # this node is leaf
        artists = get_artists(node_name.lower())
        if artists:
            leafs = []
            for artist, attributes in artists.items():
                leafs.append(
                    GenreVisualNode(
                        node_name,
                        artist,
                        attributes['year_of_birth'],
                        attributes['group_members_num'],
                        attributes['theme'],
                        attributes['is_male']))
            return leafs
        else:
            node = VisualNode(val=node_name)
    else:
        node = VisualNode(val=node_name)
    for child_name in children_dict.keys():
        if children_dict:
            res = create_node(child_name, children_dict[child_name])
            if isinstance(res, list):
                for artist_node in res:
                    node.add_child(artist_node)
            else:
                node.add_child(res)
    return node


def create_tree_from_json(filename='genres.json') -> VisualNode:
    tree_dict = load_tree_dict(filename)
    return create_node('hiphop', tree_dict['hiphop'])


