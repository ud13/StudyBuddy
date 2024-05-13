
from flask import Flask, g, render_template, render_template_string, request, session
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

    print(f'**** request.method={request.method}')    
    if request.method == 'POST':
        session_uuid = 'dev'
        # session_uuid=uuid4().hex[0:8]  # to be uncommented for prod
        session['uuid'] = session_uuid
        session['total_grade'] = 0
        session['max_grade'] = 0
        print(f'**** session_uuid={session_uuid}')
        filepath = apphelper.upload_handler(request.files, session_uuid=session_uuid )
        print(f'***** filepath={filepath}')
        print(f'***** start finding topics')
        topic_list = apphelper.find_topics(filepath)
        session['topic_list'] = topic_list
        last_topic_used = 0
        session['last_topic_used'] = last_topic_used
        topic = topic_list[last_topic_used]
        
        json_response = apphelper.generate_question(filepath, topic, session_uuid)
        
        print(f'**** json_response={json_response}')
        question = json_response['question']
        model_answer = json_response['answer']
        session['question'] = question
        session['model_answer'] = model_answer
        session['filepath'] = filepath
        
        print(f'*** question={question}')
        print(f'*** model_answer={model_answer}')
        answer = ''
        session['answer'] = answer
        return render_template('question.html', question=question, answer=answer, topic=topic )
    else:
        return render_template('index.html')

@app.route('/answer', methods=['GET', 'POST'])
def chat():
    # create a uuid to distinguish this session from others
    session_uuid = session['uuid']
    print(f'***** session_uuid={session_uuid}')
    user_answer = request.form.get('user_answer')
    model_answer = session['model_answer'] 
    question = session['question'] 
    
    # tbd hier scores fertig ausrechner
    json_response = apphelper.evaluate_question(question, 
                                                model_answer, 
                                                user_answer)
    print(json_response)
    clarity = json_response['clarity']
    faithfulness = json_response['faithfulness']
    correctness = json_response['correctness']
    
    grade = 0.9 * correctness + 0.05 * clarity + 0.05 * faithfulness
    
    total_grade = session['total_grade']
    total_grade += grade
    session['total_grade'] = total_grade
    session['max_grade'] += 10
    max_grade = session['max_grade']

    session['grade'] = grade
    session['answer'] = user_answer
    question = session['question']
    return render_template('grade.html', 
                        question=question, 
                        answer=user_answer, 
                        grade=round(grade, 2), 
                        total_grade=round(total_grade, 2),
                        max_grade=max_grade)
    
    
@app.route('/next', methods=['GET', 'POST'])
def decide_next_step():
    print(f'***** session_uuid={session["uuid"]}')
    print(f'**** form value={request.form.get("button_action")}')
       
    if request.form.get('button_action') == 'next':
        print (f'*** next pressed')
        filepath = session['filepath']
        topic_list = session['topic_list']
        last_topic_used = session['last_topic_used'] + 1
        session['last_topic_used'] = last_topic_used
        topic = topic_list[last_topic_used]
        
        json_response = apphelper.generate_question(filepath, topic, session["uuid"])
        
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
                               answer=answer,
                               topic=topic)
    
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
    
    