# Using tools with AI agents : calculator, get weather and file reader

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import requests
import json
import streamlit as s

import os
from dotenv import load_dotenv
load_dotenv()

api_key_weather = os.getenv("API")

api_key_llm = "dummy key"

print("Weather api key : ", api_key_weather)

@tool
def calculator(expression):
    """
    This calculator function solves any arithmetic expression containing all constant values.
    It support basic arithmetic operators +, -, *, /, %, and parenthesis.
    
    :param expression: str input arithmetic expression
    :returns expression result as str
    """

    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Cannot solve expression"
    
@tool
def get_weather(city_name):
    """
    This get_weather() function gets the current weather of given city.
    If weather cannot be found, it returns "Error".
    This function doesn't return historic or general weather of the city.
    
    :param city_name: str inpt - name of the city
    : returns current weather in json format or "Error"
    """

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key_weather}&units=metric"
        response = requests.get(url)
        weather = response.json()
        return json.dumps(weather)
    except:
        return "Error"
    
@tool
def read_file(filepath):
    """
    This read_file() method gets file path as input and open file in read format.
    reads the content of file and return the readed content as it is.
    Dont add any extra tags except file content in result content.
    If file not found as designeted path then it returns "Error"
    
    :param filepath: path of file in str form
    :returns content read from the file or "Error"
    """
    try:
        with open(filepath,'r') as file:
            text = file.read()
            return text
    except:
        return "Error: file path not found"

# create model
model = init_chat_model(
    model = "google/gemma-3n-e4b",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "None"
)

# create agents
agent = create_agent(
    model = model,
    tools= [calculator, get_weather, read_file],
    system_prompt = "You are a helpful assistant. Give correct answer."

)

s.title("Multi Modal AI agent")

# check in session state file is uploaded or not

if "conversation" not in s.session_state:
    s.session_state.conversation = []


user_input = s.chat_input("Ask something: ")
if user_input:
    s.write("You: ", user_input)
    result = agent.invoke(
    {
        "messages": [
        {"role": "user", "content": user_input}
    ]
    }
    )

    llm_output = result["messages"][-1]
    s.write("AI : ", llm_output.content)



    
