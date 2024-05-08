# All about Vector Store
from studybuddy_utils.config import Config
from langchain_community.vectorstores import Qdrant

from studybuddy_utils.models import SBEmbeddingsModel


from qdrant_client import QdrantClient, models

class IndexBuilder:
    def __init__(self, split_chunks):
        # tbd - ausprobieren, ob die geladen werden https://python.langchain.com.cn/docs/modules/data_connection/vectorstores/integrations/qdrant
        embedding_model = SBEmbeddingsModel().embedding_model
            
        self.qdrant_vectorstore = Qdrant.from_documents(
            split_chunks,
            embedding_model,
            location=":memory:",
            # path=Config.persist_dir,
            collection_name=Config.collection_name,
        )
        self.retriever = self.qdrant_vectorstore.as_retriever()