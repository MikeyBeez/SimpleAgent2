import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import config
import json 

embedding_model = OllamaEmbeddings(model=config.embedding_model_name)
vectorstore = Chroma("my_context", embedding_function=embedding_model)

chat_history = [] # Store the chat history directly in context_manager.py

def update_context(question, response):
    """
    Updates the context vectorstore and chat history.
    """
    print(f"Updating context with question-answer pair: {question} - {response}")

    # Append question-answer pair to history
    chat_history.append(f"User: {question}\nAgent: {response}")

    # Embed the question-answer pair
    qa_pair_text = f"User: {question}\nAgent: {response}"
    qa_pair_embedding = embedding_model.embed_query(qa_pair_text)

    # Convert chat_history to a JSON string
    chat_history_json = json.dumps(chat_history)

    # Add to vectorstore
    vectorstore.add_texts(
        texts=[qa_pair_text],
        embeddings=[qa_pair_embedding],
        metadatas=[{"history": chat_history_json}]
    )

def get_chat_history():
    """Returns the current chat history."""
    return chat_history 
