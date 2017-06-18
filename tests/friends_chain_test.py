from unittest.mock import MagicMock

from app.services import friends_chain

user1 = 1
user2 = 2


def test_empty_chain():
    friends_chain.vk.get_friends_ids = MagicMock(return_value=[user2])
    
    chain = friends_chain.find_chain(user1, user2)
    
    assert [] == chain


def test_chain_through_one():
    friends_chain.vk.get_friends_ids = MagicMock(return_value=[])
    friends_chain.vk.get_mutual_friends_ids = MagicMock(return_value=[3])
    
    chain = friends_chain.find_chain(user1, user2)
    
    assert [3] == chain


def test_normal_chain():
    friends_chain.vk.get_mutual_friends_ids = MagicMock(return_value=[])
    friends_chain.vk.get_friends_count = MagicMock(return_value=1)
    friends_chain.vk.get_friends_ids = MagicMock(
        side_effect=lambda *args: {(user1,): [3],
                                   (user2,): [4],
                                   (3,): [user1, 4],
                                   (4,): [user2, 3]}[args])
    
    chain = friends_chain.find_chain(user1, user2)
    
    assert [3, 4] == chain


def test_no_chain():
    friends_chain.vk.get_mutual_friends_ids = MagicMock(return_value=[])
    friends_chain.vk.get_friends_count = MagicMock(return_value=1)
    friends_chain.vk.get_friends_ids = MagicMock(
        side_effect=lambda *args: {(user1,): [3],
                                   (user2,): [4],
                                   (3,): [user1],
                                   (4,): [user2]}[args])
    
    chain = friends_chain.find_chain(user1, user2)
    
    assert None is chain


def test_reversed_chain():
    friends_chain.vk.get_mutual_friends_ids = MagicMock(return_value=[])
    friends_chain.vk.get_friends_count = MagicMock(return_value=1)
    friends_chain.vk.get_friends_ids = MagicMock(
        side_effect=lambda *args: {(user1,): [3, 5],
                                   (user2,): [4],
                                   (3,): [user1, 4],
                                   (4,): [user2, 3]}[args])
    
    chain = friends_chain.find_chain(user1, user2)
    
    assert [3, 4] == chain
