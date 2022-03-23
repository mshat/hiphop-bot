from typing import Dict
from hiphop_bot.recommender_system.tree.node import Node
from hiphop_bot.recommender_system.models.genre_tree import GenreTreeModel


def load_genre_tree():
    genre_tree_model = GenreTreeModel()
    genre_tree = genre_tree_model.get_all()

    return genre_tree.tree_dict


def create_node(node_name, children_dict):
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


def load_genres_tree() -> Node:
    genres_tree: Dict[str, Dict] = load_genre_tree()
    return create_node('hiphop', genres_tree['hiphop'])
