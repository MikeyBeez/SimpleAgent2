from chat_loop_modules.search_logic import should_search
from chat_loop_modules.context_manager import update_context
from chat_loop_modules.skill_handler import handle_skills
from langchain_community.tools import DuckDuckGoSearchRun
import logging

# Configure logging
logging.basicConfig(
    filename='chat_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
)

DO_NOTHING_TOKEN = "##DO_NOTHING##"

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
            str: The response to the user, or DO_NOTHING_TOKEN if a skill was handled.
        """
        logging.info(f"User question: {question}")  

        # Check for "assistant" wakeword
        if question.lower().startswith("assistant"):
            logging.info("Assistant wakeword detected.")
            command = question.lower().split("assistant", 1)[1].strip().lstrip(" ,.;:")
            logging.info(f"Extracted command: {command}") 

            # Call handle_skills() only inside the "assistant" wakeword block
            skill_response = handle_skills(command, chat_history, available_skills) 
            if skill_response:
                logging.info("Skill triggered successfully.")
                return DO_NOTHING_TOKEN  
            else:
                logging.info("No skill matched the command.")

        # Regular routing logic (for questions without the "assistant" wakeword) 
        if should_search(question, chat_history, self.llm, self.embeddings, self.chat_history_embeddings):
            logging.info("Decision: Performing a search.") 
            search_results = self.search.run(question)
            return search_results
        else:
            logging.info("Decision: Using knowledge base (not implemented).") 
            return "I don't know."

        update_context(question, response)  
