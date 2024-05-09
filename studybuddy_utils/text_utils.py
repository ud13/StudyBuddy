# Loading, from studybuddy_utils.config import ConfigCleaning, Chunking
from studybuddy_utils.config import Config
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

# tbd can we also set verbose as in LlamaIndex

class SBDocLoader:
    def __init__(self, path: str = "./data"):
        # tbd wo muss das hin - hier oder in ipynb
        OpenAIEmbeddings(model=Config.embeddings_model_name)
        self.path = path
        """
        self.parser = parser = LlamaParse(
            result_type="text",  # "markdown" and "text" are available
         verbose=verbose,
        )          
        """      
    # tbd use LlamaIndex here?
    # tbd is async possible or necessary?
    def load_and_parse_pdf(self, path):
        docs = PyMuPDFLoader(path).load()
        chunks = self.chunk_docs(docs)
        return(chunks)
    
    # length function for the text_splitter
    def tiktoken_len(self,text):
        tokens = tiktoken.encoding_for_model(Config.chat_model).encode(
            text,
        )
        return len(tokens) 
 
                  
    def chunk_docs(self, docs):
        # tbd for other models, that do not use tiktoken, this must be adjusted
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = Config.chunk_size,
            chunk_overlap = Config.chunk_overlap,
            length_function = self.tiktoken_len, 
        )
        split_chunks = text_splitter.split_documents(docs)
        self.control_chunks(split_chunks) 
        return split_chunks

    def control_chunks(self, split_chunks):
        print(f'# of chunks: {len(split_chunks)}')
        
        max_chunk_length = 0
        for chunk in split_chunks:
            max_chunk_length = max(max_chunk_length, self.tiktoken_len(chunk.page_content)) # type: ignore
        print(f'# max chunk len: {max_chunk_length}')
        
if __name__ == "__main__":
    sbd = SBDocLoader("path")
    chunks = sbd.load_and_parse_pdf_dir()