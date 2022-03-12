from collections import OrderedDict
from hiphop_bot.dialog_bot.recommender_system.tree.artist_node import ArtistVisualNode
from hiphop_bot.dialog_bot.recommender_system.proximity_measures import \
    calc_generalizing_proximity_measure_for_all_leafs
from hiphop_bot.dialog_bot.recommender_system.tools import format_print
from hiphop_bot.dialog_bot.recommender_system.config import MIN_SIMILARITY_PROXIMITY
from hiphop_bot.dialog_bot.recommender_system.models.artist_pairs_proximity import ArtistPairsProximityModel


# TODO дописать метод для записи в бд список близости артистов
def create_artist_pairs_proximity(tree):
    artist_pairs_proximity = calc_generalizing_proximity_measure_for_all_leafs(tree)
    pass


def load_artist_pairs_proximity() -> dict:
    artist_pairs_proximity_model = ArtistPairsProximityModel()
    res = artist_pairs_proximity_model.get_all()
    return res.artists_proximity


def get_recommendations(
        seed_object: ArtistVisualNode,
        artist_pairs_proximity: dict) -> OrderedDict:
    artist_pairs = artist_pairs_proximity[seed_object.name]
    artist_pairs_sorted_by_proximity = OrderedDict(sorted(artist_pairs.items(), key=lambda item: item[1]))

    recommendations = OrderedDict()
    for artist_name, proximity in artist_pairs_sorted_by_proximity.items():
        if proximity <= MIN_SIMILARITY_PROXIMITY:
            if artist_name not in recommendations:
                recommendations[artist_name] = proximity
    return recommendations


# TODO не используется
def show_recommendations(
        seed_object: ArtistVisualNode,
        artist_pairs_proximity: dict,
        show_proximity=False) -> None:
    recommendations = get_recommendations(seed_object, artist_pairs_proximity)

    for recommendation_name, proximity in recommendations.items():
        if show_proximity:
            format_print([recommendation_name, proximity], [20, 5])
        else:
            print(recommendation_name)
