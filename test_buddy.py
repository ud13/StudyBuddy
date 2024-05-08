# Script to test everything and to prepare Chainlit

from dotenv import load_dotenv

from studybuddy_utils.text_utils import SBDocLoader
from studybuddy_utils.vectorstore import IndexBuilder
from studybuddy_utils.reasoning import SimpleChain

load_dotenv()


path = path = 'studybuddy_utils/'

# load the docs and create chunks
sbdocs_loader = SBDocLoader(path)
chunks = sbdocs_loader.load_and_parse_pdf_dir()

# embed and create index (vector store)
index = IndexBuilder(chunks)
qdrant_retriever = index.retriever

# execute the chain
chain = SimpleChain(qdrant_retriever)
question = "What is the meaning of the number 42 in Douglas Adam's Hitchhicker's Guide?"
response = chain.reason(question)

# display the result
print(response)
