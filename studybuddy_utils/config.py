# Config for StudyBuddy


class Config:
    # Parameters for embedding  model
    embeddings_model_name='text-embedding-ada-002'
    # embeddings_model_name='text-embedding-3-small'
    embeddings_model_size=1536

    # parameters for collection and store
    collection_name='test_collection'
    persist_dir='./storage_test'

    # the file name
    pdf_path='data/midterm-data.pdf'
    pickle_path='data/nodes.pickle'

    # paramteters for chunking
    verbose=True
    chunk_size=128
    chunk_overlap=30
    # separator=" "  Blank is default

    # parametrs for retrieval
    distance='Cosine'
    similarity_top_k=50
    similarity_cutoff=0.4

    # parameters for the chat model
    chat_model='gpt-3.5-turbo'
    temperature=0.0
    max_tokens=2048
    streaming=True
    context_window=4096



