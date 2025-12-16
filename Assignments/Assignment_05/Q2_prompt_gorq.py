# 2. ⁠Connect to Groq and Gemini AI using REST api. 
# Send same prompt and compare results. Also compare the speed.

import os
import requests
import json
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"

}

user_prompt = input("Ask anything:")

req_data = {
    "model": "llama-3.3-70b-versatile",
    "messages":[ 
        {"role": "user", "content": user_prompt}
    ],
}
init_time = time.perf_counter()
resopnse = requests.post(url, data = json.dumps(req_data), headers = headers)

end_time = time.perf_counter()
print("status: ", resopnse.status_code)

print("Time taken (in seconds): ", end_time - init_time)
output = resopnse.json()

print(output['choices'][0]['message']['content'])