from prompts import SHOULD_SEARCH_PROMPT
import spacy
from scipy.spatial.distance import cosine

def should_search(question, chat_history, llm, embeddings, chat_history_embeddings):
    # Check for common greetings
    common_greetings = ["hello", "hi", "hey", "good morning", 
                        "good afternoon", "good evening", "good night", 
                        "goodbye", "bye", "see you later", "talk to you later"]
    if question.lower() in common_greetings:
        return False

    # Check for simple questions
    simple_questions = ["how are you?", "what's up?", "how's it going?", 
                        "what's your name?", "what can you do?", "what's the time?"]
    if question.lower() in simple_questions:
        return False

    # Check for contextual similarity
    question_embedding = embeddings.embed_query(question)
    if chat_history_embeddings:
        similarities = [1 - cosine(question_embedding, embedding) 
                        for embedding in chat_history_embeddings]
        most_similar_index = similarities.index(max(similarities))
        most_similar_score = similarities[most_similar_index]
        if most_similar_score > 0.8:  # Adjust threshold as needed
            return False

    # If none of the checks pass, use the LLM to determine if a search is needed
    response = llm.invoke(
        SHOULD_SEARCH_PROMPT.format(question=question, chat_history=chat_history)
    ).strip()
    return response.lower() == "yes"
