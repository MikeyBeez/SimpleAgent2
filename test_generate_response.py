import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from generate_response import generate_response
from chat_manager import ChatManager

class TestGenerateResponse(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    @patch('chat_manager.ChatManager.llm.agenerate_stream')  # Replace 'agenerate_stream' with the actual method name
    def test_generate_response(self, mock_stream, mock_stdout):
        chat_manager = ChatManager()
        mock_stream.return_value = ["This is ", "a test ", "response."]
        response = generate_response("Test question", "Test search results", chat_manager)
        self.assertEqual(response, "This is a test response.")

        # Check printed output
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "This is a test response.")

if __name__ == "__main__":
    unittest.main()
