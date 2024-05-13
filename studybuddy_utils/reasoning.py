# do the reasoning and the chain

from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter

from langchain.schema.runnable import RunnablePassthrough
from studybuddy_utils.models import SBChatModel
from studybuddy_utils.prompts import ExamPrompt
from studybuddy_utils.prompts import EvaluationPrompt
from studybuddy_utils.prompts import TopicsPrompt
from studybuddy_utils.models import SBChatModel
from langchain_core.prompts import ChatPromptTemplate

from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI

class SBChains:
    def __init__(self, retriever):
        self.openai_chat_model = SBChatModel().openai_chat_model     
        self.retriever = retriever
        
    def generate_question(self, question):
        
        rag_prompt = ChatPromptTemplate.from_template(ExamPrompt().system_prompt)
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
            | {"response": rag_prompt | self.openai_chat_model, "context": itemgetter("context")}
        )

        response = retrieval_augmented_qa_chain.invoke({"question" : question})
        return response['response'].content
    
    def evaluate_answer(self, question, ideal_answer, answer):
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
            

    def find_topics(self, file, chain_type="map_reduce"):

        # generate a summary
        loader = PyPDFLoader(file)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        # Initialize LLM (Replace 'YOUR_API_KEY' with your actual OpenAI API key)
        llm = OpenAI(temperature=0, max_tokens=500)
        chain = load_summarize_chain(llm, chain_type=chain_type)  # Specify map_reduce

        summary = chain.invoke(texts)
        
        # extract topics from the summary
        topics_prompt = ChatPromptTemplate.from_messages([
                    ("system", TopicsPrompt.system_prompt),
                    ("human", TopicsPrompt.human_prompt)
                ])
        chain = topics_prompt | SBChatModel().openai_chat_model
        
        response = chain.invoke({"text": summary})
        list_of_topics = response.content.split('\n')
        print(list_of_topics)
        # tbd enhancce this list to contain tuples (topic, counter)
        # inti the counter with 0 - augment the counter each time 
        # the topic is used. 
        # Start with simple questions, for counter=0 - then medium questions 
        # for counter=1 etc
        return list_of_topics


    
        