from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

import os
from dotenv import load_dotenv
load_dotenv()


api_key_groq = os.getenv("GROQ_API_KEY")

#cteate model

llm = init_chat_model(
    model = "openai/gpt-oss-120b",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = api_key_groq
)


# conversation context
conversation = []

# create agent
agent = create_agent(
    model = llm,
    tools =[],
    system_prompt = "You are a helpful assistant. Answer in short"
)

while True:
    # take user input
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # append user message in conversation
    conversation.append({"role": "user", "content": user_input})

    # incoke the agent
    result = agent.invoke({"messages":conversation})

    # print the result's last message
    ai_msg = result["messages"][-1]
    print("AI: ",ai_msg.content)

    # use conversation history returned by agent
    # because agents internally maintain previous conversation, except appending the ai_ans we 
    # pass the result of agent as conversation history
    conversation = result["messages"] 