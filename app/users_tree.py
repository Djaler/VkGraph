class Node:
    def __init__(self, user_id, parents=None):
        if parents is None:
            parents = []
        self._id = user_id
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

    def get_by_id(self, user_id: int) -> Node:
        return self._nodes[self._indexes.index(user_id)]

    def is_id_exists(self, user_id):
        return user_id in self._indexes
    
    @property
    def nodes(self):
        return self._nodes
