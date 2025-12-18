import streamlit as s
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()

s.title("Langchain Chatbot with History")

llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)

if "conversation" not in s.session_state:
    s.session_state.conversation = []



        
user_input = s.chat_input("Say something...")
if user_input:
    s.session_state.conversation.append({"role": "user", "content": user_input})
    message = s.session_state.conversation    
    result = llm.invoke(message)
    s.session_state.conversation.append({"role": "assistant", "content": result.content})


for msg in s.session_state.conversation:
    with s.chat_message(msg["role"]):
        s.markdown(msg["content"])