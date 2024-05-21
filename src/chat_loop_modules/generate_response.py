import logging
from prompts import MAIN_PROMPT

def generate_response(user_input, response, chat_manager):
    """Formats the prompt and generates a response from the LLM."""
    logging.info("Formatting prompt...")
    user_name = chat_manager.entities.get_user_name()
    formatted_prompt = MAIN_PROMPT.format(
        chat_history=chat_manager.memory.buffer,
        question=user_input,
        search_results=response,
        user_name=user_name
    )
    logging.info(f"Formatted prompt: {formatted_prompt}")

    logging.info("Generating response...")
    llm_response = ""
    for chunk in chat_manager.llm.stream(formatted_prompt, temperature=0.7):
        llm_response += chunk
        print(chunk, end="", flush=True)
        logging.info(f"Response chunk: {chunk}")
    logging.info("Response generation complete.")
    print()

    logging.info(f"Response: {llm_response}")
    return llm_response 
