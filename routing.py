from search_logic import should_search
from context_manager import update_context
from skill_handler import handle_skills
from langchain_community.tools import DuckDuckGoSearchRun 

class Router:
    """
    Determines the best approach to answering a user's question.
    """

    def __init__(self, llm, embeddings):
        self.llm = llm
        self.embeddings = embeddings
        self.chat_history_embeddings = []
        self.search = DuckDuckGoSearchRun() 

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
        print(f"Question received in route(): {question}") 

        if question.lower().startswith("assistant"): 
            print("Wakeword detected!")
            # Remove punctuation and split the command
            command = question.split("assistant", 1)[1].strip().lstrip(" ,.;:") 
            return handle_skills(command, chat_history, available_skills)  

        else:
            # Regular routing logic (search or knowledge base)
            if should_search(question, chat_history, self.llm, self.embeddings, self.chat_history_embeddings):
                search_results = self.search.run(question)
                return search_results
            else:
                # ... (Your logic for responding directly using the knowledge base)
                return "I don't know." 

        # Update the context
        update_context(question, chat_history, self.embeddings, self.chat_history_embeddings)
