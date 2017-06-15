from typing import Dict, List

from .user import User


class UsersGraph:
    def __init__(self, users: List[User], mutual_ids: Dict[int, List[int]]):
        self._friends = [user.to_json() for user in users]
        
        self._connections = []
        for friend_id, mutual_friends_ids in mutual_ids.items():
            for mutual_friend_id in mutual_friends_ids:
                if dict(target=mutual_friend_id,
                        source=friend_id) not in self._connections:
                    self._connections.append(dict(source=mutual_friend_id,
                                                  target=friend_id))
    
    def to_json(self):
        return dict(friends=self._friends, connections=self._connections)
