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
            commond_friends = [tree.get_by_id(friend) for friend in his_friends
                               if tree.is_id_exists(friend)]

            if commond_friends:
                commond_friends.sort(key=lambda node: len(node.parents))
                nearest = commond_friends[0]

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


def get_chain(user1: int, user2: int, max_length: int):
    if user2 in vk.get_friends_ids([user1])[0]:
        return []
    
    depth = (max_length + 1) / 2
    
    tree = _build_tree(user1, max_depth=ceil(depth))
    
    chain = _find_common_friend(user2, tree, max_depth=floor(depth))

    return chain if chain else None
