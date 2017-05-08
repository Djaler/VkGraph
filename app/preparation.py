from typing import Dict, Iterable, List

from .model import User


def prepare_user(user: User) -> Dict:
    return dict(id=user.id, name=user.name, photo=user.photo)


def prepare_users(users: Iterable[User]) -> List[Dict]:
    return list(map(prepare_user, users))


def prepare_friends_connections(mutual_friends: Dict[int, List[int]]):
    connections = []
    for friend_id, mutual_friends_ids in mutual_friends.items():
        for mutual_friend_id in mutual_friends_ids:
            if dict(target=mutual_friend_id,
                    source=friend_id) not in connections:
                connections.append(dict(source=mutual_friend_id,
                                        target=friend_id))
    
    return connections
