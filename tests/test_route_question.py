import unittest
from unittest.mock import MagicMock
from route_question import route_question
from chat_manager import ChatManager

class TestRouteQuestion(unittest.TestCase):
    def test_route_question(self):
        chat_manager = ChatManager()
        chat_manager.router.route = MagicMock(return_value="Test response")  # Mock the route method
        response = route_question("Test question", chat_manager)
        self.assertEqual(response, "Test response")
        chat_manager.router.route.assert_called_once_with(
            "Test question", [], chat_manager.available_skills  # Pass the expected arguments
        )

if __name__ == "__main__":
    unittest.main()
