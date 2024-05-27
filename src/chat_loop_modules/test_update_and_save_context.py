import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import unittest
from unittest.mock import MagicMock, patch
# Assume this file is in the same package as context_manager module for proper relative imports
from context_manager import update_and_save_context

class TestUpdateAndSaveContext(unittest.TestCase):
    @patch('context_manager.update_context')
    @patch('context_manager.ChatManager.memory.save_context')
    def test_update_and_save_context(self, mock_save_context, mock_update_context):
        user_input = "Test input"
        response = "Test response"

        # Set up the logging calls to be asserted in our tests
        logger_mock = MagicMock()
        update_and_save_context(user_input, response)

        # Assert that update_context was called with correct parameters
        mock_update_context.assert_called_once_with({"input": user_input, "output": response})

        # Assert save_context method of ChatManager is called with the same context data
        mock_save_context.assert_called_once_with({"input": user_input, "output": response})

        # Test that logging information was printed as expected
        logger_mock.info.assert_called()
        self.assertEqual(logger_mock.info.call_args[0][0], f'Context updated with input: {user_input} and output: {response}')
        logger_mock.info.assert_called()
        self_assertEqual(logger_mock.info.call_args[0][0], 'Context saved successfully.')

if __name__ == '__main__':
    unittest.main()
