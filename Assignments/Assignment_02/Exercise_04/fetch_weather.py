import os
from dotenv import load_dotenv
import requests


load_dotenv()

API = os.getenv("API")

def f_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric"

    response = requests.get(url)

    # print("Status code: ",response.status_code)

    data = response.json()

    if response.status_code != 200:
        print("Error:", data.get("message", "Unable to fetch data"))
        return



    report = (
        "==============weather report=============\n"
        f"City : {data['name']}\n"
        f"Temperature: {data['main']['temp']}\n"
        f"Humidity : {data['main']['humidity']}\n"
        f"Pressure: {data['main']['pressure']}\n"
        f"Weather : {data['weather'][0]['main']} ({data['weather'][0]['description']})\n"
        f"Wind speed: {data['wind']['speed']}"
    )

    print(report)
