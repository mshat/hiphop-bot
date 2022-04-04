from typing import List, Tuple, Dict
from copy import deepcopy
from hiphop_bot.base_models.abstract_model import Model, ModelError


class _GenreTreeConverter:
    """
    Класс для преобразования таблицы смежности (adjacency_table) в дерево, представленное в виде вложенных словарей
    И для обратного преобразования
    """
    adjacency_table: List[Tuple[str, str, str]] | None
    genre_tree: Dict[str, Dict] | None
    _parent_children_nodes: Dict[str, Dict] | None  # {parent: {child1: {}, child2: {}}, ...} (дети только 1 поколения!)
    _child_parent_nodes: Dict[str, str] | None  # {child1: parent1, child2: parent1, child 3: parent2, ...}

    def __init__(self, adjacency_table: List[Tuple[str, str, str]] = None, genre_tree: Dict[str, Dict] = None):
        assert adjacency_table or genre_tree
        self.adjacency_table = adjacency_table
        self.genre_tree = genre_tree
        self._parent_children_nodes = None
        self._child_parent_nodes = None

        if self.adjacency_table:
            self._parent_children_nodes = self._create_parent_children_nodes()
            self._child_parent_nodes = self._create_child_parent_nodes()

    def _create_parent_children_nodes(self) -> Dict[str, Dict]:
        parent_children_nodes: Dict[str, Dict] | Dict = {}
        for i, parent, child in self.adjacency_table:
            if parent in parent_children_nodes:
                parent_children_nodes[parent].update({child: {}})
            else:
                parent_children_nodes[parent] = {child: {}}
        return parent_children_nodes

    def _create_child_parent_nodes(self) -> Dict[str, str]:
        child_parent_nodes: Dict[str, str] | Dict = {}
        for i, parent, child in self.adjacency_table:
            child_parent_nodes[child] = parent
        return child_parent_nodes

    def create_tree_from_adjacency_table(self) -> Dict[str, Dict]:
        """
        Метод работает с полями:
        Словарь parent_children_nodes вида Dict[str, Dict], содержащий в качестве ключей родительские ноды,
        а в качестве значений ноды-дети первого поколения.
        Словарь child_parent_nodes вида Dict[str, str], содержащий в качестве ключей нод-детей, а в качестве
        значений - родителей этих детей.

        В ходе работы метод копирует parent_children_nodes в tree и далее работает с этим tree:
        Проходит по ключам tree (это родители n-го порядка) и находит те из них, которые являются детьми
        (являются ключами в child_parent_nodes). Дети этих родителей (которые для кого-то тоже являются детьми)
        добавляются tree в качестве детей 2-го и более порядков.
        Таким образом в словарь детей корневой ноды добавляются вложенные словари детей 2-го и более порядков.
        Затем из tree удаляются оставшиеся пары родитель-дети, которые были добавлены в корневую ноду и
        в результируещем словаре остаётся только корневая нода с вложенными детьми
        """
        if not self.adjacency_table:
            raise Exception('Converting is impossible because self.adjacency_table is None')

        # список пар родитель - дети, которые добавляются в tree как дети 2 и далее поколений
        # после выполнения алгоритма они останутся лежать в tree как отдельные элементы,
        # поэтому их надо будет удалить
        parent_names_to_remove = []

        tree = deepcopy(self._parent_children_nodes)
        for parent_name, children in tree.items():
            if parent_name in self._child_parent_nodes.keys():
                tree[self._child_parent_nodes[parent_name]][parent_name] = children
                parent_names_to_remove.append(parent_name)
        for parent_name in parent_names_to_remove:
            tree.pop(parent_name)

        self.genre_tree = tree
        return self.genre_tree

    def create_adjacency_table_from_tree(self):
        pass


class _GenreTree:
    tree_dict: Dict[str, Dict]

    def __init__(self, node_tree_dict: Dict[str, Dict]):
        self.tree_dict = node_tree_dict

    def __str__(self):
        return f'{self.tree_dict}'

    def __repr__(self):
        return f'GenreTree: root node: {list(self.tree_dict.keys())[0]}'


class GenreTreeModel(Model):
    def __init__(self):
        super().__init__('genres_adjacency_table', _GenreTree)

        self._get_all_query = (
            "SELECT gat.id, g1.name as parent_genre, g2.name as child_genre "
            f"FROM {self._table_name} as gat "
            "inner join genre as g1 on gat.parent_genre_node_id = g1.id "
            "inner join genre as g2 on gat.child_genre_node_id = g2.id "
        )

    def _convert_to_objects(self, raw_data: List[Tuple]) -> _GenreTree:
        """
        Преобразует список кортежей в объекты класса GenreTree
        """
        try:
            converter = _GenreTreeConverter(adjacency_table=raw_data)
            node_tree = converter.create_tree_from_adjacency_table()
            object_ = self._model_class(node_tree)
            return object_
        except TypeError as e:
            raise ModelError(f'Conversion type error: {e}')
        except Exception as e:
            raise ModelError(f'Unknown conversion error: {e}')

    def _select_model_objects(self, query) -> _GenreTree:
        raw_data = self._raw_select(query)
        object_ = self._convert_to_objects(raw_data)
        return object_

    # this method must be overridden because _select_model_objects is overridden
    def get_all(self) -> _GenreTree:
        artists = self._select_model_objects(self._get_all_query)
        return artists


