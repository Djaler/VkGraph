from typing import Dict, List, Set

from .user import User


class UsersGraph:
    def __init__(self, users: List[User], mutual_ids: Dict[int, List[int]]):
        self._users = users
        
        self._connections = []
        for user_id, mutual_friends_ids in mutual_ids.items():
            for mutual_friend_id in mutual_friends_ids:
                self.add_connection(user_id, mutual_friend_id)

    def add_connection(self, user_id1, user_id2):
        connection = {user_id1, user_id2}
        if connection not in self._connections:
            self._connections.append(connection)
    
    @property
    def users(self):
        return self._users

    @property
    def connections(self) -> List[Set[int]]:
        return self._connections
    
    def to_json(self):
        return dict(friends=[user.to_json() for user in self._users],
                    connections=[
                        dict(source=min(connection), target=max(connection))
                        for connection in self._connections])
