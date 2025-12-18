import streamlit as s
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()

s.title("Langchain Chatbot with History")

# add sidebar to control conversation history
with s.sidebar:
    s.header("Settings")
    count = s.slider("Message Count", min_value = 1, max_value = 10, value = 5, step = 1)


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

messages = s.session_state.conversation[-count*2:]
for msg in messages:
    with s.chat_message(msg["role"]):
        s.markdown(msg["content"])