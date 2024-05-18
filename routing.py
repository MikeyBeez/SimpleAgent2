from prompts import SHOULD_SEARCH_PROMPT
from langchain_community.embeddings import OllamaEmbeddings  # Import OllamaEmbeddings
from scipy.spatial.distance import cosine

class Router:
    """
    Determines if a search is needed for a given question.
    """

    def __init__(self, llm):
        self.llm = llm
        self.should_search_prompt = SHOULD_SEARCH_PROMPT
        self.common_greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "good night", "goodbye", "bye", "see you later", "talk to you later"]
        self.simple_questions = ["how are you?", "what's up?", "how's it going?", "what's your name?", "what can you do?", "what's the time?"]
        self.embeddings = OllamaEmbeddings(model="mxbai-embed-large")  # Use OllamaEmbeddings
        self.chat_history_embeddings = [] 

    def should_search(self, question, chat_history):
        """
        Determines if a search is needed for the given question.

        Args:
            question (str): The user's question.
            chat_history (str): The conversation history.

        Returns:
            bool: True if a search is needed, False otherwise.
        """
        # Check for common greetings
        if question.lower() in self.common_greetings:
            return False  # No search needed

        # Check for simple questions
        if question.lower() in self.simple_questions:
            return False  # No search needed

        # Check for contextual similarity
        question_embedding = self.embeddings.embed_query(question)
        if self.chat_history_embeddings:
            # Calculate cosine similarity with chat history embeddings
            similarities = [1 - cosine(question_embedding, embedding) for embedding in self.chat_history_embeddings]
            # Find the most similar message
            most_similar_index = similarities.index(max(similarities))
            most_similar_score = similarities[most_similar_index]
            if most_similar_score > 0.8:  # Adjust threshold as needed
                return False  # No search needed, question is similar to previous questions

        # If none of the checks pass, use the LLM to determine if a search is needed
        response = self.llm.invoke(
            self.should_search_prompt.format(question=question, chat_history=chat_history)
        ).strip()
        return response.lower() == "yes" 

    def update_context(self, question, chat_history):
        """
        Updates the context vectorstore with the new question.
        """
        # Get the embedding for the new question
        question_embedding = self.embeddings.embed_query(question)
        self.chat_history_embeddings.append(question_embedding)
