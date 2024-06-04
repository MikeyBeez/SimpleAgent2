from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import config

# Initialize the embedding model
embedding_model = OllamaEmbeddings(model=config.embedding_model_name)

# Initialize the Chroma vectorstore with the "my_chat_history" collection
vectorstore = Chroma(persist_directory="my_kb", embedding_function=embedding_model, collection_name="my_chat_history")

# Get the total number of items stored in the "my_chat_history" collection
total_items = vectorstore._collection.count()
print(f"Total items in the 'my_chat_history' collection: {total_items}")

# Retrieve all items from the "my_chat_history" collection
items = vectorstore._collection.get()

for i, item in enumerate(items["documents"], start=1):
    print(f"\nItem {i}:")
    print("Text:")
    print(item)
    
    # Check if the metadata exists
    if items["metadatas"]:
        metadata = items["metadatas"][i - 1]
        print("\nMetadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print("\nNo metadata available.")

# Skip printing embeddings and English tokens
