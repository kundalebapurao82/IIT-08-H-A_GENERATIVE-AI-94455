import streamlit as s
import pandasql as ps
import pandas as pd
if 'messsages' not in s.session_state:
    s.session_state.messages = []

s.title("CSV Dataframe explorer")

data_file = s.file_uploader("Upload a CSV file...",type=["csv"])

df = None

if data_file:
    df = pd.read_csv(data_file)
    s.subheader("data:")
    s.dataframe(df)


query = s.chat_input("Enter your SQL query treat table name as 'data'...")
if query:
    s.session_state.messages.append(query)
    try:
        response = ps.sqldf(query, {"data":df})
        s.session_state.messages.append(response)
    except Exception as e:
        s.session_state.messages.append("Error; please enetr correct query...")

    msglist = s.session_state.messages

    for idx, msg in enumerate(msglist):
        if idx%2 == 0:
            s.subheader("Query: ")
            s.write(msg)
        else:
            s.write("Query output: ")
            s.write(msg)