from studybuddy_utils.config import Config
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

class SBEmbeddingsModel:
    def __init__(self):    
        self.embedding_model = OpenAIEmbeddings(model=Config.embeddings_model_name)
        print("EmbeddingModel set "+Config.embeddings_model_name)

class SBChatModel:
    def __init__(self):
        self.openai_chat_model = ChatOpenAI(model=Config.chat_model)       
        print("ChatModel set " + self.openai_chat_model.model_name)
    