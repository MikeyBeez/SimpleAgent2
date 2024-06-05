# SimpleAgent2: A Chatbot That Remembers, Learns, and Uses Skills
# This is a work in Progress not a polished piece of code.  Nevertheless, there are a lot of powerfule ideas here.  
I've added Debug statements that are eneabled in config.py by setting DEBUG = True.  

SimpleAgent2 is an advanced chatbot framework that combines the power of natural language processing, memory management, and modular skills to create intelligent and engaging conversational experiences. With SimpleAgent2, developers can build chatbots that understand user intents, provide relevant information, and execute specific tasks.

## Key Features

* **Contextual Memory:** SimpleAgent2 uses embeddings to store and retrieve conversation history, allowing the chatbot to maintain context and provide more accurate responses.
* **Modular Skills:** The framework supports the creation of custom skills, enabling developers to extend the chatbot's capabilities and handle specific tasks or queries.
* **Flexible Architecture:** SimpleAgent2 follows a modular design, making it easy to customize and integrate with various language models, search engines, and external APIs.
* **Extensible Knowledge Base:** The chatbot can leverage a knowledge base to provide answers to user queries, and developers can easily integrate their own knowledge sources.
* **Search Capabilities:** SimpleAgent2 includes a search component that allows the chatbot to retrieve relevant information from external sources when needed.

## Getting Started

To get started with SimpleAgent2, follow these steps:

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

5. **Configuration:**
   - Create a copy of the `config.sample.py` file and rename it to `config.py`.
   - Open `config.py` in a text editor and replace the placeholders with your actual API keys and desired settings.
   - Save the `config.py` file.
   - **Important:** Make sure to keep your `config.py` file secure and do not share it publicly, as it contains sensitive information like API keys.

6. **Run the Chatbot:**
   - `python main.py`

## Chatting with the Bot

* The chatbot will ask for your name.
* You can type messages and ask it questions.
* To use a custom skill, start your input with the wakeword "**assistant**" followed by a phrase or keyword that triggers the skill.
* Try asking it things like:
  - "What's the capital of France?"
  - "How do you make a pizza?"
* To clear the chatbot's memory, type: `/clear memory`
* To get help and see available commands, type: `/help`
* To exit the chatbot, type: `/quit`, `/exit`, or `/bye`.

## Making It Your Own

You can change how the chatbot talks and acts:

* **Change its personality:** Edit the messages in the `prompts.py` file.
* **Use a different search engine:** If you don't like DuckDuckGo, you can replace it with another search engine.
* **Try a different AI model:** Ollama has different models you can experiment with.
* **Add new skills:** Follow the instructions in the **Adding New Skills** section.

## Adding New Skills

1. **Create a Skill Class:**
   - Create a new Python file in the project's `skills` directory (for example, `my_new_skill.py`).
   - Define a class that inherits from the `Skill` class.
   - Implement the `process(self, input_text)` method to perform the skill's action.
   - Implement the `trigger(self, input_text)` method to determine when the skill should be activated. The `trigger` method should check for phrases or keywords *after* the "assistant" wakeword.

2. **Register Your Skill:**
   - In the `chat_manager.py` file, import your new skill class.
   - Create an instance of your skill class in the `ChatManager`'s `__init__` method.
   - Add the instance to the `available_skills` list.

**To use a custom skill, start your input with the wakeword "assistant" followed by a phrase or keyword that triggers the skill.**

For example, if you have a skill called `TellJokeSkill`, you could trigger it with: "Assistant, tell a joke."

## Debugging and Troubleshooting

SimpleAgent2 provides several tools and techniques to assist developers in identifying and resolving issues:

* **Logging:** The framework uses the `logging` module to capture important events, errors, and information during the chatbot's execution. Developers can configure the logging settings in the `config.py` file and analyze the generated logs to diagnose issues.
* **Error Handling:** SimpleAgent2 includes error handling mechanisms to gracefully handle exceptions and provide meaningful error messages. Developers can add custom error handling logic in the relevant files to handle specific exceptions and provide informative feedback to users.
* **Testing:** The framework includes a suite of unit tests to ensure the correctness of individual components. Developers can run these tests using the `pytest` framework and add new tests to validate the functionality of custom skills, memory management, and other modifications.
* **Interactive Debugging:** Developers can use interactive debugging tools, such as Python's built-in `pdb` module or IDEs with debugging capabilities, to step through the code, inspect variables, and identify the root cause of issues.
* **Monitoring and Analytics:** Implementing monitoring and analytics tools can help developers track the chatbot's performance, identify usage patterns, and detect anomalies. Popular tools like Prometheus, Grafana, or custom logging solutions can be integrated with SimpleAgent2 to gain insights into the chatbot's behavior and user interactions.

## Contributing

We welcome contributions to SimpleAgent2! If you'd like to contribute, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure that the code passes all tests.
4. Submit a pull request describing your changes and their benefits.

Please make sure to adhere to the project's coding style and guidelines.

## License

SimpleAgent2 is released under the [MIT License](LICENSE).

## Acknowledgements

We would like to express our gratitude to the open-source community for their valuable contributions and the developers of the libraries and tools used in SimpleAgent2.

## Contact

If you have any questions, suggestions, or feedback, please feel free to contact us 
opening an issue.

Happy chatbot building with SimpleAgent2!
