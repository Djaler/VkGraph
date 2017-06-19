from typing import Dict, Iterable, List

from celery import group

from app import cache
from app.exceptions import NoUserException, UserDeactivatedException
from app.model import User
from app.utils import chunks
from . import tasks

_cache_timeout = 30 * 60


@cache.memoize(timeout=_cache_timeout)
def get_user(user_id) -> User:
    user = tasks.get_user.delay(user_id).get()
    if user is None:
        raise NoUserException
    elif 'deactivated' in user:
        raise UserDeactivatedException
    else:
        return User.from_vk_json(user)


@cache.memoize(timeout=_cache_timeout)
def get_users(user_ids: Iterable[int]) -> List[User]:
    users = tasks.get_users.delay(user_ids).get()
    
    return list(map(User.from_vk_json, users))


@cache.memoize(timeout=_cache_timeout)
def get_friends_count(user_id: int) -> int:
    return tasks.get_friends_count.delay(user_id).get()


@cache.memoize(timeout=_cache_timeout)
def get_friends(user_id: int) -> List[User]:
    friends = tasks.get_friends.delay(user_id).get()
    return list(map(User.from_vk_json, friends))


@cache.memoize(timeout=_cache_timeout)
def get_friends_ids(user_id: int) -> List[int]:
    return tasks.get_friends_ids.delay(user_id).get()


@cache.memoize(timeout=_cache_timeout)
def get_friends_ids_batch(user_ids: List[int]) -> List[List[int]]:
    job = group([tasks.get_friends_ids_batch.s(chunk) for chunk in
                 chunks(user_ids, 75)])
    
    result = job.apply_async().join()
    
    full_result = []
    
    for list_ in result:
        full_result.extend(list_)
    
    return full_result


@cache.memoize(timeout=_cache_timeout)
def get_mutual_friends_ids(user1: int, user2: int) -> List[int]:
    return tasks.get_mutual_friends_ids.delay(user1, user2).get()


@cache.memoize(timeout=_cache_timeout)
def get_mutual_friends_ids_batch(user_ids: List[int],
                                 my_id: int) -> Dict[int, List[int]]:
    job = group(
        [tasks.get_mutual_friends_ids_batch.s(chunk, my_id) for chunk in
         chunks(user_ids, 75)])
    
    result = job.apply_async().join()
    
    full_result = {int(key): value for dictionary in result for key, value in
                   dictionary.items()}
    
    return full_result
