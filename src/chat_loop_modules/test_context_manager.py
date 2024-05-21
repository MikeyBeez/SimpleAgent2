import unittest
from context_manager import update_context, get_chat_history, chat_history

class ContextManagerTests(unittest.TestCase):

    def setUp(self):
        """Clears the chat history before each test."""
        global chat_history  # Access the global chat_history variable
        chat_history.clear()

    def test_update_context(self):
        """Tests that update_context adds messages to history and updates the vectorstore."""
        update_context("What is the capital of France?", "Paris is the capital of France.")
        update_context("How are you?", "I am an AI, so I don't have feelings, but I'm here to help!")

        # Check if the chat history is updated correctly
        expected_history = [
            "User: What is the capital of France?",
            "Agent: Paris is the capital of France.",
            "User: How are you?",
            "Agent: I am an AI, so I don't have feelings, but I'm here to help!"
        ]
        self.assertEqual(get_chat_history(), expected_history)

        # (Optional) Add assertions to check the vectorstore content 
        # You'll need to access the vectorstore and verify 
        # that the embeddings and metadata are added correctly.

    def test_get_chat_history(self):
        """Tests that get_chat_history returns the correct history."""
        # Add some test data to the chat history
        update_context("Test Question 1", "Test Answer 1")
        update_context("Test Question 2", "Test Answer 2")

        expected_history = [
            "User: Test Question 1",
            "Agent: Test Answer 1",
            "User: Test Question 2",
            "Agent: Test Answer 2"
        ]
        self.assertEqual(get_chat_history(), expected_history)

if __name__ == '__main__':
    unittest.main()
