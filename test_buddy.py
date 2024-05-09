# Script to test everything and to prepare Chainlit

from dotenv import load_dotenv

from studybuddy_utils.text_utils import SBDocLoader
from studybuddy_utils.vectorstore import IndexBuilder
from studybuddy_utils.reasoning import SimpleChain
from studybuddy_utils.config import Config
from studybuddy_utils.prompts import TestPrompt
import json
from uuid import uuid4

load_dotenv()


path = path = 'studybuddy_utils/'
session_uuid=uuid4().hex[0:8]
session_uuid='dev'

# load the docs and create chunks
sbdocs_loader = SBDocLoader(path)
chunks = sbdocs_loader.load_and_parse_pdf(Config.pdf_path)

# embed and create index (vector store)
index = IndexBuilder(chunks, session_uuid=session_uuid)
qdrant_retriever = index.retriever

# execute the chain
chain = SimpleChain(qdrant_retriever)
query = TestPrompt.query
response = chain.reason(query)
json_response = json.loads(response)
# display the result
print(json_response['question'])
print(json_response['answer'])
