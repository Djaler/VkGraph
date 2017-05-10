from math import ceil, floor
from typing import List, SupportsInt

from . import vk
from ..users_tree import Node, Tree


def _build_tree(root_id: int, max_depth: SupportsInt) -> Tree:
    tree = Tree()
    tree.add(Node(root_id))
    
    def add_next_level(prev_level: List[int], depth: int, parents: List[int]):
        friends = vk.get_friends_ids(prev_level)
        for user, his_friends in zip(prev_level, friends):
            for friend in his_friends:
                tree.add(Node(friend, parents + [user]))
            
            if depth != max_depth:
                add_next_level(his_friends, depth + 1, parents + [user])
    
    add_next_level([root_id], 2, [])
    
    return tree


def _find_common_friend(root_id: int, tree: Tree, max_depth: SupportsInt):
    def check_next_level(prev_level: List[int], depth: int,
                         parents: List[int]):
        friends = vk.get_friends_ids(prev_level)
        for user, his_friends in zip(prev_level, friends):
            for friend in his_friends:
                if tree.is_id_exists(friend):
                    return friend, parents + [user]
        
        for user, his_friends in zip(prev_level, friends):
            if depth != max_depth:
                result = check_next_level(his_friends, depth + 1,
                                          parents + [user])
                if result:
                    return result
        
        return None
    
    return check_next_level([root_id], 2, [])


def get_friends_chain(user1: int, user2: int, max_length: int):
    depth = (max_length + 1) / 2
    
    tree = _build_tree(user1, max_depth=ceil(depth))
    
    result = _find_common_friend(user2, tree, max_depth=floor(depth))
    
    if not result:
        return None
    
    friend, parents = result
    
    return (
        *tree.get_by_id(friend).parents[1:], friend, *reversed(parents)[:-1])
