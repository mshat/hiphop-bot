import json

genders = {'male': 0, 'female': 1}

themes = {'hard-gangsta': 0, 'workout': 1, 'soft-gangsta': 2, 'feelings': 3, 'fun': 4, 'art': 5, 'conscious': 6}

with open('genres.json', 'r', encoding='utf-8') as file:
    genres = json.load(file)
genres = {genre['name']: genre['id'] for genre in genres}

with open('artists_source.json', 'r', encoding='utf-8') as file:
    artists = json.load(file)

print(genres)
new_artists = []
for artist in artists:
    new_artists.append({
        'id': artist['id'],
        'name': artist['name'],
        'year_of_birth': artist['year_of_birth'],
        'group_members_num': artist['group_members_num'],
        'theme_id': themes[artist['theme']],
        'gender_id': genders[artist['sex']],
        'genre_id': genres[artist['genre']],
    })

print(artists)
print(new_artists)

with open('artists.json', 'w', encoding='utf-8') as file:
    json.dump(new_artists, file, ensure_ascii=False)
