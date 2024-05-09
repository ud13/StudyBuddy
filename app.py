import os
from flask import Flask, render_template, render_template_string, request, session
from studybuddy_utils.text_utils import SBDocLoader
from studybuddy_utils.vectorstore import IndexBuilder
from studybuddy_utils.reasoning import SimpleChain
from studybuddy_utils.flaskchat import SBFlaskBackend

from uuid import uuid4

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Details on the Secret Key: https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing
#       the session data.
app.secret_key = 'BAD_SECRET_KEY'

backend = SBFlaskBackend()
chain = None


@app.route('/', methods=['GET', 'POST'])
def prepare_index():
    # create a uuid to distinguish this session from others
    
    print(f'**** request.method={request.method}')
    if request.method == 'POST':
        session_uuid = 'dev'
        # session_uuid=uuid4().hex[0:8]  # to be uncommented for prod
        session['uuid'] = session_uuid
        session['total_grade']=0
        print(f'**** session_uuid={session_uuid}')
        filepath=backend.upload_handler(request.files, session_uuid=session_uuid )
        print(f'***** filepath={filepath}')
        
        # load the docs and create chunks
        sbdocs_loader = SBDocLoader(filepath)
        chunks = sbdocs_loader.load_and_parse_pdf(filepath)

        # embed and create index (vector store)
        IndexBuilder(chunks, session_uuid=session_uuid)
        question = 'dynamic question 1'
        session['question'] = question
        answer = ''
        session['answer'] = answer
        return render_template('question.html', question=question, answer=answer )
    else:
        return render_template('index.html')

@app.route('/answer', methods=['GET', 'POST'])
def chat():
    session_uuid = session['uuid']
    print(f'***** session_uuid')
    index = IndexBuilder(None, session_uuid=session_uuid)
    qdrant_retriever = index.retriever
    chain = SimpleChain(qdrant_retriever)
    print(f'***** chain found={type(chain)}')
    user_answer = request.form['user_answer']
    print(f'**** user_answer={user_answer}')
    response = chain.reason(user_answer)
    print(f'**** response={response}')
    total_grade = 13  # tbd ausrechnen
    grade = 7 # tbd ermitteln
    session['total_grade'] = total_grade
    session['grade'] = grade
    session['answer'] = user_answer
    question = session['question']
    return render_template('grade.html', 
                           question=question, 
                           answer=user_answer, 
                           grade=grade, 
                           total_grade=total_grade)
    
@app.route('/next', methods=['GET', 'POST'])
def decide_next_step():
    print(f'***** session_uuid={session["uuid"]}')
    print(f'**** form value={request.form.get("button_action")}')
       
    if request.form.get('button_action') == 'next':
        question = 'dynamic question 2'
        session['question'] = question
        answer = ''
        session['answer'] = answer
        session['grade'] = 0
        return render_template('question.html', 
                               question=question, 
                               answer=answer )
    
    elif request.form.get('button_action') == 'explain':
        question = session['question']
        answer = session['answer']
        grade = session['grade']
        total_grade = session['total_grade']
        explanation = 'my explanation' #tbd generieren
        return render_template('explain.html', 
                               question=question, 
                               answer=answer, 
                               grade=grade, 
                               total_grade=total_grade,
                               explanation=explanation)
 
    elif request.form.get('button_action') == 'history':
        # Code to handle the "Delete" actio
        return "history pressed"
    elif request.form.get('button_action') == 'end':
        # Code to handle the "Delete" actio
        return "end pressed"
    else:
        return "Unknown action" # tbd: handle this case


if __name__ == '__main__':
    app.run(port=8000, debug=True)    
    
    