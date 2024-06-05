import asyncio
import logging
from prompts import MAIN_PROMPT
from .context_manager import update_context, get_chat_history
from logging_config import configure_logging
import config

configure_logging()

async def run_conversation(chat_manager):
    """Handles the main conversation loop."""
    if config.DEBUG:
        print("DEBUG: Starting conversation loop...")

    while True:
        # Get user input
        user_name = chat_manager.entities.get_user_name()
        if user_name:
            question = input(f"{user_name}: ")
        else:
            question = input("You: ")

        if config.DEBUG:
            print(f"DEBUG: User Input: {question}")

        # Handle special commands like "clear memory" and exit
        if question.lower() == "/clear memory":
            if config.DEBUG:
                print("DEBUG: Clearing memory...")
            chat_manager.memory.vectorstore.delete_collection()
            print("Conversation memory cleared.")
            if config.DEBUG:
                print("DEBUG: Memory cleared.")
            continue

        if question.lower() in ["/quit", "/exit", "/bye"]:
            if config.DEBUG:
                print("DEBUG: Exiting conversation loop...")
            break

        # Load relevant context from memory using embeddings
        if config.DEBUG:
            print("DEBUG: Loading context from memory...")
        context = chat_manager.memory.load_memory_variables(question)
        embedded_memory_results = context.get("history", "")
        if config.DEBUG:
            print(f"DEBUG: Loaded embedded memory results: {embedded_memory_results}")
            print("DEBUG: End of loading context from memory.")

        # Filter context based on relevance and recency
        relevant_context = chat_manager.memory.filter_context(embedded_memory_results, question)
        if config.DEBUG:
            print(f"DEBUG: Filtered relevant context: {relevant_context}")

        # Route the question
        if config.DEBUG:
            print("DEBUG: Routing question...")
        search_results = chat_manager.router.route(question, relevant_context, chat_manager.available_skills)
        if config.DEBUG:
            print("DEBUG: Routing complete.")

        # Format the main prompt
        if config.DEBUG:
            print("DEBUG: Formatting prompt...")
        formatted_prompt = MAIN_PROMPT.format(
            chat_history=relevant_context,  # Use the filtered relevant context as chat history
            question=question,
            search_results=search_results,
            user_name=user_name
        )
        if config.DEBUG:
            print(f"DEBUG: Formatted prompt: {formatted_prompt}")

        # Generate the agent's response using streaming output
        print("Agent: ", end="")
        response = ""
        if config.DEBUG:
            print("DEBUG: Generating response...")
        for chunk in chat_manager.llm.stream(formatted_prompt, temperature=0.7):
            response += chunk
            print(chunk, end="", flush=True)
            if config.DEBUG:
                print(f"DEBUG: Response chunk: {chunk}")
        if config.DEBUG:
            print("DEBUG: Response generation complete.")
        print()

        if config.DEBUG:
            print(f"DEBUG: Response: {response}")

        # Update context and save to memory
        if config.DEBUG:
            print("DEBUG: Updating context and saving to memory...")
        update_context({"input": question, "output": response})
        chat_manager.memory.save_context({"input": question}, {"output": response})
        if config.DEBUG:
            print("DEBUG: Context updated and saved.")
