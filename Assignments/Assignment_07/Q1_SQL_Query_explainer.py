from langchain.chat_models import init_chat_model
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as s
import pandasql as ps

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = init_chat_model(
     model = "llama-3.3-70b-versatile",
     model_provider = "openai",
     base_url = "https://api.groq.com/openai/v1",
     api_key = api_key
)



s.title("CSV Explainer Chatbot")

# check in session state file is uploaded or not
if "uploaded_file" not in s.session_state:
    s.session_state.uploaded_file = None

if "df" not in s.session_state:
    s.session_state.df = None

if "conversation" not in s.session_state:
    s.session_state.conversation = []

# sidebar for file upload
with s.sidebar:
    s.header("File Upload")
    uploaded_file = s.file_uploader("Upload your CSV file", type=["csv"])
    s.session_state.uploaded_file = uploaded_file


if s.session_state.uploaded_file is None:
    s.info("Please upload a CSV file to proceed.")
else:
    csv_file_Path = s.session_state.uploaded_file
    df = pd.read_csv(csv_file_Path)
    s.session_state.df = df
    # print("CSV Schema:", df.dtypes)
    s.subheader("CSV Data")
    s.dataframe(df)
    s.subheader("CSV Schema")
    schema_df = df.dtypes.reset_index()
    schema_df.columns = ["Column Name", "Data Type"]
    s.dataframe(schema_df)

    # User Input for questions
    user_input = s.chat_input("Ask questions about your CSV data...")
    if user_input:
        s.write("User:", user_input)
        llm_input = f"""
                Table name : data
                Table schema = {schema_df}
                Question = {user_input}
                Instruction:
                        You are SQLite expert developer with extensive knowledge of SQL queries and 10 years of experience.
                        Write SQL query for above question.
                        Generate SQL query only without any explanation in plain text format and othing else.
                        if you cannot generate SQL query for the question, then reply with 'Error: please ask right question.
                """
        
        
        result = llm.invoke(llm_input)
        llm_output = result.content.strip()
        # s.session_state.conversation.append({"role": "assistant", "content": llm_output})

        query = llm_output
        s.write("Generated SQL Query:", query)

        if query.startswith("Error"):
            s.info("Error: please ask right question.")

        else:
            try:
                response = ps.sqldf(query, {"data": s.session_state.df})

                if response.empty:
                    s.info("Query executed successfully but returned no results.")
                else:
                    s.dataframe(response)
            except Exception as e:
                s.error("Error: Please ask right question.")

        
        # explain the query output in simple english using LLM
        explanation_input = f"""
                Table name : data
                Table schema = {schema_df}
                SQL Query = {query}
                Query Output = {response}
                Instruction:
                        You are data analyst expert with extensive knowledge of SQL queries and 10 years of experience.
                        you can explain SQL query output in simple english.
                        explain the query output in simple english so that a non-technical person can understand easily.
                        Generate explanation so that user can understand easily.
                        But do not explain SQL query itself and its syntax.
                        Provide only the explanation.
                        if query output is empty, then reply with 'No data found for the question.'
                        if possible explain why data not founded for the question.
                """
        explanation_result = llm.invoke(explanation_input)
        explanation_output = explanation_result.content.strip()
        s.subheader("Explanation of Query Output")
        s.write(explanation_output)



    