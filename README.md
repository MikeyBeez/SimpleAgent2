# SimpleAgent2: A Chatbot That Remembers, Learns, and Uses Skills

This chatbot is like a friend you can talk to and ask questions. It's built with some cool AI technology, and it can:

* **Remember your conversations:** So it doesn't forget what you've talked about.
* **Search the internet:** To find answers to your questions.
* **Learn from a huge knowledge base:** To give you even better responses. 
* **Use custom skills:** To perform specific tasks or provide specialized information.

## Getting Started

This chatbot code is hosted on GitHub. Here's how to get a copy on your computer:

1. **Fork the Repository:**
   - Go to the project's GitHub page: https://github.com/MikeyBeez/SimpleAgent2
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
     - Download the DBpedia short abstracts dataset from this link: https://databus.dbpedia.org/vehnem/text/short-abstracts/2021.05.01/short-abstracts_lang=en.ttl.bz2
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
* To use a custom skill, start your input with the wakeword "**assistant**" followed by a phrase or keyword that triggers the skill.  
* For example:

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
* **Add new skills:** Follow the instructions in the **Adding New Skills** section.

## Adding New Skills

1. **Create a Skill Class:**
* Create a new Python file in the project's root directory (for example, `my_new_skill.py`).
* Define a class that inherits from the `Skill` class.
* Implement the `process(self, input_text)` method to perform the skill's action.
* Implement the `trigger(self, input_text)` method to determine when the skill should be activated.  The `trigger` method should check for phrases or keywords *after* the "assistant" wakeword.

2. **Register Your Skill:**
* In the `chat_manager.py` file, import your new skill class.
* Create an instance of your skill class in the `ChatManager`'s `__init__` method.
* Add the instance to the `available_skills` list. 

**To use a custom skill, start your input with the wakeword "assistant" followed by a phrase or keyword that triggers the skill.**

For example, if you have a skill called `TellJokeSkill`, you could trigger it with:


## If Something Goes Wrong

* **Check the error messages:**  If you get an error message, read it carefully. It might tell you what's wrong.
* **Make sure Ollama is running:**  The chatbot needs Ollama to work.
* **Be patient:**  Extracting information from the knowledge base can take a long time. 

## Want to Help?

* **Report problems:** If you find any bugs, let us know!
* **Share your ideas:**  Have ideas for new features? Tell us about them!

## System Architecture

The chatbot's code is organized into several modules:

**Core Components:**

* **`chat_manager.py`:** Initializes the LLM, search engine, entities, embeddings, and the router. Runs the main conversation loop. 
* **`prompts.py`:**  Defines prompt templates for the LLM.
* **`memory.py`:**  Handles conversation history storage and retrieval.
* **`entities.py`:**  Keeps track of user information.
* **`routing.py`:**  Contains the `Router` class, which decides how to handle user input (search, skills, or knowledge base).

**Refactored Modules:**

* **`search_logic.py`:**  Determines if a web search is needed based on the user's question and conversation history.
* **`context_manager.py`:**  Updates the context vectorstore with new questions for semantic similarity checks.
* **`skill_handler.py`:**  Checks if any registered skills should be triggered and executes them. 

**Knowledge Base:**

- **`kb` directory:**  Contains the knowledge base data and processing scripts.
- **`extract_json.py` and `generate_embeddings.py`:**  Scripts to process and embed the knowledge base. 
- **ChromaDB:** A vector database for efficient knowledge base search. 

**Skills:**

* **`get_time_skill.py`:**  A skill to get the current time.
* **(Add your new skill files here)**

**Main Program:**

* **`main.py`:**  The main program that sets up and runs the chatbot.

**Customization and Extension:**

The modular design makes it easy to customize the chatbot:

* **Prompts:** Modify the prompts in `prompts.py` to change the chatbot's personality.
* **Search Engine:** Replace DuckDuckGo with a different search engine.
* **Embedding Model:** Use different embedding models for semantic similarity.
* **Knowledge Base:** Update or replace the knowledge base data.
* **Skills:** Add new skills to extend the chatbot's capabilities.

Let's chat! 😊 
