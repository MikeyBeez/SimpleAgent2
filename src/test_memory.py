import unittest
from unittest.mock import MagicMock, ANY
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from memory import EmbeddingMemory

class MemoryTests(unittest.TestCase):

    def setUp(self):
        """Sets up the test environment."""
        # Create a mock vectorstore and LLM
        self.vectorstore = MagicMock(spec=Chroma)
        self.llm = MagicMock(spec=Ollama)

        # Set the _embedding_function attribute on the mock vectorstore
        self.vectorstore._embedding_function = MagicMock(spec=OllamaEmbeddings)

        # Initialize EmbeddingMemory with mocks
        self.memory = EmbeddingMemory(self.vectorstore, self.llm)

    def test_load_memory_variables(self):
        """Tests loading memory variables with chat history."""

        def mock_get_chat_history():
            return ["User: Hello", "Chatbot: Hi there!"]

        # Call load_memory_variables with the mock function
        context = self.memory.load_memory_variables(
            {"question": "What's up?"}, 
            mock_get_chat_history  # Pass the function as an argument
        )

        # Assertions
        self.assertEqual(context.get("history"), ["User: Hello", "Chatbot: Hi there!"])

        # (Optional): Assert that the vectorstore's similarity search was called 
        # self.vectorstore.similarity_search_by_vector.assert_called()

    def test_save_context(self):
        """Tests saving context to memory."""
        self.memory.save_context({"input": "What's the weather?"}, {"output": "Sunny today!"})

        # Assert that the vectorstore's add_texts method was called
        self.vectorstore.add_texts.assert_called_once_with(
            ['User: What\'s the weather?\nChatbot: Sunny today!'], 
            embeddings=ANY, 
            metadatas=[{'source': 'conversation'}]
        ) 

if __name__ == '__main__':
    unittest.main()
