from hiphop_bot.recommender_system.tree.node import Node


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


def calc_distance_between_nodes(root, node1: Node, node2: Node):
    if root:
        path1 = find_path_to_node(root, [], node1.value)
        path2 = find_path_to_node(root, [], node2.value)

        i = 0
        while i < len(path1) and i < len(path2):
            if path1[i] != path2[i]:
                break
            i = i + 1

        distance = len(path1) + len(path2) - 2 * i
        return distance
    else:
        raise Exception('Root arg is None')

