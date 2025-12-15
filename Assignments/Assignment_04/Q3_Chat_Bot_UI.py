import streamlit as s
import time

if 'messages' not in s.session_state:
    s.session_state.messages = []

s.title("Chatbot...")

def stream_text(text):
    for word in text.split():
        yield word+ " "
        time.sleep(0.1)

for chat in s.session_state.messages:
    with s.chat_message(chat["role"]):
        s.write(chat["content"])


msg = s.chat_input("Say something....")



if msg:

    with s.chat_message("User"):
        s.write(msg)

    s.session_state.messages.append({
        "role" : "user",
        "content": msg
    })

    response = f"{msg}"

    with s.chat_message("assistant"):
        s.write_stream(stream_text(response))

    s.session_state.messages.append({
        "role" : "assistant",
        "content": response
    })