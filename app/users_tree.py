class Node:
    def __init__(self, id, parents=None):
        if parents is None:
            parents = []
        self._id = id
        self._parents = parents
    
    @property
    def id(self):
        return self._id
    
    @property
    def parents(self):
        return self._parents


class Tree:
    def __init__(self):
        self._indexes = []
        self._nodes = []
    
    def add(self, node: Node):
        self._indexes.append(node.id)
        self._nodes.append(node)
    
    def get_by_id(self, id: int) -> Node:
        return self._nodes[self._indexes.index(id)]
    
    def is_id_exists(self, id):
        return id in self._indexes
    
    @property
    def nodes(self):
        return self._nodes
