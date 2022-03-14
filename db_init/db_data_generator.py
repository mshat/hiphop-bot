from typing import Dict, List
import json


genders = {'male': 0, 'female': 1}

themes = {'hard-gangsta': 0, 'workout': 1, 'soft-gangsta': 2, 'feelings': 3, 'fun': 4, 'art': 5, 'conscious': 6}

with open('artists.json', 'r', encoding='utf-8') as file:
    artists = json.load(file)
artists = {artist['name']: artist['id'] for artist in artists}

with open('artist_pairs_proximity_.json', 'r', encoding='utf-8') as file:
    artists_pairs_proximity = json.load(file)

with open('genres.json', 'r', encoding='utf-8') as file:
    genres = json.load(file)
genres = {genre['name']: genre['id'] for genre in genres}

with open('artists_source.json', 'r', encoding='utf-8') as file:
    artists_source = json.load(file)

with open('genres_source.json', 'r', encoding='utf-8') as file:
    genres_source = json.load(file)

with open('streaming_service_links_source.json', 'r', encoding='utf-8') as file:
    streaming_service_links_source = json.load(file)

with open('streaming_services.json', 'r', encoding='utf-8') as file:
    streaming_services = json.load(file)
streaming_services = {service['name']: service['id'] for service in streaming_services}


def genres_tree_hardcode_references():
    def get_all_nodes(root: Dict[str, Dict] | None, nodes: List[str] | List):
        if isinstance(root, dict):
            nodes += list(root.keys())
            for val in root.values():
                get_all_nodes(val, nodes)
        else:
            return nodes

    def get_node_children(root: Dict[str, Dict], target_node_name: str):
        for node_name in root.keys():
            if node_name == target_node_name:
                return root[node_name]
            res = get_node_children(root[node_name], target_node_name)
            if res:
                return res

    def create_adjacency_table(genre_nodes: list, source_genres: dict, genres_ids: Dict[str, int]) -> List[Dict]:
        adjacency_table = []

        nodes_children = {}
        for node in genre_nodes:
            res = get_node_children(source_genres, node)
            if res:
                nodes_children[node] = list(res.keys())

        i = 0
        for parent_node, children_nodes in nodes_children.items():
            for child_node in children_nodes:
                adjacency_table.append({
                    'id': i,
                    'parent_genre_node_id': genres_ids[parent_node],
                    'child_genre_node_id': genres_ids[child_node]
                })
                i += 1

        return adjacency_table

    genre_nodes = []
    get_all_nodes(genres_source, genre_nodes)

    with open('genres.json', 'r', encoding='utf-8') as file:
        genres = json.load(file)
    genres_ids = {genre['name']: genre['id'] for genre in genres}

    adjacency_table = create_adjacency_table(genre_nodes, genres_source, genres_ids)
    for line in adjacency_table:
        print(line)

    with open('genres_adjacency_table.json', 'w', encoding='utf-8') as file:
        json.dump(adjacency_table, file, ensure_ascii=False)


def artists_data_hardcode_genre_gender_theme_references():
    print(genres)
    new_artists = []
    for artist in artists_source:
        new_artists.append({
            'id': artist['id'],
            'name': artist['name'],
            'year_of_birth': artist['year_of_birth'],
            'group_members_num': artist['group_members_num'],
            'theme_id': themes[artist['theme']],
            'gender_id': genders[artist['sex']],
            'genre_id': genres[artist['genre']],
        })

    print(artists_source)
    print(new_artists)

    with open('artists.json', 'w', encoding='utf-8') as file:
        json.dump(new_artists, file, ensure_ascii=False)


def artist_pairs_proximity_hardcode_references():
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


def streaming_service_links_hardcode_references():
    print(streaming_service_links_source)
    streaming_service_links_db = []
    i = 0
    for streaming_service_item in streaming_service_links_source:
        artist_name = streaming_service_item['artist_name']
        service_name = streaming_service_item['service_name']
        link = streaming_service_item['link']
        db_line = {
            "id": i,
            "artist_id": artists[artist_name],
            "streaming_service_id": streaming_services[service_name],
            "link": link
        }
        streaming_service_links_db.append(db_line)
        i += 1
    print(streaming_service_links_db)

    with open('streaming_service_links.json', 'w', encoding='utf-8') as file:
        json.dump(streaming_service_links_db, file, ensure_ascii=False)


def main():
    # artist_pairs_proximity_hardcode_references()
    # artists_data_hardcode_genre_gender_theme_references()
    # genres_tree_hardcode_references()
    # streaming_service_links_hardcode_references()
    pass


if __name__ == '__main__':
    main()