import streamlit as s
import pandas as pd
from datetime import datetime
import os

def load_users():
    if not os.path.exists("users.csv"):
        df = pd.DataFrame(columns = ["username","password"])
        df.to_csv("Users.csv", index=False)
    return pd.read_csv("Users.csv")

def save_user(username, password):
    df = load_users()
    df.loc[len(df)] = [username, password]
    df.to_csv("users.csv", index = False)

def save_upload_history(username, filename):
    if not os.path.exists("userfiles.csv"):
        df = pd.DataFrame(columns = ["username", "filename","datetime"])
    else:
        df = pd.read_csv("userfiles.csv")
    
    df.loc[len(df)] = [username, filename, datetime.now()]
    df.to_csv("userfiles.csv", index = False)


def home_page():
    s.title("Home")
    s.write("Welcome to CSV Explorer App")

def login_page():
    s.header("Login page: ")
    with s.form("Login form"):
        s.markdown("Enter login credintials:")
        user_name = s.text_input("Username:")
        password = s.text_input("Password:", type = "password")

        submit_button = s.form_submit_button("Login")
        if submit_button:
            df = load_users()
            if ((df["username"] == user_name)&(df["password"] == password)).any() :
                s.success("Login successful!")
                s.session_state.page = "csv_explorer"
                s.session_state.authenticated = True
                s.session_state.user = user_name
            else:
                s.error("Invalid username or password")

def registration_page():
    s.title("Registration page")
    with s.form("Register form"):
        s.markdown("Enter details to register:")
        first_name = s.text_input("First name:")
        last_name = s.text_input("Last name: ")
        username = s.text_input("Usrname: ")
        password1 = s.text_input("Password: ", type = "password")
        password2 = s.text_input("Re-enter password: ", type = "password")
        reg_button = s.form_submit_button("Register")
        
        if reg_button:
            if password1 == password2:
                save_user(username, password1)
                s.success("Registration successfully done..")
                s.session_state.page = "login"
                s.rerun()
            else:
                s.toast("Incorrect password match")

def explore_csv_page():
    s.header("Explore CSV")

    file = s.file_uploader("Upload CSV file", type = ['csv'])
    if file:
        df = pd.read_csv(file)
        s.dataframe(df)
        save_upload_history(s.session_state.user, file.name)


def history_page():
    s.header("Upload history")
    if os.path.exists("userfiles.csv"):
        df = pd.read_csv("userfiles.csv")
        s.dataframe(df[df["username"] == s.session_state.user])


if 'page' not in s.session_state:
    s.session_state.page = 'main'
if "authenticated" not in s.session_state:
    s.session_state.authenticated = False

if "user" not in s.session_state:
    s.session_state.user = None


with s.sidebar:
    s.header("⊞ Menu: ")

    if not s.session_state.authenticated:

        if s.button("Login page", width = "stretch"):
            s.session_state.page = "Login"
        if s.button("Registration page", width = "stretch"):
            s.session_state.page = 'registration'
        if s.button("Home page", width = "stretch"):
            s.session_state.page = 'main'
    else:
        if s.button("Explore csv", width = 'stretch'):
            s.session_state.page = 'csv_explorer'
        if s.button("History", width = 'stretch'):
            s.session_state.page = 'history'
        if s.button("Logout"):
            s.session_state.authenticated = False
            s.session_state.user = None
            s.session_state.page = "main"
            s.rerun()

if s.session_state.page == "Login":
    login_page()

elif s.session_state.page == "registration":
    registration_page()

elif s.session_state.page == 'main':
    home_page()
elif s.session_state.page == 'csv_explorer':
    explore_csv_page()

elif s.session_state.page == 'history':
    history_page()
    

