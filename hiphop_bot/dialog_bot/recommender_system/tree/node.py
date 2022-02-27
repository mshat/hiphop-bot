class Node:
    def __init__(self, val: int = 0, children: list = None):
        self.value = val
        self.children = children if children else []

    def add_child(self, node):
        self.children.append(node)

    @property
    def values_str(self):
        return str(self.value)

    @staticmethod
    def get_child_by_name(root, name):
        if root.value == name:
            return root
        if not root.children:
            return
        for child in root.children:
            res = Node.get_child_by_name(child, name)
            if res:
                return res

    @staticmethod
    def show_tree(root, spaces_num: int = 0):
        print(f"{'-' * spaces_num}{root.values_str}")
        if not root.children:
            return
        for child in root.children:
            Node.show_tree(child, spaces_num + 1)

    def __str__(self):
        return f'node {self.value}'



