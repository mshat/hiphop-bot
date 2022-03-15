from typing import List
from collections import OrderedDict
from hiphop_bot.recommender_system.recommendation_list import get_recommendations
from hiphop_bot.recommender_system.tree.node import Node
from hiphop_bot.recommender_system.tree.tree_loader import load_tree
from hiphop_bot.recommender_system.recommendation_list import load_artist_pairs_proximity
from hiphop_bot.recommender_system.proximity_measures import (
    calc_max_general_proximity,
    calc_min_general_proximity,
    normalize_proximities
)
from hiphop_bot.recommender_system.tree.tree_tools import get_leafs_values
from hiphop_bot.recommender_system.tree.artist_node import ArtistVisualNode
from hiphop_bot.recommender_system.singleton import Singleton


class RecommenderSystemArgumentError(Exception): pass


class RecommenderSystem(metaclass=Singleton):
    def __init__(self):
        self._tree = load_tree()
        self._artists_pairs_proximity = load_artist_pairs_proximity()

        max_proximity = calc_max_general_proximity(self._artists_pairs_proximity)
        min_proximity = calc_min_general_proximity(self._artists_pairs_proximity)
        normalize_proximities(self._artists_pairs_proximity, min_proximity, max_proximity)

    def find_artist(self, name: str) -> ArtistVisualNode:
        artist = Node.get_child_by_name(self._tree, name)
        if not artist:
            raise RecommenderSystemArgumentError(f'Артиста "{name}" нет в базе')
        return artist

    def recommend_by_seed(self, seed_artist: str, disliked_artists: List[str], debug=False) -> OrderedDict[str, float]:
        seed = self.find_artist(seed_artist)

        recommendations = get_recommendations(seed, self._artists_pairs_proximity)
        for dislike in disliked_artists:
            if dislike in recommendations:
                recommendations.pop(dislike)
                if debug:
                    print(f'Артист {dislike} удалён из выборки')

        return recommendations

    def recommend_by_likes(
            self,
            liked_artists: List[str],
            disliked_artists: List[str],
            debug=False) -> OrderedDict[str, float]:
        artists_recommendations = OrderedDict()
        for artist_name in liked_artists:
            recommendations_: OrderedDict[str, float] = self.recommend_by_seed(artist_name, disliked_artists, debug)
            artists_recommendations[artist_name] = list(recommendations_.items())

        recommendations_by_likes: OrderedDict[str, float] = OrderedDict()
        max_recommendation_len = max(map(len, artists_recommendations.values()))
        for i in range(max_recommendation_len):
            for artist, recommendations in artists_recommendations.items():
                if len(recommendations) > i:
                    name = recommendations[i][0]
                    proximity = recommendations[i][1]
                    if name not in recommendations_by_likes and name not in liked_artists:
                        recommendations_by_likes[name] = proximity
        return recommendations_by_likes

    def get_all_artists(self) -> List[ArtistVisualNode]:
        artists = []
        get_leafs_values(self._tree, artists)  # TODO возможно, это можео сделать мтеодами класса Node
        return artists

    def get_artists_by_genre(self, genre: str) -> List[ArtistVisualNode]:
        artists = []
        genre_node = Node.get_child_by_name(self._tree, genre)
        if genre_node:
            get_leafs_values(genre_node, artists)

        all_artists = self.get_all_artists()
        for artist in all_artists:
            if artist.genre == genre:
                artists.append(artist)

        if artists is None:
            artists = []
        artists = list(set(artists))
        return artists
