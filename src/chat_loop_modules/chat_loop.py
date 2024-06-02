import asyncio
import logging
from prompts import MAIN_PROMPT
from .context_manager import update_context, get_chat_history
from logging_config import configure_logging

configure_logging()

async def run_conversation(chat_manager):
    """Handles the main conversation loop."""
    logging.info("Starting conversation loop...")

    while True:
        # Get user input
        user_name = chat_manager.entities.get_user_name()
        if user_name:
            question = input(f"{user_name}: ")
        else:
            question = input("You: ")

        logging.info(f"User Input: {question}")

        # Handle special commands like "clear memory" and exit
        if question.lower() == "/clear memory":
            logging.info("Clearing memory...")
            chat_manager.memory.vectorstore.delete_collection()
            print("Conversation memory cleared.")
            logging.info("Memory cleared.")
            continue

        if question.lower() in ["/quit", "/exit", "/bye"]:
            logging.info("Exiting conversation loop...")
            break

        if question.lower() == "/help":
            logging.info("Help request...")
            help_text = """
Available commands:
- /clear memory: Clears the conversation memory
- /help: Displays this help information
- /quit, /exit, /bye: Exits the chatbot

Available skills:
"""
            for skill in chat_manager.available_skills:
                help_text += f"- {skill.__class__.__name__}: {skill.description}\n"
            print(help_text)
            continue

        # Check for skill invocation
        if "assistant" in question.lower():
            logging.info("Assistant keyword detected, checking for skills.")
            command = question.lower().split("assistant", 1)[1].strip()
            for skill in chat_manager.available_skills:
                if skill.trigger(command):
                    logging.info(f"Skill triggered: {skill.__class__.__name__}")
                    response = skill.process(command)
                    print(f"Agent: {response}")
                    update_context(question, response)
                    break
            else:
                logging.info("No skill matched the command, passing to router.")
                context = chat_manager.memory.load_memory_variables({"question": question})
                chat_history = context.get("history", "")
                response = chat_manager.router.route(question, chat_history, chat_manager.available_skills)
                print(f"Agent: {response}")
                update_context(question, response)
            continue  # Go to the next user input

        # Load relevant context from memory using embeddings
        logging.info("Loading context from memory...")
        context = chat_manager.memory.load_memory_variables({"question": question})
        chat_history = context.get("history", "")
        logging.info(f"Loaded chat history: {chat_history}")

        # Route the question (for regular questions, not skills)
        logging.info("Routing question...")
        response = chat_manager.router.route(question, chat_history, chat_manager.available_skills)
        logging.info("Routing complete.")

        # Check if the response is None (no route found)
        if response is None:
            logging.info("No route found, defaulting response...")
            response = "I'm not sure how to answer that."
            logging.info(f"Default response: {response}")

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
        update_context(question, response)
        logging.info("Context updated.")

        # Save the current interaction to memory (using embeddings)
        logging.info("Saving context to memory...")
        chat_manager.memory.save_context({"input": question}, {"output": response})
        logging.info("Context saved.")
