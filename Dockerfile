FROM python:3.11
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app
COPY --chown=user . $HOME/app
COPY ./requirements.txt ~/app/requirements.txt
# RUN pip install -r requirements.txt
RUN pip install numpy==1.26.4
RUN pip install pandas==2.2.2
RUN pip install matplotlib==3.8.4
RUN pip install huggingface_hub==0.22.2
RUN pip install jupyter==1.0.0
# RUN pip install chainlit==0.7.700
RUN pip install openai==1.23.6
RUN pip install tiktoken==0.6.0
RUN pip install python-dotenv==1.0.1
RUN pip install qdrant-client==1.9.0
RUN pip install langchain==0.1.17
RUN pip install langchain-core==0.1.52
RUN pip install langchain-community==0.0.37
RUN pip install langchain-openai==0.1.6
RUN pip install pymupdf==1.24.2
RUN pip install Flask=3.0.3
RUN pip install sentence_transformers==2.7.0
COPY . .
CMD ["chainlit", "run", "app.py", "--port", "7860"]