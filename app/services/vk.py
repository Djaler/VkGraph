import os
from typing import Dict, Iterable, List, Optional

import vk_api
from celery import group

from .. import app, cache, celery
from ..model import User
from ..utils import chunks

token = os.environ.get("ACCESS_TOKEN")

_incognito_api = vk_api.VkApi().get_api()

_authorized_session = vk_api.VkApi(token=token)
_authorized_session.auth()
_authorized_api = _authorized_session.get_api()

_cache_timeout = app.config.get("CACHE_TIMEOUT")
_default_user_fields = ['id', 'first_name', 'last_name', 'photo_100']


@cache.memoize(timeout=_cache_timeout)
def get_user(user_id) -> User:
    user = _get_user_task.delay(user_id).get()
    if user is None:
        raise NoUserException
    elif 'deactivated' in user:
        raise UserDeactivatedException
    else:
        return User.from_vk_json(user)


@celery.task()
def _get_user_task(user_id) -> Optional[dict]:
    try:
        response = _authorized_api.users.get(user_ids=user_id,
                                             fields=_default_user_fields,
                                             lang="ru")
    except vk_api.ApiError:
        return None
    else:
        return response[0]


@cache.memoize(timeout=_cache_timeout)
def get_users(user_ids: Iterable[int]) -> List[User]:
    users = _get_users_task.delay(user_ids).get()
    
    return list(map(User.from_vk_json, users))


@celery.task()
def _get_users_task(user_ids: Iterable[int]) -> List[dict]:
    user_ids_str = list(map(str, user_ids))
    response = _authorized_api.users.get(user_ids=",".join(user_ids_str),
                                         fields=_default_user_fields,
                                         lang="ru")

    return response


@cache.memoize(timeout=_cache_timeout)
def get_friends_count(user_id: int) -> int:
    return _get_friends_count_task.delay(user_id).get()


@celery.task()
def _get_friends_count_task(user_id: int) -> int:
    response = _incognito_api.friends.get(user_id=user_id)
    
    return response['count']


@cache.memoize(timeout=_cache_timeout)
def get_friends(user_id: int) -> List[User]:
    friends = _get_friends_task.delay(user_id).get()
    return list(map(User.from_vk_json, friends))


@celery.task()
def _get_friends_task(user_id: int) -> List[dict]:
    response = _authorized_api.friends.get(user_id=user_id,
                                           fields=_default_user_fields,
                                           lang="ru")

    return response['items']


@cache.memoize(timeout=_cache_timeout)
def get_friends_ids(user_ids: List[int]) -> List[List[int]]:
    job = group([_get_friends_ids_task.s(chunk) for chunk in
                 chunks(user_ids, 75)])
    
    result = job.apply_async().join()
    
    full_result = []
    
    for list_ in result:
        full_result.extend(list_)
    
    return full_result


@celery.task()
def _get_friends_ids_task(user_ids: Iterable[int]) -> List[List[int]]:
    user_ids_str = list(map(str, user_ids))
    
    result = []
    for chunk in chunks(user_ids_str, 25):
        response = _authorized_api.execute.friends(targets=",".join(chunk))
        result.extend(response)
    
    return result


@cache.memoize(timeout=_cache_timeout)
def get_mutual_friends_ids(user_ids: List[int],
                           my_id: int) -> Dict[int, List[int]]:
    job = group([_get_mutual_friends_ids_task.s(chunk, my_id) for chunk in
                 chunks(user_ids, 75)])
    
    result = job.apply_async().join()
    
    full_result = {int(key): value for dictionary in result for key, value in
                   dictionary.items()}
    
    return full_result


@celery.task()
def _get_mutual_friends_ids_task(user_ids: List[int],
                                 my_id: int) -> Dict[int, List[int]]:
    with vk_api.VkRequestsPool(_authorized_session) as pool:
        response = pool.method_one_param(
            'friends.getMutual',
            key='target_uid',
            values=user_ids,
            default_values={'source_uid': my_id}
        )
    
    return response.result


class NoUserException(Exception):
    pass


class UserDeactivatedException(Exception):
    pass
