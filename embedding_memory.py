from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Extra
from context_manager import get_chat_history  
import logging

logging.basicConfig(
    filename='chat_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
)

class EmbeddingMemory(ConversationBufferMemory):
    """
    Memory class using embeddings to store and retrieve conversation history.
    """

    class Config:
        extra = Extra.allow

    def __init__(self, vectorstore, llm, summary_frequency=5):
        super().__init__(llm=llm, memory_key="chat_history", input_key="input", output_key="output")
        self.vectorstore = vectorstore
        self._summary_frequency = summary_frequency
        self.turn_count = 0

    def load_memory_variables(self, question):
        """Loads relevant context from vectorstore based on the current question."""
        logging.info("Loading memory variables")

        inputs = {"question": question}
        question_embedding = self.vectorstore._embedding_function.embed_query(question)

        # Retrieve top 5 most similar results (not used for now)
        results = self.vectorstore.similarity_search_by_vector(question_embedding, k=5)

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
        """Saves the current interaction to memory and the vectorstore. """
        logging.info("Saving context")
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
        """Summarizes the conversation history using the LLM."""
        logging.info("Summarizing history")
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
