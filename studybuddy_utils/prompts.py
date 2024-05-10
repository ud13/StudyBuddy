# Prompts used in this project

class TestPrompt:
    prompt = """
    SYSTEM: 
    You are an university professor for undergraduate compute science specialized in Information Retrieval.
    Generate a question for a written closed-book exam and generate a short answer which merits a top grade.
    
     
    CONTEXT:
    {context}

    QUERY:
    {question}
    
    Use the provide context to answer the provided user query. Only use the provided context to answer the query. If you do not know the answer, response with "I don't know"
    Provide your answer as JSON with two keys 'question' and 'answer'.
    If you don't find the topic in the context, then return an empty set.
    """

    query = """
    
    Topic of the question is 'inverted index'.
    
    """

###### Old Prompts used to setup
class FirstPrompts:
    system_template = "You are a legendary and mythical Wizard. You speak in riddles and make obscure and pun-filled references to exotic cheeses."
    human_template = "{content}"
    
class SecondPrompts:
    system_template = "You are a helpful assistant."
    human_template = "{content}"
    
class ThirdPrompts:
    HUMAN_TEMPLATE = """
    #CONTEXT:
    {context}

    QUERY:
    {query}

    Use the provide context to answer the provided user query. Only use the provided context to answer the query. If you do not know the answer, response with "I don't know"
    """

    CONTEXT = """
    LangChain Expression Language or LCEL is a declarative way to easily compose chains together. There are several benefits to writing chains in this manner (as opposed to writing normal code):

    Async, Batch, and Streaming Support Any chain constructed this way will automatically have full sync, async, batch, and streaming support. This makes it easy to prototype a chain in a Jupyter notebook using the sync interface, and then expose it as an async streaming interface.

    Fallbacks The non-determinism of LLMs makes it important to be able to handle errors gracefully. With LCEL you can easily attach fallbacks to any chain.

    Parallelism Since LLM applications involve (sometimes long) API calls, it often becomes important to run things in parallel. With LCEL syntax, any components that can be run in parallel automatically are.

    Seamless LangSmith Tracing Integration As your chains get more and more complex, it becomes increasingly important to understand what exactly is happening at every step. With LCEL, all steps are automatically logged to LangSmith for maximal observability and debuggability.
    """
    
class RAGPrompt:
    prompt = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    Only use the context provided. If the context provided does not answer the question, then answer with 'I don't know the answer to that question based on the provided context.'. 
    """
