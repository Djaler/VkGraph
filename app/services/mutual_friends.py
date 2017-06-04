from colorsys import hsv_to_rgb

from ..services import vk
from ..utils import rgb_to_hex


def get_mutual_friends(user_id: int):
    friends = vk.get_friends(user_id)

    mutual_ids = vk.get_mutual_friends_ids_batch([user.id for user in
                                                  friends], user_id)
    
    connections_counts = [len(mutual_ids.get(user.id, [])) for user in
                          friends]
    interval = max(connections_counts) - min(connections_counts)
    
    for friend, connections_count in zip(friends, connections_counts):
        friend.color = _calculate_color(connections_count, interval)

    return friends, mutual_ids


def _calculate_color(connections_count, interval):
    try:
        hue = 240 - 240 * connections_count / interval
        return rgb_to_hex(*hsv_to_rgb(hue / 360, 1, 1))
    except ZeroDivisionError:
        return rgb_to_hex(1, 0, 0)
