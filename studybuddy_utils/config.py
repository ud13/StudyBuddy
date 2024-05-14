# Config for StudyBuddy


class Config:
    # select the model-type to use 'openai' 'ud-ir-m'
    embedding_type='openai'
    # Parameters for embedding  model OpenAI
    embeddings_model_name='text-embedding-ada-002'
    # embeddings_model_name='uderiu/snowflake-ft-ir2-m'
    # embeddings_model_size=1536   
    # embeddings_model_name='text-embedding-3-small'

    # parameters for collection and store
    collection_name='test_collection'
    persist_dir='./storage_test'

    # the file name
    # pdf_path='data/AI-Powered_Search_v20-6-30.pdf'
    # pdf_path='https://www.deyeshigh.co.uk/downloads/literacy/world_book_day/the_hitchhiker_s_guide_to_the_galaxy.pdf'
    # pickle_path='data/nodes.pickle'
    pdf_path='data/AI-Powered_Search_v20.pdf'

    # paramteters for chunking
    verbose=True
    chunk_size=200
    chunk_overlap=0
    # separator=" "  Blank is default

    # parametrs for retrieval
    distance='Cosine'
    similarity_top_k=50
    similarity_cutoff=0.4

    # parameters for the chat model
    chat_model='gpt-3.5-turbo'
    temperature=0.5
    max_tokens=2048
    # streaming=True
    # context_window=4096
    # top_p=1
    # frequency_penalty=0
    # presence_penalty=0
     
    # parameters for flask
    uploads_path='uploads'




