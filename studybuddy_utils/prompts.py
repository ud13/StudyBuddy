# Prompts used in this project
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate

class ExamPrompt:
    system_prompt = """
SYSTEM: 
You are an university professor for undergraduate compute science specialized in Information Retrieval.
Generate a question for a written closed-book exam and generate a short answer which merits a top grade.

Don't refer to the provided context - better include the necessary context in question you generate.
If you don't find the topic in the context, then return an empty set.
    
CONTEXT:
{context}


QUERY:
Topic of the question is
{question}

Use the provided context to generate a question provided in the user-query. 
In the question you generate, never refer to the provided context. 
Only use the provided context to answer the query. 
If you do not know the answer, response with "I don't know"
Provide your answer as JSON with two keys 'question' and 'answer'.

"""

class EvaluationPrompt:
    system_prompt = """
You are a university professor grading a quiz in information retrieval.

You should be hyper-critical.

Provide scores (out of 10) for the following attributes:

1. Clarity - how clear is the response
2. Relatedness - how related to the original query is the response
3. Correctness - was the response correct?

Provide also a textual explanation about the scores.

The question is given below:

---------------------
{question}
---------------------

Given the question score the user's answer based on the ideal answer provided here:

---------------------
{ideal_answer}
---------------------

If you don't know then simply provide scores -1.
When you are done -  please provide your response in a JSON format with the following keys 
'clarity', 'faithfulness', 'correctness', 'explanation'.

"""

    human_prompt = """
Based on the information given, score the following answer:
---------------------
{student_answer}
---------------------
"""
    
class TopicsPrompt:
    system_prompt = """
Extract topics from the following text and also write down
three possible different subthemes. 

Do not mention the word "topic" or „article“ when describing the topics.
Do not generate topics containing the words 'Ursula' 'Deriu', 'licensed', 'Manning'
Use the following template for the response. Generate 10 themes. 
Do not number the themes. Do not use bulletpoints.

Do not provide an introduction or a conclusion, only describe the topics.
Do not privide empty topics.

Here the template:
Phrase describing the topic.
Phrase describing the topic.
"""
        
    human_prompt = """
        Here the text:
        {text}
        """