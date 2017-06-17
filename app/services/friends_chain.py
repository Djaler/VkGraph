from math import ceil, floor
from typing import List, Optional, SupportsInt

from . import vk


class _Node:
    def __init__(self, user_id: int, parents: List[int] = None):
        if parents is None:
            parents = []
        self._id = user_id
        self._parents = parents
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def parents(self) -> List[int]:
        return self._parents


class _Tree(dict):
    def add(self, node: _Node):
        self[node.id] = node
    
    def get_by_id(self, user_id: int) -> _Node:
        return self[user_id]
    
    def is_id_exists(self, user_id: int):
        return user_id in self
    
    @property
    def nodes(self) -> List[_Node]:
        return list(self.values())


def _build_tree(root_id: int, max_depth: SupportsInt) -> _Tree:
    tree = _Tree()
    tree.add(_Node(root_id))
    
    def add_next_level(prev_level: List[int], depth: int, parents: List[int]):
        if len(prev_level) == 1:
            friends = [vk.get_friends_ids(prev_level[0])]
        else:
            friends = vk.get_friends_ids_batch(prev_level)
        
        for user, his_friends in zip(prev_level, friends):
            for friend in his_friends:
                tree.add(_Node(friend, parents + [user]))
            
            if depth != max_depth:
                add_next_level(his_friends, depth + 1, parents + [user])
    
    add_next_level([root_id], 2, [])
    
    return tree


def _find_common_friend(root_id: int, tree: _Tree,
                        max_depth: SupportsInt) -> Optional[List[int]]:
    def check_next_level(prev_level: List[int], depth: int,
                         parents: List[int]) -> Optional[List[int]]:
        if len(prev_level) == 1:
            friends = [vk.get_friends_ids(prev_level[0])]
        else:
            friends = vk.get_friends_ids_batch(prev_level)
        
        for user, his_friends in zip(prev_level, friends):
            common_friends = [tree.get_by_id(friend) for friend in his_friends
                              if tree.is_id_exists(friend)]

            if common_friends:
                common_friends.sort(key=lambda node: len(node.parents))
                nearest = common_friends[0]
                
                chain = nearest.parents[1:]
                chain.append(nearest.id)
                if depth > 2:
                    chain.append(user)
                chain.extend(reversed(parents[1:]))

                return chain
        
        for user, his_friends in zip(prev_level, friends):
            if depth != max_depth:
                result = check_next_level(his_friends, depth + 1,
                                          parents + [user])
                if result:
                    return result
        
        return None
    
    return check_next_level([root_id], 2, [])


def find_chain(user1: int, user2: int,
               max_length: int = 5) -> Optional[List[int]]:
    user1_friends = vk.get_friends_ids(user1)
    if user2 in user1_friends:
        return []
    
    mutual_friends = vk.get_mutual_friends_ids(user1, user2)
    if mutual_friends:
        return [mutual_friends[0]]
    
    depth = (max_length + 1) / 2
    
    user1_friends_count = len(user1_friends)
    user2_friends_count = vk.get_friends_count(user2)
    
    if user2_friends_count < user1_friends_count:
        user1, user2 = user2, user1

    tree = _build_tree(user1, max_depth=floor(depth))

    chain = _find_common_friend(user2, tree, max_depth=ceil(depth))
    
    if not chain:
        return None
    
    if user2_friends_count < user1_friends_count:
        chain = list(reversed(chain))
    
    return chain
