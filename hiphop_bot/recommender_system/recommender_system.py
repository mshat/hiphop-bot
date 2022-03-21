from typing import List, Dict
from collections import OrderedDict
from hiphop_bot.recommender_system.tree.node import Node
from hiphop_bot.recommender_system.tree.tree_loader import load_tree
from hiphop_bot.recommender_system.proximity_measures import (
    calc_max_general_proximity,
    calc_min_general_proximity,
    normalize_proximities
)
from hiphop_bot.recommender_system.tree.tree_tools import get_leafs_values
from hiphop_bot.recommender_system.tree.artist_node import ArtistNode
from hiphop_bot.recommender_system.singleton import Singleton
from hiphop_bot.recommender_system.config import MIN_SIMILARITY_PROXIMITY
from hiphop_bot.recommender_system.artist_filterer import filter_artists
from hiphop_bot.recommender_system.models.artist_pairs_proximity import ArtistPairsProximityModel


class RecommenderSystemArgumentError(Exception): pass


class RecommenderSystem(metaclass=Singleton):
    _artists_pairs_proximity: Dict[str, Dict[str, float]]

    def __init__(self):
        self._tree = load_tree()
        artist_pairs_proximity_model = ArtistPairsProximityModel()
        artist_pairs_proximity_obj = artist_pairs_proximity_model.get_all()
        self._artists_pairs_proximity = artist_pairs_proximity_obj.artists_proximity

        max_proximity = calc_max_general_proximity(self._artists_pairs_proximity)
        min_proximity = calc_min_general_proximity(self._artists_pairs_proximity)
        normalize_proximities(self._artists_pairs_proximity, min_proximity, max_proximity)

    def get_artist_by_name(self, name: str) -> ArtistNode:
        artist = Node.get_child_by_name(self._tree, name)
        if not artist:
            raise RecommenderSystemArgumentError(f'Артиста "{name}" нет в базе')
        return artist

    def _get_recommendations(
            self,
            seed_object: ArtistNode) -> OrderedDict[str, float]:
        artist_pairs: Dict[str, float] = self._artists_pairs_proximity[seed_object.name]

        # pycharm подсвечивает ошибку типов, но ошибки нет. Sorted возвращает List[Tuple[str, float]], а не List[str]
        artist_pairs_sorted_by_proximity = OrderedDict(sorted(artist_pairs.items(), key=lambda item: item[1]))

        recommendations = OrderedDict()
        for artist_name, proximity in artist_pairs_sorted_by_proximity.items():
            if proximity <= MIN_SIMILARITY_PROXIMITY:
                if artist_name not in recommendations:
                    recommendations[artist_name] = proximity
        return recommendations

    def recommend_by_seed(self, seed_artist: str, disliked_artists: List[str], debug=False) -> List[ArtistNode]:
        seed = self.get_artist_by_name(seed_artist)

        recommendations_by_artist: List[ArtistNode] = []
        recommendations = self._get_recommendations(seed)

        for artist_name, proximity in recommendations.items():
            if artist_name not in disliked_artists:
                recommendations_by_artist.append(self.get_artist_by_name(artist_name))
            else:
                if debug:
                    print(f'Артист {artist_name} удалён из выборки')
        return recommendations_by_artist

    def recommend_by_likes(self, liked_artists: List[str], disliked_artists: List[str], debug=False)\
            -> List[ArtistNode]:
        artists_recommendations: Dict[str, List[ArtistNode]] = OrderedDict()
        for artist_name in liked_artists:
            recommendations_: List[ArtistNode] = self.recommend_by_seed(artist_name, disliked_artists, debug)
            artists_recommendations[artist_name] = list(recommendations_)

        recommendations_by_likes: List[ArtistNode] = []
        max_recommendation_len = max(map(len, artists_recommendations.values()))
        for i in range(max_recommendation_len):
            for artist, recommended_artists in artists_recommendations.items():
                if len(recommended_artists) > i:
                    recommended_artist = recommended_artists[i]
                    if recommended_artist in recommendations_by_likes:
                        continue
                    if recommended_artist.name in liked_artists:
                        continue
                    recommendations_by_likes.append(recommended_artist)
        return recommendations_by_likes

    def get_all_artists(self) -> List[ArtistNode]:
        artists = []
        get_leafs_values(self._tree, artists)  # TODO возможно, это можео сделать мтеодами класса Node
        return artists

    def get_artists_by_genre(self, genre: str) -> List[ArtistNode]:
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

    def filter_artists(
            self,
            artists: List[ArtistNode],
            group_type: str = 'any',
            sex: str = 'anysex',
            younger: int = None,
            older: int = None) -> List[ArtistNode]:
        return filter_artists(artists, group_type, sex, younger, older)



