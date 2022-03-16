from typing import Dict
from hiphop_bot.recommender_system.tree.node import Node
from hiphop_bot.recommender_system.tree.artist_node import ArtistNode
from hiphop_bot.recommender_system.models.artist import ArtistModel
from hiphop_bot.recommender_system.models.genre_tree import GenreTreeModel


def load_genre_tree():
    genre_tree_model = GenreTreeModel()
    genre_tree = genre_tree_model.get_all()

    return genre_tree.tree_dict


def load_artists(genre):
    artist_model = ArtistModel()
    artists = artist_model.get_by_genre(genre)
    return artists


def create_node(node_name, children_dict):
    if not children_dict:  # this node is leaf
        artists = load_artists(node_name.lower())
        if artists:
            leafs = []
            for artist in artists:
                leafs.append(ArtistNode(artist))
            return leafs
        else:
            node = Node(val=node_name)
    else:
        node = Node(val=node_name)
    for child_name in children_dict.keys():
        if children_dict:
            res = create_node(child_name, children_dict[child_name])
            if isinstance(res, list):
                for artist_node in res:
                    node.add_child(artist_node)
            else:
                node.add_child(res)
    return node


def load_tree() -> Node:
    genres_tree: Dict[str, Dict] = load_genre_tree()
    return create_node('hiphop', genres_tree['hiphop'])
