from typing import Dict
from hiphop_bot.recommender_system.proximity_measures import \
    calc_generalizing_proximity_measure_for_all_leafs
from hiphop_bot.recommender_system.models.artist_pairs_proximity import ArtistPairsProximityModel
from hiphop_bot.recommender_system.tree.tree_loader import load_tree


# TODO дописать метод для записи в бд список близости артистов
def create_artist_pairs_proximity(tree):
    tree = load_tree()
    artist_pairs_proximity = calc_generalizing_proximity_measure_for_all_leafs(tree)

    # with open('data/artist_pairs_proximity.json', 'w') as file:
    #     json.dump(artist_pairs_proximity, file)
    pass


def load_artists_pairs_proximity() -> Dict[str, Dict[str, float]]:
    artist_pairs_proximity_model = ArtistPairsProximityModel()
    res = artist_pairs_proximity_model.get_all()
    return res.artists_proximity

