from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()


groq_api_key = os.getenv("GROQ_API_KEY")

gemini_api_key = os.getenv("Gemini_API_KEY")
# print("Groq API Key:", groq_api_key)

# Groq model invocation
# llm = ChatGroq(model = "llama-3.3-70b-versatile", api_key = groq_api_key)

# user_input = input("You: ")

# result = llm.invoke(user_input)

# print("AI: ",result.content)


# Google Generative AI model invocation

# llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", api_key = gemini_api_key)

# user_input = input("You: ")
# result = llm.invoke(user_input)
# print("AI: ",result.content)

# OpenAI local (offline) model invocation
# llm_url = "http://127.0.0.1:1234/v1"
# dummy_api = "dummy_api_key"

# llm = ChatOpenAI(
#     base_url = llm_url,
#     model = "google/gemma-3n-e4b",
#     api_key = dummy_api
# )

# user_input = input("You: ")
# result = llm.invoke(user_input)
# print("AI: ",result.content)


# using streaming responses
# Google Generative AI model invocation

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", api_key = gemini_api_key)

user_input = input("You: ")

result = llm.stream(user_input)
for chunk in result:
    print(chunk.content, end="")