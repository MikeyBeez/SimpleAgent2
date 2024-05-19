def update_context(question, chat_history, embeddings, chat_history_embeddings):
    question_embedding = embeddings.embed_query(question)
    chat_history_embeddings.append(question_embedding)
