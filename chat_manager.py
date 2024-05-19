import asyncio
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from prompts import MAIN_PROMPT, SHOULD_SEARCH_PROMPT
from memory import load_memory, save_memory, clear_memory, update_memory_async
from entities import Entities
from routing import Router  # Don't import should_search, it's now accessed through Router
from langchain_community.embeddings import OllamaEmbeddings
from context_manager import update_context # Import update_context
import logging

# Set up logging
logging.basicConfig(filename='chat_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ChatManager:
    def __init__(self):
        # Initialize the Ollama language model
        self.llm = Ollama(model="llama3-chatqa")  # Initialize self.llm here

        # Initialize the DuckDuckGo search tool
        self.search = DuckDuckGoSearchRun()

        # Create an instance of the Entities class
        self.entities = Entities()

        # Initialize the router with OllamaEmbeddings
        self.embeddings = OllamaEmbeddings(model="all-minilm")
        self.router = Router(self.llm, self.embeddings)

        # Initialize available skills (empty for now)
        self.available_skills = []

    async def run_conversation(self):
        # Get the user's name if it's not already set
        if not self.entities.get_user_name():
            user_name = input("What is your name? ")
            print(f"Hello, {user_name}!")
            print("How can I help you?")
            self.entities.set_user_name(user_name)

        # Load the conversation memory from file or create a new one
        memory = load_memory(self.llm)  # Initialize memory here

        # Main conversation loop
        while True:
            # Get user input
            user_name = self.entities.get_user_name()
            if user_name:
                question = input(f"{user_name}: ")
            else:
                question = input("You: ")

            # Log the user input (question)
            logging.info(f"User Input: {question}")

            # Check for special commands
            if question.lower() == "clear memory":
                await clear_memory()
                memory = load_memory(self.llm)  # Re-assign memory after clearing

            if question.lower() in ["quit", "exit", "bye"]:
                break

            # Load relevant context from memory
            context = memory.load_memory_variables({"question": question})
            chat_history = context.get("history", "")

            # Determine if a search is needed, a skill should be used, or the knowledge base should be queried
            response = self.router.route(question, chat_history, self.available_skills)

            # Check if the response is None (meaning no route was found)
            if response is None:
                response = "I'm not sure how to answer that."

            # Format the main prompt
            formatted_prompt = MAIN_PROMPT.format(
                chat_history=chat_history,
                question=question,
                search_results=response, 
                user_name=user_name
            )

            # Generate the agent's response using streaming output
            print("Agent: ", end="")
            response = ""
            for chunk in self.llm.stream(formatted_prompt, temperature=0.7):
                response += chunk
                print(chunk, end="", flush=True)

            print()

            # Log the response
            logging.info(f"Response: {response}")

            # Update the chat history
            if user_name:
                chat_history += f"{user_name}: {question}\nAgent: {response}\n"
            else:
                chat_history += f"You: {question}\nAgent: {response}\n"

            # Update the context vectorstore 
            update_context(question, chat_history, self.embeddings, self.router.chat_history_embeddings) # Call the imported function 

            # Save the current interaction to memory
            asyncio.create_task(update_memory_async(memory, question, response, self.entities))

        # Save the conversation memory to file
        await save_memory(memory)
