
from flask import Flask, render_template, render_template_string, request, session
from studybuddy_utils.app_helper import AppHelper


from uuid import uuid4

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Details on the Secret Key: https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing
#       the session data.
app.secret_key = 'BAD_SECRET_KEY'

apphelper = AppHelper()
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
        filepath = apphelper.upload_handler(request.files, session_uuid=session_uuid )
        print(f'***** filepath={filepath}')
        json_response = apphelper.generate_question(filepath, session_uuid)
        question = json_response['question']
        model_answer = json_response['answer']
        session['question'] = question
        session['model_answer'] = model_answer
        
        print(f'*** question={question}')
        print(f'*** model_answer={model_answer}')
        answer = ''
        session['answer'] = answer
        return render_template('question.html', question=question, answer=answer )
    else:
        return render_template('index.html')

@app.route('/answer', methods=['GET', 'POST'])
def chat():
    session_uuid = session['uuid']
    print(f'***** session_uuid')
    user_answer = request.form.get('user_answer')
    # tbd hier grading einbauen
    json_response = apphelper.generate_question(None, session_uuid)
    print(json_response)
    
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
        json_response = apphelper.generate_question(None, session["uuid"])
        question = json_response['question']
        model_answer = json_response['answer']
        session['question'] = question
        session['model_answer'] = model_answer
        
        print(f'*** question={question}')
        print(f'*** model_answer={model_answer}')
        answer = ''
        session['answer'] = answer
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
    
    