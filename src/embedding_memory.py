from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Extra
from chat_loop_modules.context_manager import get_chat_history
import logging

logging.basicConfig(
    filename='chat_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
)

TOP_N_RESULTS = 5  # Adjust the value as needed
SIMILARITY_THRESHOLD = 0.8  # Adjust the value as needed

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

        # Retrieve top N most similar results
        results = self.vectorstore.similarity_search_by_vector(
            question_embedding,
            k=TOP_N_RESULTS
        )

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
        logging.info("Saving context")

        # Get the user input and chatbot response
        user_input = inputs['input']
        chatbot_response = outputs['output']

        # Create the question-answer pair text
        qa_pair_text = f"User: {user_input}\nChatbot: {chatbot_response}"

        # Generate the embedding for the question-answer pair
        qa_pair_embedding = self.vectorstore._embedding_function.embed_query(qa_pair_text)

        # Create metadata for the question-answer pair
        metadata = {
            "user_input": user_input,
            "chatbot_response": chatbot_response,
            "source": "conversation"
        }

        # Add the question-answer pair text, embedding, and metadata to the vectorstore
        self.vectorstore.add_texts(
            texts=[qa_pair_text],
            embeddings=[qa_pair_embedding],
            metadatas=[metadata]
        )

        # Update the base ConversationBufferMemory with the user input and chatbot response
        super().save_context(inputs, outputs)

        # Increment the turn count
        self.turn_count += 1

        # Summarize the conversation history if the turn count reaches the summary frequency
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
