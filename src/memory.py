from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Extra
from chat_loop_modules.context_manager import get_chat_history
from config import SIMILARITY_THRESHOLD, TOP_N_RESULTS

class EmbeddingMemory(ConversationBufferMemory):
    """
    Memory class that uses embeddings to store and retrieve conversation history.
    """

    class Config:
        extra = Extra.allow

    def __init__(self, vectorstore, llm, summary_frequency=5): 
        super().__init__(llm=llm, memory_key="chat_history", input_key="input", output_key="output")
        self.vectorstore = vectorstore  
        self._summary_frequency = summary_frequency
        self.turn_count = 0

    def load_memory_variables(self, question):
        """
        Loads relevant context from the vectorstore based on the current question.
        """
        # Create the inputs dictionary here
        inputs = {"question": question}

        question_embedding = self.vectorstore._embedding_function.embed_query(question)

        # Retrieve top N most similar results based on similarity threshold
        results = self.vectorstore.similarity_search_by_vector(
            question_embedding,
            k=TOP_N_RESULTS,
            score_threshold=SIMILARITY_THRESHOLD
        )

        # Print the retrieved embeddings and convert them into English tokens
        for i, result in enumerate(results):
            print(f"Embedding {i+1}:")
            print(result.embedding)

            # Convert the embedding into English tokens
            tokens = self.vectorstore._embedding_function.decode(result.embedding)
            print(f"English tokens {i+1}:")
            print(tokens)
            print()

        # Get the chat history directly:
        chat_history = get_chat_history() 

        # Load context into ConversationBufferMemory
        for message in chat_history: 
            if message.startswith('User'):
                self.chat_memory.add_user_message(HumanMessage(content=message.split('User: ')[1]))
            elif message.startswith('Chatbot'):
                self.chat_memory.add_ai_message(AIMessage(content=message.split('Chatbot: ')[1]))

        return {"history": chat_history} 

    def save_context(self, inputs, outputs):
        """
        Saves the current interaction to memory and the vectorstore. 
        """
        text = f"User: {inputs['input']}\nChatbot: {outputs['output']}"
        embedding = self.vectorstore._embedding_function.embed_query(text) 

        # Provide a dictionary or None for metadatas
        metadata = {"source": "conversation"} 
        self.vectorstore.add_texts([text], embeddings=[embedding], metadatas=[metadata]) 

        # Update the base ConversationBufferMemory 
        super().save_context(inputs, outputs) 

        self.turn_count += 1
        if self.turn_count % self._summary_frequency == 0:  
            self.summarize_history(inputs, outputs)

    def summarize_history(self, inputs, outputs):
        """
        Summarizes the conversation history using the LLM.
        """
        messages = self.chat_memory.messages
        if len(messages) == 0:
            return

        summarization_prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "system",
                    "Condense the above chat messages into a single, concise summary message. "
                    "Include important details and user requests."
                ),
            ]
        )
        summarization_chain = summarization_prompt | self.llm

        summary_message = summarization_chain.invoke({"chat_history": messages})

        self.chat_memory.clear()  
        self.chat_memory.add_message(summary_message)
