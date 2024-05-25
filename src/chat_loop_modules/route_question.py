import logging

def route_question(user_input, chat_manager):
    """Routes the question to the appropriate handler (skills, search, or knowledge base)."""
    logging.info("Routing question...")
    # Load relevant context from memory using embeddings
    logging.info("Loading context from memory...")
    context = chat_manager.memory.load_memory_variables({"question": user_input})
    chat_history = context.get("history", "")
    logging.info(f"Loaded chat history: {chat_history}")
    response = chat_manager.router.route(
        user_input, chat_history, chat_manager.available_skills
    )
    logging.info("Routing complete.")
    return response
