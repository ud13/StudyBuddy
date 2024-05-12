# do the reasoning and the chain

from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter

from langchain.schema.runnable import RunnablePassthrough
from studybuddy_utils.models import SBChatModel
from studybuddy_utils.prompts import ExamPrompt
from studybuddy_utils.prompts import EvaluationPrompt
from studybuddy_utils.models import SBChatModel
from langchain_core.prompts import ChatPromptTemplate

class SBChains:
    def __init__(self, retriever):
        self.openai_chat_model = SBChatModel().openai_chat_model
        self.rag_prompt = ChatPromptTemplate.from_template(ExamPrompt().prompt)
        self.retriever = retriever
        
    def reason(self, question):
        
        retrieval_augmented_qa_chain = (
            # INVOKE CHAIN WITH: {"question" : "<<SOME USER QUESTION>>"}
            # "question" : populated by getting the value of the "question" key
            # "context"  : populated by getting the value of the "question" key and chaining it into the base_retriever
            {"context": itemgetter("question") | self.retriever, "question": itemgetter("question")}
            # "context"  : is assigned to a RunnablePassthrough object (will not be called or considered in the next step)
            #              by getting the value of the "context" key from the previous step
            | RunnablePassthrough.assign(context=itemgetter("context"))
            # "response" : the "context" and "question" values are used to format our prompt object and then piped
            #              into the LLM and stored in a key called "response"
            # "context"  : populated by getting the value of the "context" key from the previous step
            | {"response": self.rag_prompt | self.openai_chat_model, "context": itemgetter("context")}
        )

        response = retrieval_augmented_qa_chain.invoke({"question" : question})
        print(f'***** response={response["response"].content}')
        return response['response'].content
    
    def one_step_reason(self, question, ideal_answer, answer):
        # tbd benöigt sicher noch einen Retriever, um noch Kontext in die Eval reinzubringen
        chat_prompt = ChatPromptTemplate.from_messages([
                    ("system", EvaluationPrompt.system_prompt),
                    ("human", EvaluationPrompt.human_prompt)
                ])
        chain = chat_prompt | SBChatModel().openai_chat_model
        
        response = chain.invoke({"question": question, 
                        "ideal_answer": ideal_answer,
                        "student_answer": answer})
        return response.content
            
            
            