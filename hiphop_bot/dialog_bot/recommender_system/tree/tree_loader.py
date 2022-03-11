import os
import json
from hiphop_bot.dialog_bot.recommender_system.tree.visual_node import VisualNode
from hiphop_bot.dialog_bot.recommender_system.tree.artist_node import ArtistVisualNode
from hiphop_bot.dialog_bot.recommender_system.models.artist import ArtistModel
from hiphop_bot.dialog_bot.recommender_system.models.genre import GenreModel

dir_path = os.path.dirname(os.path.realpath(__file__))


def load_tree_dict(filename='genres.json'):
    with open(filename, 'r') as file:
        genres = json.load(file)
    return genres


def get_artists(genre):
    artist_model = ArtistModel()
    artists = artist_model.get_by_genre(genre)
    return artists


def create_node(node_name, children_dict):
    if not children_dict:  # this node is leaf
        artists = get_artists(node_name.lower())
        if artists:
            leafs = []
            for artist in artists:
                leafs.append(
                    ArtistVisualNode(
                        genre=node_name,
                        name=artist.name,
                        year_of_birth=artist.year_of_birth,
                        group_members_num=artist.group_members_num,
                        theme=artist.theme,
                        is_male=1 if artist.gender == 'male' else 0,)
                )
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
