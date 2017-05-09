import os
from typing import Dict, List

import vk_api

from .model import User

_default_user_fields = ['id', 'first_name', 'last_name', 'photo_200_orig']

token = os.environ.get("ACCESS_TOKEN")

_session = vk_api.VkApi()

_vk = _session.get_api()


def authorized_session():
    session = vk_api.VkApi(token=token)
    session.authorization()
    return session


def get_user(user_id, fields=None) -> User:
    if not fields:
        fields = _default_user_fields

    try:
        response = _vk.users.get(user_ids=user_id, fields=fields)
    except vk_api.ApiError:
        raise NoUserException
    else:
        if 'deactivated' in response[0]:
            raise UserDeactivatedException

        return User.from_vk_json(response[0])


def get_friends_count(user_id: int) -> int:
    response = _vk.friends.get(user_id=user_id)
    
    return response['count']


def get_friends(user_id: int, fields=None) -> List[User]:
    if not fields:
        fields = _default_user_fields
    
    response = _vk.friends.get(user_id=user_id, fields=fields)

    return list(map(User.from_vk_json, response['items']))


def get_mutual_friends_ids(users: List[User],
                           my_id: int) -> Dict[int, List[int]]:
    users_ids = [user.id for user in users]

    with vk_api.VkRequestsPool(authorized_session()) as pool:
        response = pool.method_one_param(
            'friends.getMutual',
            key='target_uid',
            values=users_ids,
            default_values={'source_uid': my_id}
        )
    
    return response.result


class NoUserException(Exception):
    pass


class UserDeactivatedException(Exception):
    pass
