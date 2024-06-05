from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Extra
from chat_loop_modules.context_manager import get_chat_history
import logging
import config

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

        # Retrieve top N results with similarity scores
        results = self.vectorstore.similarity_search_with_score(
            question_embedding,
            k=TOP_N_RESULTS
        )

        logging.info(f"Retrieved {len(results)} results from the vectorstore.")

        # Filter results based on the similarity score
        filtered_results = [result for result in results if result[1] >= SIMILARITY_THRESHOLD]

        logging.info(f"After filtering, {len(filtered_results)} relevant results remain.")

        # Load context into ConversationBufferMemory
        for result in filtered_results:
            document = result[0]
            if isinstance(document, str):
                # If the document is a string, use it directly
                text = document
            else:
                # If the document is not a string, try to access the 'text' key in the metadata
                text = document.metadata.get('text', '')

            if text.startswith('User'):
                self.chat_memory.add_user_message(HumanMessage(content=text.split('User: ')[1]))
            elif text.startswith('Chatbot'):
                self.chat_memory.add_ai_message(AIMessage(content=text.split('Chatbot: ')[1]))

        return {"history": [result[0].metadata.get('text', '') for result in filtered_results]}

    def save_context(self, inputs, outputs):
        """Saves the current interaction to memory and the vectorstore."""
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
            "text": qa_pair_text,
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

        logging.info("Added current interaction to the vectorstore.")

        # Update the base ConversationBufferMemory
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

    def filter_context(self, context, question):
        """Filters the context based on relevance to the current question."""
        if config.DEBUG:
            print("DEBUG: Filtering context based on relevance...")

        filtered_context = []
        for message in context:
            if self.is_relevant(message, question):
                filtered_context.append(message)

        return filtered_context

    def is_relevant(self, message, question):
        """Determines if a message is relevant to the current question."""
        # Implement your relevance logic here
        # For example, you can use string matching, keyword extraction, or semantic similarity
        # Return True if the message is relevant, False otherwise
        # You can adjust the relevance criteria based on your specific requirements
        return True  # Placeholder implementation, replace with your own logic
