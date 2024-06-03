from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

embedding_model = OllamaEmbeddings(model="all-minilm")
vectorstore = Chroma("my_context", embedding_function=embedding_model)

# Retrieve the last 20 items stored in Chroma
last_20_items = vectorstore.get_documents()[-20:]

for i, item in enumerate(last_20_items, start=1):
    print(f"Item {i}:")
    print("Text:", item.page_content)
    print("Embedding:", item.embedding)

    # Convert the embedding into English tokens
    tokens = embedding_model.decode(item.embedding)
    print("English tokens:", tokens)
    print()
