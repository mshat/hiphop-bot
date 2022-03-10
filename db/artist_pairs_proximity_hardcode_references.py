import json

with open('artists.json', 'r', encoding='utf-8') as file:
    artists = json.load(file)
artists = {artist['name']: artist['id'] for artist in artists}

with open('artist_pairs_proximity_.json', 'r', encoding='utf-8') as file:
    artists_pairs_proximity = json.load(file)

artists_pairs_proximity_for_db = []

i = 0
for first_artist, pairs_proximity in artists_pairs_proximity.items():
    for second_artist, proximity in pairs_proximity.items():
        artists_pairs_proximity_for_db.append(
            {'id': i, 'first_artist_id': artists[first_artist], 'second_artist_id': artists[second_artist], 'proximity': proximity}
        )
        i += 1

print(artists_pairs_proximity_for_db)

with open('artist_pairs_proximity.json', 'w', encoding='utf-8') as file:
    json.dump(artists_pairs_proximity_for_db, file, ensure_ascii=False)
