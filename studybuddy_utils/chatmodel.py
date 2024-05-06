from studybuddy_utils.config import Config
from langchain_openai import ChatOpenAI

import os

class ChatModel:
    def __init__(self):
        # self.openai_chat_model = ChatOpenAI(model=Config.chat_model)
        self.openai_chat_model = 'gugus'
        
        print("MidtermChatModel set " + self.openai_chat_model.model_name)

