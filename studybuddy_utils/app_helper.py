
from werkzeug.utils import secure_filename
from studybuddy_utils.vectorstore import IndexBuilder
from studybuddy_utils.reasoning import SimpleChain
from studybuddy_utils.config import Config
from studybuddy_utils.text_utils import SBDocLoader
from studybuddy_utils.vectorstore import IndexBuilder
from studybuddy_utils.prompts import TestPrompt
import os
import json

class AppHelper:
    def __init__(self):
        self.readme = 'tbd constructor'
        
    def upload_handler(self, files, session_uuid: str):
        if 'file' not in files:
            return 'No file selected.'

        file = files['file']

        # Basic filename security
        filename = secure_filename(session_uuid + file.filename)

        # Ensure it's a PDF
        if not filename.lower().endswith('.pdf'):
            return 'Invalid file type. Please upload a PDF.'

        filepath = os.path.join(Config.uploads_path, filename)
        file.save(filepath)

        file_size = os.path.getsize(filepath)
        print(f'****** file_size={file_size}')
        return filepath


    def generate_question(self, filepath, session_uuid):
        chunks = None
        if filepath is not None:
            # load the docs and create chunks
            sbdocs_loader = SBDocLoader(filepath)
            chunks = sbdocs_loader.load_and_parse_pdf(filepath)

        # embed and create index (vector store)
        index = IndexBuilder(chunks, session_uuid=session_uuid)
        qdrant_retriever = index.retriever
        chain = SimpleChain(qdrant_retriever)
        query = TestPrompt.query
        print(f'****** query={query}')
        response = chain.reason(query)
        json_response = json.loads(response)
        return json_response
    