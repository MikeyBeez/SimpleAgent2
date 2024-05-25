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
    print(f"Updating context with question: {question}")

    # Append question and response to history 
    chat_history.append(f"User: {question}") 
    chat_history.append(f"Agent: {response}")

    # Embed question and response
    question_embedding = embedding_model.embed_query(question)
    response_embedding = embedding_model.embed_query(response)

    # Convert chat_history to a JSON string
    chat_history_json = json.dumps(chat_history)

    # Add to vectorstore
    vectorstore.add_texts(
        texts=[question, response],
        embeddings=[question_embedding, response_embedding],
        metadatas=[{"history": chat_history_json}]
    )

def get_chat_history():
    """Returns the current chat history."""
    return chat_history 
