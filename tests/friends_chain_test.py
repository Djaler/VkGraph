import unittest
from unittest.mock import MagicMock

from app.services import friends_chain


class FriendsChainTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user1 = 1
        cls.user2 = 2
        friends_chain.vk = MagicMock()
    
    def test_empty_chain(self):
        friends_chain.vk.get_friends_ids = MagicMock(return_value=[self.user2])
        
        chain = friends_chain.find_chain(self.user1, self.user2)
        
        self.assertEqual([], chain)
    
    def test_chain_through_one(self):
        friends_chain.vk.get_friends_ids = MagicMock(return_value=[])
        
        friends_chain.vk.get_mutual_friends_ids = MagicMock(return_value=[3])
        
        chain = friends_chain.find_chain(self.user1, self.user2)
        
        self.assertEqual([3], chain)
    
    def test_normal_chain(self):
        friends_chain.vk.get_mutual_friends_ids = MagicMock(return_value=[])
        
        friends_chain.vk.get_friends_count = MagicMock(return_value=1)
        
        friends_chain.vk.get_friends_ids = MagicMock(
            side_effect=lambda *args: {(self.user1,): [3],
                                       (self.user2,): [4],
                                       (3,): [self.user1, 4],
                                       (4,): [self.user2, 3]}[args])
        
        chain = friends_chain.find_chain(self.user1, self.user2)
        
        self.assertEqual([3, 4], chain)


if __name__ == '__main__':
    unittest.main()
