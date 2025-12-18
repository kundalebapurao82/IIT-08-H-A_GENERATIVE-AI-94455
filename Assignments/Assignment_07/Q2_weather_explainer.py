import streamlit as s
import requests 
import os
from dotenv import load_dotenv
import pandasql as ps
from langchain.chat_models import init_chat_model
load_dotenv()

api_key_groq = os.getenv("GROQ_API_KEY")

if 'view' not in s.session_state:
    s.session_state['view'] = 'login'


def login_page():
    with s.form("Login form"):
        s.markdown("Enter login credintials:")
        user_name = s.text_input("Username:")
        password = s.text_input("Password:", type = "password")

        submit_button = s.form_submit_button("Login")
    if submit_button:
        if user_name == password:
            s.session_state['user_name'] = user_name
            s.session_state['view'] = 'main'
            s.rerun()
        else:
            s.error("Invalid username or password")

def main_page():
    s.title("Welcome, to weather report:")

    load_dotenv()

    API = os.getenv("API")

    s.subheader("Enter city to get weather report...")
    city = s.text_input("City:")

    if s.button("Get Weather"):
        if city.strip() == "":
            s.warning("Please enter a city name")
            return

        

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric"

        response = requests.get(url)

        data = response.json()

        if response.status_code != 200:
            s.write("Error:", data.get("message", "Unable to fetch data"))
            s.rerun()

        # s.write(f"\nCity : {data['name']}\n")
        # s.write(f"Temperature: {data['main']['temp']}\n")
        # s.write(f"Humidity : {data['main']['humidity']}\n")
        # s.write(f"Pressure: {data['main']['pressure']}\n")
        # s.write(f"Weather : {data['weather'][0]['main']} ({data['weather'][0]['description']})\n")
        # s.write(f"Wind speed: {data['wind']['speed']}")

        weather_report_input = f"""
                city : f"{city}"
                fetched weather data : {data}
                ststus code = {response.status_code}
                Instructions: Generate a detailed and easy-to-understand weather report based on the fetched weather data for the specified city. 
                The report should include information about temperature, humidity, pressure, weather conditions, and wind speed, rain information if available. 
                don't show unnecessary weather data except above mentioned data , present the information in a user-friendly format..
                and lastly summarize the weather conditions briefly.
            
                if status code is not 200 then show error message only. else don't explain anything about status code, ont a single word.
        """

        llm = init_chat_model(
                model = "llama-3.3-70b-versatile",
                model_provider = "openai",
                base_url = "https://api.groq.com/openai/v1",
                api_key = api_key_groq
        )

        result = llm.invoke(weather_report_input)
        s.markdown("### Weather Report:")
        s.markdown(result.content)

    if s.button("Logout"):
        s.session_state['view'] = 'login'
        s.rerun()

if s.session_state['view'] == 'login':
    login_page()
elif s.session_state['view'] == 'main':
    main_page()
