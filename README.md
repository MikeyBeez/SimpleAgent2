# SimpleAgent2: A Chatbot That Remembers and Learns

This chatbot is like a friend you can talk to and ask questions. It's built with some cool AI technology, and it can:

* **Remember your conversations:** So it doesn't forget what you've talked about.
* **Search the internet:** To find answers to your questions.
* **Learn from a huge knowledge base:** To give you even better responses. 

## Getting Started

This chatbot code is hosted on GitHub. Here's how to get a copy on your computer:

1. **Fork the Repository:**
   - Go to the project's GitHub page: https://github.com/MikeyBeez/SimpleAgent2/tree/main 
   - Click the "Fork" button in the top right corner. This will create your own copy of the project that you can work on.

2. **Clone Your Fork:**
   - Go to your forked repository on GitHub. 
   - Click the green "Code" button and copy the URL. 
   - Open your terminal and run the following command, replacing `<your_repository_url>` with the copied URL:
     ```bash
     git clone <your_repository_url>
     ```
   - This will download the code to your computer.

3. **Set Up Your Tools:**
   - You'll need to have [Conda](https://docs.conda.io/en/latest/) installed.
   - Open your terminal (or command prompt) and go into the project directory that you just cloned.
   - Create a special environment for this project:
      ```bash
      conda env create -f environment.yaml -n lg2
      conda activate lg2
      ```
   - Install the necessary Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - You'll also need [Ollama](https://ollama.com/) installed and running. It's an AI tool that powers the chatbot.
   - Download the language and embedding models for Ollama:
     ```bash
     ollama pull llama3-chatqa
     ollama pull all-minilm
     ```

4. **Prepare the Knowledge Base (RAG):**

   - **The `kb` Directory:** You already have a `kb` directory, so you're good to go!

   - **Download the Dataset:**
     - Download the DBpedia short abstracts dataset from this link: https://databus.dbpedia.org/vehnem/text/short-abstracts/2021.05.01/short-abstracts_lang=en.ttl.bzip2
     - Save the downloaded file (it will be named something like `short-abstracts_lang=en.ttl.bz2`) into your `kb` directory.

   - **Unzip the Dataset:**
     - Open your terminal, navigate to the `kb` directory (`cd kb`), and unzip the dataset using this command (replace `short-abstracts_lang=en.ttl.bz2` with the actual name of the file you downloaded):
       ```bash
       bunzip2 -k short-abstracts_lang=en.ttl.bz2
       ```
     - This will create a file named `short-abstracts_lang=en.ttl` in your `kb` directory. 

   - **Prepare the Conversion Tools:**
     - Copy the files `extract_json.py` and `generate_embeddings.py` from the main project directory into the `kb` directory. 

   - **Extract Text from the Dataset:**
     - While still in the `kb` directory in your terminal, run the following script:
       ```bash
       python extract_json.py 
       ```
     - This will create a new file named `extracted_kb.json`.
     - **Important:** This process might take a few hours.

   - **Generate Embeddings:**
     - Run the following script:
       ```bash
       python generate_embeddings.py
       ```
     - This will create a new file named `kb_with_embeddings.json`.
     - **Important:** This can take a very long time (possibly more than 20 hours). 

   - **ChromaDB:** The chatbot uses ChromaDB, a special database, to store and quickly search the knowledge base embeddings. ChromaDB will create its data files in the `my_kb` directory.

5. **Run the Chatbot:**
   - `python main.py`

## Chatting with the Bot

* The chatbot will ask for your name.
* You can type messages and ask it questions. 
* Try asking it things like:
    - "What's the capital of France?"
    - "How do you make a pizza?"
* To clear the chatbot's memory, type: `clear memory`
* To exit the chatbot, type: `quit`, `exit`, or `bye`.

## Making It Your Own

You can change how the chatbot talks and acts:

* **Change its personality:**  Edit the messages in the `prompts.py` file. 
* **Use a different search engine:**  If you don't like DuckDuckGo, you can replace it with another search engine. 
* **Try a different AI model:** Ollama has different models you can experiment with.

## If Something Goes Wrong

* **Check the error messages:**  If you get an error message, read it carefully. It might tell you what's wrong.
* **Make sure Ollama is running:**  The chatbot needs Ollama to work.
* **Be patient:**  Extracting information from the knowledge base can take a long time. 

## Want to Help?

* **Report problems:** If you find any bugs, let us know!
* **Share your ideas:**  Have ideas for new features? Tell us about them!

## System Architecture

This chatbot is designed as a modular system with several key components:

**1. Language Model (LLM):**

- **`chat_manager.py`:** This file initializes and interacts with the Ollama language model (currently `llama3-chatqa`).
- **`prompts.py`:**  Defines the prompt templates used to guide the LLM's responses.

**2. Search Engine:**

- **`chat_manager.py`:**  Handles web searches using DuckDuckGo.

**3. Conversation Memory:**

- **`memory.py`:** Manages and stores the conversation history so the chatbot remembers what you've talked about. 

**4. User Information:**

- **`entities.py`:** Keeps track of user information, like your name.

**5. Routing Logic:**

- **`routing.py`:**  Decides whether to use the knowledge base, perform a web search, or respond directly based on your questions.

**6. Knowledge Base (KB):**

- **`kb` directory:**  Contains the files related to the knowledge base.
- **`extract_json.py` and `generate_embeddings.py`:** These scripts process the knowledge base data. 
- **ChromaDB:** A database (stored in the `my_kb` directory) that allows the chatbot to search the knowledge base efficiently. 

**7. Main Chat Loop:**

- **`main.py`:**  The main part of the program that sets up everything and runs the chatbot.

**Customization and Extension:**

- **Prompts:** You can modify the prompts in `prompts.py` to customize the chatbot's responses. 
- **Search Engine:** You can use a different search engine by changing the code in `chat_manager.py`. 
- **Embedding Model:** You can try different Ollama embedding models by updating the model name in `chat_manager.py` and `routing.py`. 
- **Knowledge Base:** You can replace the knowledge base data in the `kb` directory and re-run the conversion scripts.
- **Adding New Tools:**
  1. **Initialize the Tool:**  Create a new tool object in `chat_manager.py`.
  2. **Pass the Tool to the Router:** Update the `Router` class in `routing.py` to accept and use your new tool. 
  3. **Add Routing Logic:**  Modify the `route()` function in `routing.py` to determine when to use the new tool.
  4. **Handle the New Route:**  Update the `run_conversation()` function in `chat_manager.py` to handle the new route and use the new tool. 

This modular architecture makes it easy to change parts of the chatbot and add new features! 

Let's chat! 😊
