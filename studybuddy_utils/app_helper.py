
from werkzeug.utils import secure_filename
from studybuddy_utils.vectorstore import IndexBuilderQdrant
from studybuddy_utils.reasoning import SBChains
from studybuddy_utils.config import Config
from studybuddy_utils.text_utils import SBDocLoader
from studybuddy_utils.vectorstore import IndexBuilderFAISS
from studybuddy_utils.prompts import ExamPrompt

import os
import json

class AppHelper:
    def __init__(self):
        self.sbchains = None
        
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

    def generate_question(self, filepath, topic, session_uuid):
        chunks = None
        if filepath is not None:
            # load the docs and create chunks
            sbdocs_loader = SBDocLoader(filepath)
            chunks = sbdocs_loader.load_and_parse_pdf(filepath)

        # embed and create index (vector store)
        index = IndexBuilderFAISS(chunks, session_uuid=session_uuid)
        retriever = index.retriever
        self.sbchains = SBChains(retriever)
        print(f'****** topic={topic}')
        response = self.sbchains.generate_question(topic)
        json_response = json.loads(response)
        return json_response
    
    def evaluate_question(self, question, ideal_answer, answer):
        response = self.sbchains.evaluate_answer(question, ideal_answer, answer)
        json_response = json.loads(response)
        return json_response
    
    def find_topics(self, file):
        retriever = None
        sbd = SBChains(retriever)
        return sbd.find_topics(file)