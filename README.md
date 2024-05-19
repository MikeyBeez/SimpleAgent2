# Simple Agent 2: A Chatbot with Memory and Search

This is a simple chatbot built using LangChain, Ollama, and DuckDuckGo. It features:

- **Conversation History:** The chatbot remembers past interactions and uses this context to provide more relevant responses.
- **Search Integration:** The chatbot can use DuckDuckGo to retrieve information from the internet when needed.
- **Semantic Search:** The chatbot uses Ollama's embedding model to identify semantically similar questions in the conversation history and avoid redundant searches.

## Getting Started

fork and clone the repository

conda env create -f environment.yaml -n lg3
conda activate lg3
pip install -r requirements.txt

ollama pull llama3-chatqa 
ollama pull mxbai-embed-large

Set up RAG with a knowledgebase.  You can start with the one below:
Download https://databus.dbpedia.org/vehnem/text/short-abstracts/2021.05.01/short-abstracts_lang=en.ttl.bzip2

Run the Chatbot:
python main.py

Usage
The chatbot will prompt you for your name.
You can interact with the chatbot by typing messages.
Use the following commands:
clear memory: Clears the conversation history stored in the conversation_memory.json file.
quit, exit, bye: Exits the chatbot.
Customization
Prompts: Modify the prompt templates in prompts.py to customize the chatbot's personality and behavior.
Search Engine: Replace DuckDuckGo with a different search engine if desired.
Embedding Model: Experiment with different embedding models supported by Ollama.
Note
You need to have Ollama running locally or on a remote server before running this code.
This chatbot is a simple example and can be further enhanced with additional features like more sophisticated memory management, context tracking, and persona development.
Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or suggestions.

