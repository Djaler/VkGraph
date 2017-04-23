import os
from typing import Dict, Iterable, List

import vk_api

from .model import User

token = os.environ.get("ACCESS_TOKEN")

_session = vk_api.VkApi(token=token)
_session.authorization()

_vk = _session.get_api()


def get_user(user_id) -> User:
    try:
        response = _vk.users.get(user_ids=user_id, fields=['id',
                                                           'first_name',
                                                           'last_name',
                                                           'photo_200_orig'])
    except vk_api.ApiError:
        raise NoUserException
    else:
        return User.from_json(response[0])


def get_friends(user_id: int, fields=None) -> Iterable[User]:
    if not fields:
        fields = ['id', 'first_name', 'last_name', 'photo_200_orig']
    
    response = _vk.friends.get(user_id=user_id, fields=fields)
    
    return map(User.from_json, response['items'])


def get_mutual_friends(users_ids: List[int],
                       my_id: int) -> Dict[int, List[int]]:
    with vk_api.VkRequestsPool(_session) as pool:
        response = pool.method_one_param(
            'friends.getMutual',
            key='target_uid',
            values=users_ids,
            default_values={'source_uid': my_id}
        )
    
    return response.result


class NoUserException(Exception):
    pass
