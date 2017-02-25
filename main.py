from typing import List

import vk_api

import settings

session = vk_api.VkApi(token=settings.access_token)
session.authorization()

vk = session.get_api()


def get_friends(user_id):
    response = vk.friends.get(user_id=user_id,
                              fields=['id', 'first_name', 'last_name',
                                      'photo'])
    
    return {friend['id']: friend for friend in response['items']}


def get_mutual_friends(users_ids: List[int], my_id):
    with vk_api.VkRequestsPool(session) as pool:
        response = pool.method_one_param(
            'friends.getMutual',
            key='target_uid',
            values=users_ids,
            default_values={'source_uid': my_id}
        )
    
    return response.result


if __name__ == '__main__':
    friends = get_friends(settings.my_id)
    
    mutual_friends = get_mutual_friends(list(friends.keys()), settings.my_id)
    
    print(mutual_friends)
