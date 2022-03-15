from collections import OrderedDict
from hiphop_bot.recommender_system.tree.artist_node import ArtistVisualNode
from hiphop_bot.recommender_system.proximity_measures import \
    calc_generalizing_proximity_measure_for_all_leafs
from hiphop_bot.recommender_system.tools import format_print
from hiphop_bot.recommender_system.config import MIN_SIMILARITY_PROXIMITY
from hiphop_bot.recommender_system.models.artist_pairs_proximity import ArtistPairsProximityModel
from hiphop_bot.recommender_system.tree.tree_loader import load_tree


# TODO дописать метод для записи в бд список близости артистов
def create_artist_pairs_proximity(tree):
    tree = load_tree()
    artist_pairs_proximity = calc_generalizing_proximity_measure_for_all_leafs(tree)

    # with open('data/artist_pairs_proximity.json', 'w') as file:
    #     json.dump(artist_pairs_proximity, file)
    pass


def load_artist_pairs_proximity() -> dict:
    artist_pairs_proximity_model = ArtistPairsProximityModel()
    res = artist_pairs_proximity_model.get_all()
    return res.artists_proximity


def get_recommendations(
        seed_object: ArtistVisualNode,
        artist_pairs_proximity: dict) -> OrderedDict[str, float]:
    artist_pairs = artist_pairs_proximity[seed_object.name]
    artist_pairs_sorted_by_proximity = OrderedDict(sorted(artist_pairs.items(), key=lambda item: item[1]))

    recommendations = OrderedDict()
    for artist_name, proximity in artist_pairs_sorted_by_proximity.items():
        if proximity <= MIN_SIMILARITY_PROXIMITY:
            if artist_name not in recommendations:
                recommendations[artist_name] = proximity
    return recommendations

