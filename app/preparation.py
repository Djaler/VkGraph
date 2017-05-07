from typing import Dict, Iterable, List

from .model import User


def prepare_nodes(users: Iterable[User]) -> List[Dict]:
    return [dict(id=user.id, name=user.name, photo=user.photo) for user in
            users]


def prepare_edges(mutual_friends: Dict[int, List[int]]):
    edges = []
    for friend_id, mutual_friends_ids in mutual_friends.items():
        for mutual_friend_id in mutual_friends_ids:
            if {"target": mutual_friend_id, "source": friend_id} not in edges:
                edges.append({"target": friend_id, "source": mutual_friend_id})
    
    return edges
