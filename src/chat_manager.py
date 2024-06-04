import json
import requests
import config
import asyncio

from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from prompts import MAIN_PROMPT, SHOULD_SEARCH_PROMPT
from entities import Entities
from routing import Router
from langchain_community.embeddings import OllamaEmbeddings
from chat_loop_modules.context_manager import update_context
from get_time_skill import GetTimeSkill
from get_weather_skill import GetWeatherSkill
from embedding_memory import EmbeddingMemory
from langchain_community.vectorstores import Chroma
import logging
import config

# Set up logging
logging.basicConfig(filename='chat_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')

class ChatManager:
    """
    Manages the conversation flow, including memory, routing, and responses.
    """
    def __init__(self):
        # Initialize the Ollama language model
        logging.info("Initializing Ollama language model...")
        self.llm = Ollama(model=config.llm_model_name)
        logging.info("Ollama language model initialized.")

        # Initialize the DuckDuckGo search tool
        logging.info("ChatManager - Initializing DuckDuckGo search tool")
        self.search = DuckDuckGoSearchRun()
        logging.info("ChatManager - DuckDuckGo search tool initialized: %s", self.search)

        # Create an instance of the Entities class (for user info)
        logging.info("ChatManager - Initializing Entities class")
        self.entities = Entities()
        logging.info("ChatManager - Entities class initialized: %s", self.entities)

        # Initialize the embedding model using the config file
        logging.info("ChatManager - Initializing embedding model")
        self.embedding_model = OllamaEmbeddings(model=config.embedding_model_name)
        self.vectorstore = Chroma("my_chat_history", embedding_function=self.embedding_model)
        logging.info("ChatManager - Embedding model initialized: %s", self.embedding_model)
        logging.info("ChatManager - Vectorstore initialized: %s", self.vectorstore)

        # Initialize EmbeddingMemory
        logging.info("ChatManager - Initializing EmbeddingMemory")
        self.memory = EmbeddingMemory(self.vectorstore, self.llm, summary_frequency=3)
        logging.info("ChatManager - EmbeddingMemory initialized: %s", self.memory)

        # Initialize available skills
        logging.info("ChatManager - Initializing skills")
        self.get_time_skill = GetTimeSkill()
        self.get_weather_skill = GetWeatherSkill(latitude=config.latitude, longitude=config.longitude)
        self.available_skills = [self.get_time_skill, self.get_weather_skill]
        logging.info("ChatManager - Skills initialized: %s", self.available_skills)

        # Initialize the router with OllamaEmbeddings
        logging.info("ChatManager - Initializing router")
        self.embeddings = OllamaEmbeddings(model="all-minilm")
        self.router = Router(self.llm, self.embeddings)
        logging.info("ChatManager - Router initialized: %s", self.router)

        logging.info("ChatManager - ChatManager initialization complete")

    async def run_conversation(self):
        """
        Handles the main conversation loop.
        """
        logging.info("ChatManager - Starting conversation loop")

        # Get the user's name if it's not already set
        if not self.entities.get_user_name():
            user_name = input("What is your name? ")
            print(f"Hello, {user_name}!")
            print("How can I help you?")
            self.entities.set_user_name(user_name)
            logging.info("ChatManager - User name set: %s", user_name)

        # Main conversation loop
        while True:
            # Get user input
            user_name = self.entities.get_user_name()
            if user_name:
                question = input(f"{user_name}: ")
            else:
                question = input("You: ")

            # Log the user input (question)
            logging.info("ChatManager - User input: %s", question)

            # Check for special commands
            if question.lower() == "clear memory":
                logging.info("ChatManager - Clearing memory")
                self.memory.vectorstore.delete_collection()  # Clear Chroma collection
                print("Conversation memory cleared.")
                logging.info("ChatManager - Memory cleared")

            if question.lower() in ["quit", "exit", "bye"]:
                logging.info("ChatManager - Exiting conversation loop")
                break

            # Load relevant context from memory using embeddings
            logging.info("ChatManager - Loading context from memory")
            context = self.memory.load_memory_variables(question)
            chat_history = context.get("history", "")
            logging.info("ChatManager - Loaded chat history: %s", chat_history)

            # Determine if a search is needed, a skill should be used,
            # or the knowledge base should be queried
            logging.info("ChatManager - Routing question")
            response = self.router.route(question, chat_history, self.available_skills)
            logging.info("ChatManager - Routing complete, response: %s", response)

            # Check if the response is None (meaning no route was found)
            if response is None:
                logging.warning("ChatManager - No route found, using default response")
                response = "I'm not sure how to answer that."
                logging.info("ChatManager - Default response: %s", response)

            # Format the main prompt
            logging.info("ChatManager - Formatting prompt")
            formatted_prompt = MAIN_PROMPT.format(
                chat_history=chat_history,
                question=question,
                search_results=response,
                user_name=user_name
            )
            logging.debug("ChatManager - Formatted prompt: %s", formatted_prompt)

            # Generate the agent's response using streaming output
            print("Agent: ", end="")
            response = ""
            logging.info("ChatManager - Generating response")
            for chunk in self.llm.stream(formatted_prompt, temperature=0.7):
                response += chunk
                print(chunk, end="", flush=True)
            logging.info("ChatManager - Response generation complete")
            print()

            # Log the complete response
            logging.info("ChatManager - Generated response: %s", response)

            # Update the chat history
            chat_history += f"{user_name}: {question}\nAgent: {response}\n"

            # Update the context vectorstore
            logging.info("ChatManager - Updating context")
            update_context(question, chat_history)
            logging.info("ChatManager - Context updated")

            # Save the current interaction to memory (using embeddings)
            logging.info("ChatManager - Saving context to memory")
            self.memory.save_context({"input": question}, {"output": response})
            logging.info("ChatManager - Context saved")
