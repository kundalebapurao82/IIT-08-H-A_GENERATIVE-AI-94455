from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

import os
from dotenv import load_dotenv
load_dotenv()

api_key_groq = os.getenv("GROQ_API_KEY")
print("API KEY :", api_key_groq)


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
        return "Error: cannot solve expression"


# create model

llm = init_chat_model(
    model = "google/gemma-3n-e4b",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "None"
)

# create agent
agent = create_agent(
    model = llm, 
    tools = [calculator],
    system_prompt = "You are a helpful assistant, give correct answer"
)

while True:
    # take user input
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    # invoke agent with user input
    result = agent.invoke({
        "messages" : [
            {"role" : "user", "content": user_input}
        ]
    })

    llm_output = result["messages"][-1]
    print("AI: ", llm_output)
    print("\n\n", result["messages"])