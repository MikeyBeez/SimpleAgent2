import asyncio
import logging
from prompts import MAIN_PROMPT
from .context_manager import update_context, get_chat_history
from routing import DO_NOTHING_TOKEN  

# Configure logging
logging.basicConfig(
    filename='chat_log.txt',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s' 
)

async def run_conversation(chat_manager):
    """Handles the main conversation loop."""
    logging.info("Starting conversation loop...")

    # Main conversation loop
    while True:
        # Get user input
        user_name = chat_manager.entities.get_user_name()
        if user_name:
            question = input(f"{user_name}: ")
        else:
            question = input("You: ")

        logging.info(f"User Input: {question}")

        # Check for special commands
        if question.lower() == "clear memory":
            logging.info("Clearing memory...")
            chat_manager.memory.vectorstore.delete_collection()
            print("Conversation memory cleared.")
            logging.info("Memory cleared.")

        if question.lower() in ["quit", "exit", "bye"]:
            logging.info("Exiting conversation loop...")
            break

        # Load relevant context from memory using embeddings
        logging.info("Loading context from memory...")
        context = chat_manager.memory.load_memory_variables({"question": question})
        chat_history = context.get("history", "")
        logging.info(f"Loaded chat history: {chat_history}")

        # Route the question:
        logging.info("Routing question...")
        response = chat_manager.router.route(question, chat_history, chat_manager.available_skills)
        logging.info("Routing complete.")

        # Check if the response is None (no route found)
        if response is None:
            logging.info("No route found, defaulting response...")
            response = "I'm not sure how to answer that."
            logging.info(f"Default response: {response}")

        # Handle DO_NOTHING_TOKEN (skill already processed)
        if response == DO_NOTHING_TOKEN:
            continue  # Skip LLM processing and get the next input

        # Format the main prompt 
        logging.info("Formatting prompt...")
        formatted_prompt = MAIN_PROMPT.format(
            chat_history=chat_history,
            question=question,
            search_results=response,
            user_name=user_name
        )
        logging.info(f"Formatted prompt: {formatted_prompt}")

        # Generate the agent's response using streaming output
        print("Agent: ", end="")
        response = ""
        logging.info("Generating response...")
        for chunk in chat_manager.llm.stream(formatted_prompt, temperature=0.7):
            response += chunk
            print(chunk, end="", flush=True)
            logging.info(f"Response chunk: {chunk}")
        logging.info("Response generation complete.")
        print()

        # Log the response
        logging.info(f"Response: {response}")

        # Update the context vectorstore 
        logging.info("Updating context...")
        update_context(question, response)  # Corrected call
        logging.info("Context updated.")

        # Save the current interaction to memory (using embeddings)
        logging.info("Saving context to memory...")
        chat_manager.memory.save_context({"input": question}, {"output": response})
        logging.info("Context saved.") 
