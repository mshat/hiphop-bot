from typing import List
from hiphop_bot.recommender_system.recommender_system import RecommenderSystem
from hiphop_bot.recommender_system.models.artist import _Artist  # Импортируется для аннотаций
from hiphop_bot.recommender_system.tree.artist_node import ArtistVisualNode


class AdaptedRecommenderSystem:
    def __init__(self):
        self.recommender_system = RecommenderSystem()

    def get_artist_by_name(self, name: str) -> _Artist:
        artist = self.recommender_system.get_artist_by_name(name)
        return artist.artist

    def recommend_by_seed(self, seed_artist: str, disliked_artists: List[str], debug=False) -> List[_Artist]:
        recommendations_by_artist = self.recommender_system.recommend_by_seed(seed_artist, disliked_artists, debug)
        adapted_recommendations_by_artist = self._adapt_artists(recommendations_by_artist)
        return adapted_recommendations_by_artist

    def recommend_by_likes(self, liked_artists: List[str], disliked_artists: List[str], debug=False) -> List[_Artist]:
        recommendations_by_likes = self.recommender_system.recommend_by_likes(liked_artists, disliked_artists, debug)
        adapted_recommendations_by_likes = self._adapt_artists(recommendations_by_likes)
        return adapted_recommendations_by_likes

    def _adapt_artists(self, artists: List[ArtistVisualNode | _Artist]) -> List[_Artist]:
        adapted_artists = []

        for artist_obj in artists:
            if isinstance(artist_obj, ArtistVisualNode):
                adapted_artists.append(artist_obj.artist)
            elif isinstance(artist_obj, _Artist):
                adapted_artists.append(artist_obj)
        return adapted_artists

    def get_all_artists(self) -> List[_Artist]:
        artists = self.recommender_system.get_all_artists()
        return self._adapt_artists(artists)

    def get_artists_by_genre(self, genre: str) -> List[_Artist]:
        artists = self.recommender_system.get_artists_by_genre(genre)
        return self._adapt_artists(artists)

    def filter_artists(
            self,
            artists: List[ArtistVisualNode] | List[_Artist],
            group_type: str = 'any',
            sex: str = 'anysex',
            younger: int = None,
            older: int = None) -> List[_Artist]:
        filtered = self.recommender_system.filter_artists(artists, group_type, sex, younger, older)
        adapted_filtered = self._adapt_artists(filtered)
        return adapted_filtered