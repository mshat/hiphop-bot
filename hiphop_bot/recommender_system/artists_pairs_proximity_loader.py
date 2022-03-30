from typing import List
from hiphop_bot.recommender_system.proximity_measures import calc_generalizing_proximity_measure
from hiphop_bot.recommender_system.models.artist_pairs_proximity import ArtistsPairsProximityModel
from hiphop_bot.recommender_system.models.recommender_system_artist import RecommenderSystemArtist


def update_artist_pairs_proximity(artists):
    artists_ids = {artist.name: artist.id for artist in artists}

    artists_pairs_proximity_model = ArtistsPairsProximityModel()

    recommender_system_artists: List[RecommenderSystemArtist] = list(map(RecommenderSystemArtist, artists))
    artist_pairs_proximity = calc_generalizing_proximity_measure(recommender_system_artists)

    pairs_to_update = []

    all_current_proximities = artists_pairs_proximity_model.get_artists_proximity_dict()
    for first_artist_name, pairs in artist_pairs_proximity.items():
        current_artist_pairs_proximities = all_current_proximities.get(first_artist_name)
        for pair_name, pair_proximity in pairs.items():
            first_artist_id = artists_ids[first_artist_name]
            pair_artist_id = artists_ids[pair_name]

            if not current_artist_pairs_proximities or pair_name not in current_artist_pairs_proximities:
                # добавляем новую запись в базу
                artists_pairs_proximity_model.add_record(
                    first_artist_id, pair_artist_id, pair_proximity.general_proximity, pair_proximity.proximities_list)
                continue

            current_pair_proximity = current_artist_pairs_proximities.get(pair_name)
            if current_pair_proximity and current_pair_proximity.general_proximity != pair_proximity.general_proximity:
                # обновляем существующую запись
                pairs_to_update.append((first_artist_id, pair_artist_id, pair_proximity.general_proximity,
                                        pair_proximity.proximities_list))

    if pairs_to_update:
        artists_pairs_proximity_model.update_multiple_proximities(pairs_to_update)


