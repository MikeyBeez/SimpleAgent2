from search_logic import should_search
from context_manager import update_context
from skill_handler import handle_skills
from langchain_community.tools import DuckDuckGoSearchRun  # Import the search tool

class Router:
    """
    Determines the best approach to answering a user's question.
    """

    def __init__(self, llm, embeddings):
        self.llm = llm
        self.embeddings = embeddings
        self.chat_history_embeddings = []
        self.search = DuckDuckGoSearchRun() # Initialize the search object here

    def route(self, question, chat_history, available_skills):
        """
        Determines whether to search, use the knowledge base, or execute a skill.

        Args:
            question (str): The user's question.
            chat_history (str): The conversation history.
            available_skills (list): A list of available Skill objects.

        Returns:
            str: The response to the user.
        """
        if should_search(question, chat_history, self.llm, self.embeddings, self.chat_history_embeddings):
            # ... (Your logic for performing a web search)
            # Example (assuming you have a search object called `self.search`):
            search_results = self.search.run(question)
            return search_results
        elif handle_skills(question, chat_history, available_skills):
            # ... (Your logic for executing a skill)
            # Example: 
            return handle_skills(question, chat_history, available_skills) 
        else:
            # ... (Your logic for responding directly using the knowledge base)
            return "I don't know."  # Placeholder for knowledge base response

        # Update the context
        update_context(question, chat_history, self.embeddings, self.chat_history_embeddings)
