# entities_test.py
import unittest
from entities import Entities

class TestEntities(unittest.TestCase):
    def test_set_and_get_user_name(self):
        entities = Entities()
        entities.set_user_name("Alice")
        self.assertEqual(entities.get_user_name(), "Alice")

    def test_get_user_name_not_set(self):
        entities = Entities()
        self.assertIsNone(entities.get_user_name())

if __name__ == "__main__":
    unittest.main()
