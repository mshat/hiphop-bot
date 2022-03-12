from typing import Dict, List
import json


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


def main():
    with open('genres_source.json', 'r', encoding='utf-8') as file:
        genres_source = json.load(file)

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


if __name__ == '__main__':
    main()
