from hiphop_bot.recommender_system.proximity_measures import calc_generalizing_proximity_measure_for_all_leafs
from hiphop_bot.recommender_system.models.artist_pairs_proximity import ArtistsPairsProximityModel
from hiphop_bot.recommender_system.models.artist import ArtistModel
from hiphop_bot.recommender_system.tree.tree_loader import load_tree


def update_artist_pairs_proximity():
    tree = load_tree()
    artist_pairs_proximity = calc_generalizing_proximity_measure_for_all_leafs(tree)
    artists_pairs_proximity_model = ArtistsPairsProximityModel()
    artist_model = ArtistModel()

    artists = artist_model.get_all()
    artists_ids = {artist.name: artist.id for artist in artists}

    pairs_to_update = []

    for first_artist_name, pairs in artist_pairs_proximity.items():
        for pair_name, proximity_obj in pairs.items():
            db_obj = artists_pairs_proximity_model.get_by_artists_name(first_artist_name, pair_name)
            first_artist_id = artists_ids[first_artist_name]
            pair_artist_id = artists_ids[pair_name]
            if db_obj:
                if db_obj.general_proximity != proximity_obj.general_proximity:
                    pairs_to_update.append((first_artist_id, pair_artist_id, proximity_obj.general_proximity,
                                            proximity_obj.proximities_list))
            else:
                # добавляем новую запись в базу
                artists_pairs_proximity_model.add_record(
                    first_artist_id, pair_artist_id, proximity_obj.general_proximity, proximity_obj.proximities_list)
    if pairs_to_update:
        artists_pairs_proximity_model.update_multiple_proximities(pairs_to_update)


# update_artist_pairs_proximity()

