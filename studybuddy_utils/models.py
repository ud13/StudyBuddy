from studybuddy_utils.config import Config
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from sentence_transformers import SentenceTransformer

class SBEmbeddingsModel:
    def __init__(self):    
        if Config.embedding_type == 'openai':
            self.embedding_model = OpenAIEmbeddings(model=Config.embeddings_model_name)
            print("EmbeddingModel set "+Config.embeddings_model_name)
        elif Config.embedding_type == 'ud-ir-m':
            # self.embedding_model = SentenceTransformer(Config.embeddings_model_name)  # This will download the model if needed
            self.embedding_model = HuggingFaceEmbeddings(model_name=Config.embeddings_model_name)
    

class SBChatModel:
    def __init__(self):
        self.openai_chat_model = ChatOpenAI(model=Config.chat_model,
                                            temperature=Config.temperature,
                                            max_tokens=Config.max_tokens,
                                            )
        print("ChatModel set " + self.openai_chat_model.model_name)
    