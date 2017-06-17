from . import vk


def get_mutual_friends(user_id: int):
    friends = vk.get_friends(user_id)

    mutual_ids = vk.get_mutual_friends_ids_batch([user.id for user in
                                                  friends], user_id)
    
    return friends, mutual_ids
