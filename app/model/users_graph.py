from typing import Dict, List

from .user import User


class UsersGraph:
    def __init__(self, users: List[User], mutual_ids: Dict[int, List[int]]):
        self._users = users
        
        self._connections = []
        for user_id, mutual_friends_ids in mutual_ids.items():
            for mutual_friend_id in mutual_friends_ids:
                if dict(target=mutual_friend_id,
                        source=user_id) not in self._connections:
                    self._connections.append(dict(source=mutual_friend_id,
                                                  target=user_id))

    @property
    def users(self):
        return self._users

    @property
    def connections(self) -> List[Dict[int, int]]:
        return self._connections
    
    def to_json(self):
        return dict(friends=[user.to_json() for user in self._users],
                    connections=self._connections)
