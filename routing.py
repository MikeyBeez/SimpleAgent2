from prompts import SHOULD_SEARCH_PROMPT
from langchain_community.vectorstores import FAISS # Import FAISS from langchain_community
from sentence_transformers import SentenceTransformer  

class Router:
    """
    Determines if a search is needed for a given question.
    """

    def __init__(self, llm):
        self.llm = llm
        self.should_search_prompt = SHOULD_SEARCH_PROMPT
        self.common_greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "good night", "goodbye", "bye", "see you later", "talk to you later"]
        self.simple_questions = ["how are you?", "what's up?", "how's it going?", "what's your name?", "what can you do?", "what's the time?"]
        self.embeddings = SentenceTransformer("all-mpnet-base-v2")
        self.vectorstore = None 

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
        if self.vectorstore:
            # Find semantically similar questions in the conversation history
            similar_questions = self.vectorstore.similarity_search_with_score(question, k=3)
            for similar_question, score in similar_questions:
                if score > 0.8:  # Adjust threshold as needed
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
        if not self.vectorstore:
            self.vectorstore = FAISS.from_texts([chat_history], self.embeddings)
        else:
            self.vectorstore.add_texts([question], self.embeddings)
