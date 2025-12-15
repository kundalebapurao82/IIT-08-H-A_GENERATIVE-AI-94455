import streamlit as s
import requests 
import os
from dotenv import load_dotenv

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

        s.write(f"\nCity : {data['name']}\n")
        s.write(f"Temperature: {data['main']['temp']}\n")
        s.write(f"Humidity : {data['main']['humidity']}\n")
        s.write(f"Pressure: {data['main']['pressure']}\n")
        s.write(f"Weather : {data['weather'][0]['main']} ({data['weather'][0]['description']})\n")
        s.write(f"Wind speed: {data['wind']['speed']}")



    if s.button("Logout"):
        s.session_state['view'] = 'login'
        s.rerun()

if s.session_state['view'] == 'login':
    login_page()
elif s.session_state['view'] == 'main':
    main_page()
