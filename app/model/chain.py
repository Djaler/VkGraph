from typing import List

from .user import User


class Chain:
    def __init__(self, users: List[User]):
        self._users = users
    
    def to_json(self):
        return [user.to_json() for user in self._users]
