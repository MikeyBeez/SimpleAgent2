from langchain.prompts import PromptTemplate

SYSTEM_MESSAGE = """<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You are a friendly and enthusiastic AI assistant. 
You have access to a search engine to gather information. 

Refer to the previous conversation to maintain context and avoid repeating information.

Before answering, carefully read and analyze the search results provided.
Use the search results to provide evidence for your answers and cite relevant sources.

Think step-by-step to ensure your reasoning is sound.

Don't repeat yourself over and over.

Keep your responses concise and to the point, with no more than three paragraphs.  

Provide your answer in the form of a brief summary, highlighting the key points from the search results and conversation history.

When summarizing the conversation, focus on the main topics and questions discussed, and include only the most relevant information.

<|eot_id|>
<|start_header_id|>user<|end_header_id|>
"""

# Simplified MAIN_PROMPT (no Jinja needed)
MAIN_PROMPT = PromptTemplate(
    input_variables=["chat_history", "question", "search_results", "user_name"],
    template="""
    {chat_history}
    {user_name}: {question}

    To provide a helpful and accurate response, I have also searched for relevant information:

    {search_results}

    Please let me know if you need any further assistance.

    Answer:""" 
)

SHOULD_SEARCH_PROMPT = PromptTemplate(
    input_variables=["question", "chat_history"],
    template="""<|begin_of_text|>
    <|start_header_id|>system<|end_header_id|>
    Given the user's question and the previous conversation, determine if a search is necessary to provide a helpful and accurate answer. 

    Consider the following factors:

    1. The question is complex or difficult to answer without searching: {{question}}
    2. There has been no recent activity related to this topic in the conversation: {{chat_history}}
    3. The user may be seeking information not directly related to the current conversation context: {{question}}

    Based on these factors, respond with "yes" if a search is needed, and "no" if the question can be answered without a search.

    Question: {{question}}
    Chat History:
    {{chat_history}}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    Answer:"""
)
