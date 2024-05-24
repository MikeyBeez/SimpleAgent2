import logging
import config
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from embedding_memory import EmbeddingMemory
from chat_manager import ChatManager

def initialize_user(chat_manager):
    """Gets the user's name and sets it in the ChatManager."""
    logging.info("Initializing user...")
    user_name = input("What is your name? ")
    print(f"Hello, {user_name}!")
    print("How can I help you?")
    chat_manager.entities.set_user_name(user_name)
    logging.info(f"User name set to {user_name}")

def initialize_chatbot():
    """
    Performs chatbot initialization tasks, including ChromaDB setup and user setup.
    """
    logging.basicConfig(
        filename='chat_log.txt',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s'
    )
    logging.info("Chatbot initialization started.")

    print(config.WELCOME_MESSAGE)

    # 1. Initialize Embedding Model 
    embedding_model = OllamaEmbeddings(model=config.embedding_model_name)

    # 2. Check if the ChromaDB collection exists
    persist_directory = "my_kb"  # Directory to store ChromaDB data
    collection_name = "my_chat_history"

    # Correctly check for the collection's existence:
    try:
        # Try to get the collection
        Chroma(persist_directory=persist_directory, embedding_function=embedding_model)._collection
        logging.info("ChromaDB collection already exists. Loading...")
    except:
        logging.info("Creating a new ChromaDB collection.")
        # Create a new collection if it doesn't exist
        Chroma.from_texts(
            texts=["Welcome to the chatbot!"],  # Initial text
            embedding=embedding_model,
            collection_name=collection_name,
            persist_directory=persist_directory
        )

    # 3. Initialize ChromaDB 
    vectorstore = Chroma(
        collection_name=collection_name, 
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )

    # 4. Initialize ChatManager
    chat_manager = ChatManager()

    # 5. Initialize EmbeddingMemory using the loaded or created vectorstore
    chat_manager.memory = EmbeddingMemory(vectorstore, chat_manager.llm, summary_frequency=3) 

    # 6. Set Other ChatManager Variables
    chat_manager.zip_code = config.zip_code
    chat_manager.latitude = config.latitude
    chat_manager.longitude = config.longitude
    chat_manager.noaa_weather_token = config.noaa_weather_token
    chat_manager.embedding_model_name = config.embedding_model_name

    # 7. Initialize the User
    initialize_user(chat_manager)

    print("Chatbot initialized. Ready to chat!")
    return chat_manager
