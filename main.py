from typing import Dict, Iterable, List

import vk_api

import settings

session = vk_api.VkApi(token=settings.access_token)
session.authorization()

vk = session.get_api()


class User:
    def __init__(self, id, first_name, last_name, photo):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._photo = photo
    
    @staticmethod
    def from_json(json):
        return User(json['id'], json['first_name'], json['last_name'],
                    json['photo'])
    
    @property
    def id(self):
        return self._id


def get_friends(user_id, fields=None) -> Iterable[User]:
    if fields is None:
        fields = ['id', 'first_name', 'last_name', 'photo']
    
    response = vk.friends.get(user_id=user_id, fields=fields)
    
    return map(User.from_json, response['items'])


def get_mutual_friends(users_ids: List[int], my_id) -> Dict[int, List[int]]:
    with vk_api.VkRequestsPool(session) as pool:
        response = pool.method_one_param(
            'friends.getMutual',
            key='target_uid',
            values=users_ids,
            default_values={'source_uid': my_id}
        )
    
    return response.result


if __name__ == '__main__':
    friends = {user.id: user for user in get_friends(settings.my_id)}
    
    mutual_friends = get_mutual_friends(list(friends.keys()), settings.my_id)
    
    print(mutual_friends)
