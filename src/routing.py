from chat_loop_modules.search_logic import should_search
from chat_loop_modules.context_manager import update_context
from chat_loop_modules.skill_handler import handle_skills
from langchain_community.tools import DuckDuckGoSearchRun
import logging
import config
import datetime
from get_weather_skill import GetWeatherSkill

DO_NOTHING_TOKEN = "##DO_NOTHING##"

# Configure logging
logging.basicConfig(
    filename='chat_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
)

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
            str: The search results or an empty string if no search is needed.
        """
        if config.DEBUG:
            print(f"DEBUG: User question: {question}")

        # Check for "assistant" wakeword
        if question.lower().startswith("assistant"):
            if config.DEBUG:
                print("DEBUG: Assistant wakeword detected.")
            command = question.lower().split("assistant", 1)[1].strip().lstrip(" ,.;:")
            if config.DEBUG:
                print(f"DEBUG: Extracted command: {command}")


            if command == "time":
                    current_time = datetime.datetime.now().strftime("%I:%M %p")
                    print(f"The current time is {current_time}.")
                    return DO_NOTHING_TOKEN

            if command == "weather":
                for skill in available_skills:
                    if isinstance(skill, GetWeatherSkill):
                        weather_info = skill.process(command)
                        print(weather_info)
                        return DO_NOTHING_TOKEN


            # Call handle_skills() only inside the "assistant" wakeword block
            skill_response = handle_skills(command, available_skills)
            if skill_response:
                if config.DEBUG:
                    print("DEBUG: Skill triggered successfully.")
                return skill_response
            else:
                if config.DEBUG:
                    print("DEBUG: No skill matched the command.")

        # Regular routing logic (for questions without the "assistant" wakeword)
        if should_search(question, chat_history, self.llm, self.embeddings, self.chat_history_embeddings):
            if config.DEBUG:
                print("DEBUG: Decision: Performing a search.")
            search_quality_reflection = "The search results provide some relevant information to answer the question, but may not be comprehensive enough to fully address all aspects of the query."
            search_quality_score = 3  # Assuming a scale of 1-5
            result = self.search.run(question)
            search_results = f"Search Quality Reflection: {search_quality_reflection}\nSearch Quality Score: {search_quality_score}\n\nSearch Results:\n{result}"
        else:
            if config.DEBUG:
                print("DEBUG: Decision: Using knowledge base (not implemented).")
            search_results = "I don't have enough information in my knowledge base to answer this question confidently."

        if config.DEBUG:
            print(f"DEBUG: Generated search results: {search_results}")

        update_context({"input": question, "output": search_results})  # Pass a dictionary with "input" and "output" keys
        return search_results
