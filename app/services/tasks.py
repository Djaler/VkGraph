import os
from typing import Dict, Iterable, List, Optional

import vk_api
from vk_api.vk_api import VkApiMethod

from app import celery
from app.utils import chunks

token = os.environ.get("ACCESS_TOKEN")

_incognito_api = vk_api.VkApi().get_api()

_authorized_session = vk_api.VkApi(token=token)
_authorized_session.auth()
_authorized_api = _authorized_session.get_api()

_default_user_fields = ['id', 'first_name', 'last_name', 'photo_100', 'domain']

VkApiMethod.__call__ = lambda self, **kwargs: self._vk.method(self._method, {
    key: ",".join(value) if isinstance(value, list) else value
    for key, value in kwargs.items()})


@celery.task()
def get_user(user_id) -> Optional[dict]:
    try:
        response = _authorized_api.users.get(user_ids=user_id,
                                             fields=_default_user_fields,
                                             lang="ru")
    except vk_api.ApiError:
        return None
    else:
        return response[0]


@celery.task()
def get_users(user_ids: Iterable[int]) -> List[dict]:
    user_ids_str = list(map(str, user_ids))
    response = _authorized_api.users.get(user_ids=user_ids_str,
                                         fields=_default_user_fields,
                                         lang="ru")
    
    return response


@celery.task()
def get_friends_count(user_id: int) -> int:
    response = _incognito_api.friends.get(user_id=user_id)
    
    return response['count']


@celery.task()
def get_friends(user_id: int) -> List[dict]:
    response = _authorized_api.friends.get(user_id=user_id,
                                           fields=_default_user_fields,
                                           lang="ru")
    
    return response['items']


@celery.task()
def get_friends_ids(user_id: int) -> List[int]:
    response = _authorized_api.friends.get(user_id=user_id)
    
    return response['items']


@celery.task()
def get_friends_ids_batch(user_ids: Iterable[int]) -> List[List[int]]:
    user_ids_str = list(map(str, user_ids))
    
    result = []
    for chunk in chunks(user_ids_str, 25):
        response = _authorized_api.execute.friends(targets=chunk)
        result.extend(response)
    
    return result


@celery.task()
def get_mutual_friends_ids(user1: int, user2: int) -> List[int]:
    return _authorized_api.friends.getMutual(target_uid=user1,
                                             source_uid=user2)


@celery.task()
def get_mutual_friends_ids_batch(user_ids: List[int],
                                 my_id: int) -> Dict[int, List[int]]:
    with vk_api.VkRequestsPool(_authorized_session) as pool:
        response = pool.method_one_param(
            'friends.getMutual',
            key='target_uid',
            values=user_ids,
            default_values={'source_uid': my_id}
        )
    
    return response.result
