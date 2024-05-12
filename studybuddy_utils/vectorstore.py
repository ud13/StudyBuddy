# All about Vector Store
from studybuddy_utils.config import Config
from langchain_community.vectorstores import Qdrant
from langchain_community.vectorstores import FAISS

from studybuddy_utils.models import SBEmbeddingsModel


from qdrant_client import QdrantClient, models


class IndexBuilderQdrant:
    # Not working should use a server-database and not local persistence
    def __init__(self, split_chunks, session_uuid: str):
        print(f'**** session_uuid={session_uuid}')
        persist_dir=Config.persist_dir
        if session_uuid:
            persist_dir = Config.persist_dir+session_uuid
            
        print(f'**** persist_dir={persist_dir}')
        embedding_model = SBEmbeddingsModel().embedding_model
        if (split_chunks):    # we have gotten chunks -> create the store
            self.qdrant_vectorstore = Qdrant.from_documents(
                split_chunks,
                embedding_model,
                # location=":memory:",
                path=persist_dir,
                collection_name=Config.collection_name,
            )
        else: # no chunks received -> try to read the store , risk http=500 (tbd error-handling)
            client = QdrantClient(path=persist_dir) 
            self.qdrant_vectorstore = Qdrant(
                client=client, 
                collection_name=Config.collection_name, 
                embeddings=embedding_model,
            )
            
        self.retriever = self.qdrant_vectorstore.as_retriever()
    
class IndexBuilderFAISS:
    def __init__(self, split_chunks, session_uuid: str):
        print(f'**** session_uuid={session_uuid}')
        embedding_model = SBEmbeddingsModel().embedding_model
        self.vector_store = FAISS.from_documents(split_chunks, embedding_model)
        self.retriever = self.vector_store.as_retriever()

            