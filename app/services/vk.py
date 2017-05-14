import os
from typing import Dict, List

import vk_api
from celery import group

from .. import app, cache, celery
from ..model import User
from ..utils import chunks

token = os.environ.get("ACCESS_TOKEN")

_incognito_api = vk_api.VkApi().get_api()

_authorized_session = vk_api.VkApi(token=token)
_authorized_session.authorization()
_authorized_api = _authorized_session.get_api()

_cache_timeout = app.config.get("CACHE_TIMEOUT")
_default_user_fields = ['id', 'first_name', 'last_name', 'photo_100']


@celery.task()
def get_friends_ids_task(user_ids: List[int]) -> List[List[int]]:
    user_ids_str = list(map(str, user_ids))
    
    result = []
    for chunk in chunks(user_ids_str, 25):
        response = _authorized_api.execute.friends(targets=",".join(chunk))
        result.extend(response)
    
    return result


@celery.task()
def get_mutual_friends_ids_task(user_ids: List[int],
                                my_id: int) -> Dict[int, List[int]]:
    with vk_api.VkRequestsPool(_authorized_session) as pool:
        response = pool.method_one_param(
            'friends.getMutual',
            key='target_uid',
            values=user_ids,
            default_values={'source_uid': my_id}
        )
    
    return response.result


@cache.memoize(timeout=_cache_timeout)
def get_user(user_id) -> User:
    try:
        response = _authorized_api.users.get(user_ids=user_id,
                                             fields=_default_user_fields,
                                             lang="ru")
    except vk_api.ApiError:
        raise NoUserException
    else:
        if 'deactivated' in response[0]:
            raise UserDeactivatedException

        return User.from_vk_json(response[0])


@cache.memoize(timeout=_cache_timeout)
def get_users(user_ids: List[int]) -> List[User]:
    user_ids_str = list(map(str, user_ids))
    response = _authorized_api.users.get(user_ids=",".join(user_ids_str),
                                         fields=_default_user_fields,
                                         lang="ru")
    
    return list(map(User.from_vk_json, response))


@cache.memoize(timeout=_cache_timeout)
def get_friends_count(user_id: int) -> int:
    response = _incognito_api.friends.get(user_id=user_id)
    
    return response['count']


@cache.memoize(timeout=_cache_timeout)
def get_friends(user_id: int) -> List[User]:
    response = _authorized_api.friends.get(user_id=user_id,
                                           fields=_default_user_fields,
                                           lang="ru")
    
    return list(map(User.from_vk_json, response['items']))


@cache.memoize(timeout=_cache_timeout)
def get_friends_ids(user_ids: List[int]) -> List[List[int]]:
    job = group([get_friends_ids_task.s(chunk) for chunk in
                 chunks(user_ids, 75)])

    result = job.apply_async().join()

    full_result = []

    for list_ in result:
        full_result.extend(list_)

    return full_result


@cache.memoize(timeout=_cache_timeout)
def get_mutual_friends_ids(user_ids: List[int],
                           my_id: int) -> Dict[int, List[int]]:
    job = group([get_mutual_friends_ids_task.s(chunk, my_id) for chunk in
                 chunks(user_ids, 75)])
    
    result = job.apply_async().join()

    full_result = {int(key): value for dictionary in result for key, value in
                   dictionary.items()}

    return full_result


class NoUserException(Exception):
    pass


class UserDeactivatedException(Exception):
    pass
