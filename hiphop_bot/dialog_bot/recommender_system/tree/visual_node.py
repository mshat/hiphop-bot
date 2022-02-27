import graphviz
import string
from .node import Node


def infinite_sequence():
    num = 0
    while True:
        yield string.printable[num]
        num += 1
        assert num <= 100


NAME_GEN = infinite_sequence()
DOT = graphviz.Graph(format='png')


class VisualNode(Node):
    def __init__(self, val: int = 0, children: list = None):
        super().__init__(val, children)
        self.dot = DOT
        self.dot_name = next(NAME_GEN)
        self.dot.node(self.dot_name, self.values_str)
        if self.children:
            for child in self.children:
                self._add_edge(child)

    def _add_edge(self, child):
        self.dot.edges([f'{self.dot_name}{child.dot_name}'])

    def render_tree(self):
        self.dot.render(directory='doctest-output')

    def add_child(self, node):
        super(VisualNode, self).add_child(node)
        self._add_edge(node)

