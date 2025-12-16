from google import genai
from dotenv import load_dotenv
import time
import os
from google.genai.errors import ServerError


load_dotenv()

api_key = os.getenv("Gemini_API_KEY_1")

# The client gets the API key from the environment variable `Gemini_API_KEY`.
client = genai.Client(api_key = api_key)

print("Type 'exit' to quit")

msg = input("Ask anything:")
init_time = time.perf_counter()
try:
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = msg
    )
    print(response.text)
except ServerError as e:
    print("Server busy. Retrying in 5 seconds...")
    time.sleep(5)
end_time = time.perf_counter()
print("Time taken (in seconds): ", end_time - init_time)
