from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

embedding_model = OllamaEmbeddings(model="all-minilm")
vectorstore = Chroma("my_context", embedding_function=embedding_model)

# Get the total number of items stored in Chroma
total_items = vectorstore._collection.count()

# Calculate the offset to retrieve the last 20 items
offset = max(0, total_items - 20)

# Retrieve the last 20 items using limit and offset
last_20_items = vectorstore._collection.get(limit=20, offset=offset)

for i, item in enumerate(last_20_items["documents"], start=1):
    print(f"Item {i}:")
    print("Text:", item)
    
    # Get the corresponding embedding and metadata
    embedding = last_20_items["embeddings"][i - 1]
    metadata = last_20_items["metadatas"][i - 1]
    
    print("Embedding:", embedding)
    print("Metadata:", metadata)

    # Convert the embedding into English tokens
    tokens = embedding_model.decode(embedding)
    print("English tokens:", tokens)
    print()
