from studybuddy_utils.config import Config
from langchain_openai import ChatOp
import openai
import os

class EmbeddingsModel:
    def __init__(self):

        openai_chat_model = ChatOpenAI(model="gpt-3.5-turbo")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")             
        if self.openai_api_key is None:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. Please set it to your OpenAI API key."
            )
        self.async_client = AsyncOpenAI()
        self.client = OpenAI()
        print("EmbeddingModel set "+Config.embeddings_model_name)
