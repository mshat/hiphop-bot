from typing import List
from hiphop_bot.recommender_system.recommender_system import RecommenderSystem
from hiphop_bot.recommender_system.models.artist import _Artist  # Импортируется для аннотаций
from hiphop_bot.recommender_system.tree.artist_node import ArtistNode
from hiphop_bot.recommender_system.recommender_system import RecommendedArtist


class AdaptedProximity:
    def __init__(self, general_proximity: float, proximities: List[float]):
        self.general_proximity = general_proximity
        self.proximities = proximities


class AdaptedRecommendedArtist:
    artist: _Artist
    proximity: AdaptedProximity

    def __init__(self, artist: _Artist, proximity: AdaptedProximity):
        self.artist = artist
        self.proximity = proximity


class AdaptedRecommenderSystem:
    def __init__(self):
        self.recommender_system = RecommenderSystem()

    def get_artist_by_name(self, name: str) -> _Artist:
        artist = self.recommender_system.get_artist_by_name(name)
        return artist.artist

    def recommend_by_seed(
            self,
            seed_artist: str,
            disliked_artists: List[str],
            debug=False) -> List[AdaptedRecommendedArtist]:
        recommendations_by_artist = self.recommender_system.recommend_by_seed(seed_artist, disliked_artists, debug)
        adapted_recommendations_by_artist = self._adapt_recommended_artists_list(recommendations_by_artist)
        return adapted_recommendations_by_artist

    def recommend_by_likes(self, liked_artists: List[str], disliked_artists: List[str], debug=False) -> List[_Artist]:
        recommendations_by_likes = self.recommender_system.recommend_by_likes(liked_artists, disliked_artists, debug)
        adapted_recommendations_by_likes = self._adapt_artists_to_artist_type(recommendations_by_likes)
        return adapted_recommendations_by_likes

    def _adapt_recommended_artist(self, artist: RecommendedArtist):
        return AdaptedRecommendedArtist(
            artist.artist.artist, AdaptedProximity(artist.proximity.general_proximity, artist.proximity.proximities))

    def _adapt_recommended_artists_list(self, artists: List[RecommendedArtist]):
        return [self._adapt_recommended_artist(artist) for artist in artists]

    def _adapt_artists_to_artist_type(self, artists: List[ArtistNode | _Artist]) -> List[_Artist]:
        adapted_artists = []
        for artist_obj in artists:
            if isinstance(artist_obj, ArtistNode):
                adapted_artists.append(artist_obj.artist)
            elif isinstance(artist_obj, _Artist):
                adapted_artists.append(artist_obj)
        return adapted_artists

    def _adapt_artists_to_artist_visual_node_type(self, artists: List[ArtistNode | _Artist]) \
            -> List[ArtistNode]:
        adapted_artists = []

        for artist_obj in artists:
            if isinstance(artist_obj, ArtistNode):
                adapted_artists.append(artist_obj)
            elif isinstance(artist_obj, _Artist):
                adapted_artists.append(ArtistNode(artist_obj))
        return adapted_artists

    def get_all_artists(self) -> List[_Artist]:
        artists = self.recommender_system.get_all_artists()
        return self._adapt_artists_to_artist_type(artists)

    def get_artists_by_genre(self, genre: str) -> List[_Artist]:
        artists = self.recommender_system.get_artists_by_genre(genre)
        return self._adapt_artists_to_artist_type(artists)

    def filter_artists(
            self,
            artists: List[ArtistNode] | List[_Artist],
            group_type: str = 'any',
            sex: str = 'anysex',
            younger: int = None,
            older: int = None) -> List[_Artist]:
        adapted_for_recommender_system_artists = self._adapt_artists_to_artist_visual_node_type(artists)
        filtered_artists = self.recommender_system.filter_artists(
            adapted_for_recommender_system_artists, group_type, sex, younger, older
        )
        adapted_filtered_artists = self._adapt_artists_to_artist_type(filtered_artists)
        return adapted_filtered_artists
