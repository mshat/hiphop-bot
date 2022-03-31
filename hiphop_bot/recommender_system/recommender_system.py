from typing import List, Dict, Set
from collections import OrderedDict
from hiphop_bot.recommender_system.singleton import Singleton
from hiphop_bot.recommender_system.config import MIN_PROXIMITY
from hiphop_bot.recommender_system.artist_filterer import filter_artists
from hiphop_bot.recommender_system.models.artist_pairs_proximity import ArtistsPairsProximityModel, Proximity
from hiphop_bot.recommender_system.models.artist import ArtistModel, _Artist
from hiphop_bot.recommender_system.tree.tree_loader import load_genres_tree


class RecommendedArtist:
    artist: _Artist
    proximity: Proximity

    def __init__(self, artist: _Artist, proximity: Proximity):
        self.artist = artist
        self.proximity = proximity


class RecommenderSystemArgumentError(Exception): pass


class RecommenderSystem(metaclass=Singleton):
    def __init__(self):
        self._artist_model = ArtistModel()
        self.artist_pairs_proximity_model = ArtistsPairsProximityModel()
        self.genres_tree = load_genres_tree()

    def _get_artist_pairs_proximity(self, name: str) -> Dict[str, Proximity]:
        pairs_proximities = self.artist_pairs_proximity_model.get_by_first_artist_name(name)
        return {pair_proximity.second_artist_name: pair_proximity.proximity for pair_proximity in pairs_proximities}

    def get_artist_by_name(self, name: str) -> _Artist:
        artist = self._artist_model.get_by_name(name)
        if not artist:
            raise RecommenderSystemArgumentError(f'Артиста "{name}" нет в базе')
        return artist

    def _get_recommendations(
            self,
            seed_object: _Artist) -> List[RecommendedArtist]:
        artist_pairs: Dict[str, Proximity] = self._get_artist_pairs_proximity(seed_object.name)

        # pycharm подсвечивает ошибку типов, но ошибки нет. Sorted возвращает именно OrderedDict[str, Proximity]]
        artist_pairs_sorted_by_proximity: Dict[str, Proximity] = OrderedDict(
            sorted(artist_pairs.items(), key=lambda item: item[1].general_proximity)
        )

        recommendations: Dict[str, RecommendedArtist] = OrderedDict()
        for artist_name, proximity in artist_pairs_sorted_by_proximity.items():
            if proximity.general_proximity <= MIN_PROXIMITY and artist_name not in recommendations:
                artist = self.get_artist_by_name(artist_name)
                recommendations.update({artist_name: RecommendedArtist(artist, proximity)})

        # добавляем рекомендации до 5 штук, если по условию MIN_PROXIMITY их получилось меньше
        for artist_name, proximity in artist_pairs_sorted_by_proximity.items():
            if len(recommendations) >= 5:
                break
            if artist_name not in recommendations:
                artist = self.get_artist_by_name(artist_name)
                recommendations.update({artist_name: RecommendedArtist(artist, proximity)})
        return list(recommendations.values())

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
            -> List[_Artist]:
        artists_recommendations: Dict[str, List[_Artist]] = OrderedDict()
        for artist_name in liked_artists:
            recommendations_: List[RecommendedArtist] = self.recommend_by_seed(artist_name, disliked_artists, debug)
            artists_recommendations[artist_name] = [artist.artist for artist in recommendations_]

        recommendations_by_likes: Dict[str, _Artist] = OrderedDict()
        max_recommendation_len = max(map(len, artists_recommendations.values()))
        for i in range(max_recommendation_len):
            for artist, recommended_artists in artists_recommendations.items():
                if len(recommended_artists) > i:
                    recommended_artist = recommended_artists[i]
                    if recommended_artist in recommendations_by_likes:
                        continue
                    if recommended_artist.name in liked_artists:
                        continue
                    recommendations_by_likes.update({recommended_artist.name: recommended_artist})
        return list(recommendations_by_likes.values())

    def get_all_artists(self) -> List[_Artist]:
        return self._artist_model.get_all()

    def get_artists_by_genre(self, genre: str) -> List[_Artist]:
        artists: Set[_Artist] | Set = set()

        genre_node = self.genres_tree.get_child_by_name(self.genres_tree, genre)
        children_genres_names = []
        self.genres_tree.get_children_names(genre_node, children_genres_names)

        searched_genres = set([genre] + children_genres_names)

        for genre in searched_genres:
            genre_artists = self._artist_model.get_by_genre(genre)
            if genre_artists:
                artists.update(genre_artists)
        return list(artists)

    def filter_artists(
            self,
            artists: List[_Artist],
            group_type: str = 'any',
            sex: str = 'anysex',
            younger: int = None,
            older: int = None) -> List[_Artist]:
        return filter_artists(artists, group_type, sex, younger, older)



