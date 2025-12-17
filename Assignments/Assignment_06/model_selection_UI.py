import streamlit as s
import requests
import json
from dotenv import load_dotenv

import os

groq_api_key = os.getenv("GROQ_API_KEY")
lm_api_key = "Dummy API key"

load_dotenv()

if "model_ch" not in s.session_state:
    s.session_state.model_ch = "Groq (Cloud)"

if "chats" not in s.session_state:
    s.session_state.chats = {
        "Groq (Cloud)": [],
        "LM Studio (Local)": []

    }

with s.sidebar:
    s.title("Model selection")
    model_choice = s.selectbox(
        "Choose a model:",
        ("Groq (Cloud)", "LM Studio (Local)")
    )
    s.session_state.model_ch = model_choice

s.title("OpenAI Model testing")

current_model = s.session_state.model_ch
for chat in s.session_state.chats[current_model]:
    with s.chat_message(chat["role"]):
        s.markdown(chat["content"])

prompt = s.chat_input("Say something...")

def call_qroq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    req_data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
    }

    response = requests.post(url, data = json.dumps(req_data), headers=headers)
    return response.json()['choices'][0]['message']['content']

def call_lmstd(prompt):
    url = "http://127.0.0.1:1234/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {lm_api_key}",
        "Content-Type": "application/json"
    }

    req_data = {
        "model": "",
        "messages": [ 
            {"role": "user", "content": prompt}
        ],
    }

    response = requests.post(url, data = json.dumps(req_data), headers= headers)
    return response.json()['choices'][0]['message']['content'] 



if prompt:
    s.session_state.chats[current_model].append({"role": "user", "content": prompt})

    with s.chat_message("user"):
        s.markdown(prompt)


    with s.chat_message("assistant"):
        if s.session_state.model_ch == "Groq (Cloud)":
            response_content = call_qroq(prompt)
        else:
            response_content = call_lmstd(prompt)

        s.markdown(response_content)
    
    s.session_state.chats[current_model].append({"role": "assistant", "content": response_content})