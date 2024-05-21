from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Initialize Embedding Model and Vectorstore
embedding_model = OllamaEmbeddings(model="all-minilm")  # Or your preferred model
vectorstore = Chroma("my_test_context", embedding_function=embedding_model)

# 2. Example Questions and Chat History
questions = [
    "What is the capital of France?",
    "How do I make a cup of tea?",
    "Tell me about artificial intelligence."
]
chat_histories = [
    "User: Hi\nAgent: Hello!",
    "User: What's your name?\nAgent: I'm a chatbot.",
    "User: What can you do?\nAgent: I can answer questions."
]

# 3. Update Context for Each Question
for question, chat_history in zip(questions, chat_histories):
    # Embed the question
    question_embedding = embedding_model.embed_query(question)

    # Add to vectorstore with metadata
    vectorstore.add_texts(
        texts=[question],
        embeddings=[question_embedding],
        metadatas=[{"history": chat_history}]
    )

# 4. Test Retrieval
test_question = "What is the weather like today?"
test_embedding = embedding_model.embed_query(test_question)

# Get similar documents and scores using similarity_search_with_score
results_and_scores = vectorstore.similarity_search_with_score(test_question, k=2) 

# Print results
print("Test Question:", test_question)
for result, score in results_and_scores:
    print("-" * 20)
    print("Similar Question:", result.page_content)
    print("Similarity Score:", score)
    print("Chat History:", result.metadata["history"])
