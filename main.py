import asyncio
from langchain_community.llms import Ollama  # Import the Ollama language model class
from langchain_community.tools import DuckDuckGoSearchRun  # Import the DuckDuckGo search tool class
from prompts import MAIN_PROMPT, SHOULD_SEARCH_PROMPT  # Import prompt templates from prompts.py
from memory import load_memory, save_memory, clear_memory # Import memory management functions (including clear_memory)

# Initialize the Ollama language model
llm = Ollama(model="llama3-chatqa")  # Create an instance of the Ollama model, using the "llama3-chatqa" model

# Initialize the DuckDuckGo search tool
search = DuckDuckGoSearchRun() # Create an instance of the DuckDuckGo search tool

# Load the conversation memory from file or create a new one
memory = load_memory(llm)  # Load conversation history, memory is a ConversationSummaryMemory object

# Main conversation loop
while True:
    # Get user input
    question = input("You: ") # question is a string containing the user's input

    # Check for special commands
    if question.lower() == "clear memory":
        clear_memory()  # Clear the conversation memory file
        memory = load_memory(llm)  # Reload memory after clearing 
        continue  # Skip to the next iteration of the loop

    if question.lower() in ["quit", "exit", "bye"]:
        break  # Exit the conversation loop

    # Load relevant context from memory based on the current question
    context = memory.load_memory_variables({"question": question}) # context is a dictionary containing memory variables
    chat_history = context.get("history", "") # chat_history is a string containing the summarized conversation history

    # Determine if a search is needed using the SHOULD_SEARCH_PROMPT
    should_search = llm.invoke(
        SHOULD_SEARCH_PROMPT.format(question=question, chat_history=chat_history)
    ).strip() # should_search is a string, either "yes" or "no", indicating if a search is needed

    # Initialize search results to an empty string
    search_results = "" # search_results will store the search results if a search is performed

    # Perform a search if the LLM determines it's necessary
    if should_search.lower() == "yes":
        print("Agent: Searching...")
        search_results = search.run(question) # search_results is a string containing the results from DuckDuckGo

    # Format the main prompt with the chat history, question, and search results
    formatted_prompt = MAIN_PROMPT.format(
        chat_history=chat_history, # Pass the chat history
        question=question, # Pass the user's question
        search_results=search_results, # Pass the search results (if any)
    )  # formatted_prompt is a string containing the complete prompt for the LLM

    # Generate the agent's response using streaming output
    print("Agent: ", end="") 
    response = "" # Initialize an empty string to store the response
    for chunk in llm.stream(formatted_prompt, temperature=0.7): # Get response chunks from the LLM (streaming)
        response += chunk  # Append each chunk to the response string
        print(chunk, end="", flush=True)  # Print the chunk immediately without a newline

    print()  # Print a newline after the response is complete

    # Update the chat history with the current turn's conversation
    chat_history += f"You: {question}\nAgent: {response}\n" 

    # Save the current interaction to memory asynchronously
    asyncio.create_task(save_memory(memory))  

# Save the conversation memory to file after the loop ends
asyncio.run(await save_memory(memory)) 
