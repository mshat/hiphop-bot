from typing import List, Dict
from collections import OrderedDict
from hiphop_bot.recommender_system.tree.node import Node
from hiphop_bot.recommender_system.tree.tree_loader import load_tree
from hiphop_bot.recommender_system.tree.tree_tools import get_leafs_values
from hiphop_bot.recommender_system.tree.artist_node import ArtistNode
from hiphop_bot.recommender_system.singleton import Singleton
from hiphop_bot.recommender_system.config import MIN_PROXIMITY
from hiphop_bot.recommender_system.artist_filterer import filter_artists
from hiphop_bot.recommender_system.models.artist_pairs_proximity import ArtistsPairsProximityModel, Proximity


class RecommendedArtist:
    artist: ArtistNode
    proximity: Proximity

    def __init__(self, artist: ArtistNode, proximity: Proximity):
        self.artist = artist
        self.proximity = proximity


class RecommenderSystemArgumentError(Exception): pass


class RecommenderSystem(metaclass=Singleton):
    _artists_pairs_proximity: Dict[str, Dict[str, Proximity]]

    def __init__(self):
        self._tree = load_tree()
        artist_pairs_proximity_model = ArtistsPairsProximityModel()
        self._artists_pairs_proximity = artist_pairs_proximity_model.get_artists_proximity_dict()

    def get_artist_by_name(self, name: str) -> ArtistNode:
        artist = Node.get_child_by_name(self._tree, name)
        if not artist:
            raise RecommenderSystemArgumentError(f'Артиста "{name}" нет в базе')
        return artist

    def _get_recommendations(
            self,
            seed_object: ArtistNode) -> List[RecommendedArtist]:
        artist_pairs: Dict[str, Proximity] = self._artists_pairs_proximity[seed_object.name]

        # pycharm подсвечивает ошибку типов, но ошибки нет. Sorted возвращает именно OrderedDict[str, Proximity]]
        artist_pairs_sorted_by_proximity: Dict[str, Proximity] = OrderedDict(
            sorted(artist_pairs.items(), key=lambda item: item[1].general_proximity)
        )

        recommendations: List[RecommendedArtist] = []
        for artist_name, proximity in artist_pairs_sorted_by_proximity.items():
            if proximity.general_proximity <= MIN_PROXIMITY and artist_name not in recommendations:
                artist = self.get_artist_by_name(artist_name)
                recommendations.append(RecommendedArtist(artist, proximity))
        return recommendations

    def recommend_by_seed(self, seed_artist: str, disliked_artists: List[str], debug=False) -> List[RecommendedArtist]:
        seed = self.get_artist_by_name(seed_artist)

        recommendations_by_artist: List[RecommendedArtist] = self._get_recommendations(seed)
        recommendations_by_artist = [recommendation for recommendation in recommendations_by_artist
                                     if recommendation.artist.name not in disliked_artists]

        if debug:  # TODO поменять на флаг дебаг принта
            for recommended_artist in recommendations_by_artist:
                if recommended_artist.artist.name in disliked_artists:
                    print(f'Артист {recommended_artist.artist.name} удалён из выборки')
        return recommendations_by_artist

    def recommend_by_likes(self, liked_artists: List[str], disliked_artists: List[str], debug=False) \
            -> List[ArtistNode]:
        artists_recommendations: Dict[str, List[ArtistNode]] = OrderedDict()
        for artist_name in liked_artists:
            recommendations_: List[RecommendedArtist] = self.recommend_by_seed(artist_name, disliked_artists, debug)
            artists_recommendations[artist_name] = [artist.artist for artist in recommendations_]

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



