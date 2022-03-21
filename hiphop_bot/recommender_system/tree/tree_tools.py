from hiphop_bot.recommender_system.tree.node import Node
from hiphop_bot.recommender_system.tree.artist_node import ArtistNode


def find_path_to_node(root: Node, path: list, node_name: str):
    if root is None:
        return

    path.append(root.value)

    if root.value == node_name:
        return path

    for child in root.children:
        if find_path_to_node(child, path, node_name):
            return path

    path.pop()
    return


def calc_distance_between_nodes(root, node_name1: str, node_name2: str):
    if root:
        path1 = find_path_to_node(root, [], node_name1)
        path2 = find_path_to_node(root, [], node_name2)

        i = 0
        while i < len(path1) and i < len(path2):
            if path1[i] != path2[i]:
                break
            i = i + 1

        return len(path1) + len(path2) - 2 * i
    else:
        return 0


def calc_distance_between_all_nodes(tree: Node, leafs: list):
    distances_between_nodes = {}
    i = 0
    for leaf1 in leafs:
        for leaf2 in leafs:
            if leaf1 != leaf2:
                distance_between_nodes = calc_distance_between_nodes(tree, leaf1.name, leaf2.name)
                distances_between_nodes.update(
                    {f'pair{i}': {'artist1': leaf1.name, 'artist2': leaf2.name, 'distance': distance_between_nodes}}
                )
                i += 1

    return distances_between_nodes


def calc_max_distance_between_nodes_optimized(distances_between_nodes: dict):
    max_distance = 0
    for pair_data in distances_between_nodes.values():
        if pair_data['distance'] > max_distance:
            max_distance = pair_data['distance']
    return max_distance


def get_leafs_values(root: Node, leafs: list):
    if not root.children:
        return root
    for child in root.children:
        res = get_leafs_values(child, leafs)
        if res and isinstance(res, ArtistNode):
            leafs.append(res)
