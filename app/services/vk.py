import os
from typing import Dict, List, SupportsInt

import vk_api

from .. import app, cache
from ..model import User
from ..utils import chunks

_default_user_fields = ['id', 'first_name', 'last_name', 'photo_200_orig']

token = os.environ.get("ACCESS_TOKEN")

_incognito_api = vk_api.VkApi().get_api()

_authorized_session = vk_api.VkApi(token=token)
_authorized_session.authorization()
_authorized_api = _authorized_session.get_api()

_cache_timeout = app.config.get("CACHE_TIMEOUT")


@cache.memoize(timeout=_cache_timeout)
def get_user(user_id) -> User:
    try:
        response = _incognito_api.users.get(user_ids=user_id,
                                            fields=_default_user_fields,
                                            lang="ru")
    except vk_api.ApiError:
        raise NoUserException
    else:
        if 'deactivated' in response[0]:
            raise UserDeactivatedException

        return User.from_vk_json(response[0])


@cache.memoize(timeout=_cache_timeout)
def get_friends_count(user_id: int) -> int:
    response = _incognito_api.friends.get(user_id=user_id)
    
    return response['count']


@cache.memoize(timeout=_cache_timeout)
def get_friends(user_id: int) -> List[User]:
    response = _incognito_api.friends.get(user_id=user_id,
                                          fields=_default_user_fields,
                                          lang="ru")
    
    return list(map(User.from_vk_json, response['items']))


@cache.memoize(timeout=_cache_timeout)
def get_friends_ids(users_ids: List[SupportsInt]) -> List[List[int]]:
    user_ids_str = list(map(str, users_ids))
    
    result = []
    for chunk in chunks(user_ids_str, 25):
        response = _authorized_api.execute.friends(targets=",".join(chunk))
        result.extend(response)
    
    return result


@cache.memoize(timeout=_cache_timeout)
def get_mutual_friends_ids(users_ids: List[SupportsInt],
                           my_id: int) -> Dict[int, List[int]]:
    with vk_api.VkRequestsPool(_authorized_session) as pool:
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
