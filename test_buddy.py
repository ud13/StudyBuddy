# Script to test everything and to prepare Chainlit

from dotenv import load_dotenv

from studybuddy_utils.text_utils import SBDocLoader
from studybuddy_utils.config import Config
from studybuddy_utils.app_helper import AppHelper


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


print("**** Execute the Chain and generate a exam-question-answer-pair")

# execute the chain
apphelper = AppHelper()
filepath = Config.pdf_path
(json_response, index) = apphelper.generate_question(filepath, session_uuid)
print(json_response['question'])
print(json_response['answer'])

question = json_response['question']
ideal_answer = json_response['answer']
answer = ideal_answer
answer = "Is almost like a dense index"

print("**** Execute the Chain and evaluate a answer")
# execute the chain for evaluation

json_response = apphelper.evaluate_question(question, ideal_answer, answer)
clarity = json_response['clarity']
faithfulness = json_response['faithfulness']
correctness = json_response['correctness']

print(f'clarity={clarity} faithfulness={faithfulness} correctness={correctness}')
