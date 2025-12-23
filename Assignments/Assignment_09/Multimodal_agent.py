from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as s
import pandasql as ps




# import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# start selenium browser session
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options = chrome_options)

# import scrap_intern_prog as ip
# import scrap_internship_info as ii


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = init_chat_model(
    model = "openai/gpt-oss-20b",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = api_key
)




# check in session state file is uploaded or not
if "uploaded_file" not in s.session_state:
    s.session_state.uploaded_file = None

if "df" not in s.session_state:
    s.session_state.df = None

if "conversation" not in s.session_state:
    s.session_state.conversation = []

if "view" not in s.session_state:
    s.session_state.view = "CSV_EXP"

# sidebar for file upload
with s.sidebar:

    CSV_QA_Button = s.button("CSV_QA", type = 'primary')
    WB_scrapping_Btn = s.button("Web Scrapping Agent", type = 'primary')

    if CSV_QA_Button:
        s.session_state.view = "CSV_EXP"
        s.rerun()


    if WB_scrapping_Btn:
        s.session_state.view = "WB_SCRAPPING"
        s.rerun()

@tool
def get_intern_prog():

    """
    This get_intern_prog() function fetch internship programs from sunbeam infotech website.
    and return the data in json format. by converting dataframe into json format.
    :returns internship programs data in json format
    """

    # load desired page in the browser
    driver.get("https://www.sunbeaminfo.in/internship")

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    # define driver wait strategy
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 5)
    # Scroll to the bottom (makes sure that dynamic contents load)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # wait for and click the "Available Internship Programs" toggle button
    plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
    plus_button.click()

    # interact with web to fetch internship info
    # fetch table class by class name

    table_div = driver.find_element(By.ID, 'collapseSix')
    table_body = table_div.find_element(By.TAG_NAME, 'tbody')
    table_rows = table_body.find_elements(By.TAG_NAME, 'tr')

    data_list2 = []

    for row in table_rows[1:]: 
        cols = row.find_elements(By.XPATH, './/td')

        info_new = {
            "Technology": cols[0].text.strip(),
                "Aim": cols[1].text.strip(),
                "Prerequisite": cols[2].text.strip(),
                "Learning": cols[3].text.strip(),
                "Location": cols[4].text.strip()
            }
        data_list2.append(info_new)
        # print(info_new)
    df2 = pd.DataFrame(data_list2)
    json_df2 = df2.to_json()
    return json_df2

@tool
def get_intern_batch_info():
    """
    This get_intern_batch_info() function fetch internship batch information from sunbeam infotech website.
    and return the data in json format. by converting dataframe into json format.
    :returns internship programs data in json format
    
    """
    # load desired page in the browser
    driver.get("https://www.sunbeaminfo.in/internship")

    # define driver wait strategy
    driver.implicitly_wait(10)

    # interact with web to fetch internship info
    # fetch table class by class name
    table_body = driver.find_element(By.CLASS_NAME, "table")
    table_rows = table_body.find_elements(By.TAG_NAME, 'tr')


    data_list = []


    for row in table_rows[1:]:  # skip header row
        cols = row.find_elements(By.TAG_NAME, 'td')
        info = {
            "sr": cols[0].text,
            "Batch": cols[1].text,
            "Batch duration": cols[2].text,
            "startdate": cols[3].text,
            "end_date": cols[4].text,
            "time": cols[5].text,
            "Fees": cols[6].text,
            "Brochure": cols[7].text
        }
        data_list.append(info)
        # print(info)

    # insert retrieved data into csv file using pandas
    df = pd.DataFrame(data_list)
    json_df1 = df.to_json()
    return json_df1


# Create agent
agent = create_agent(
    model = llm,
    tools= [get_intern_batch_info, get_intern_prog],
    system_prompt = "You are a helpful assistant. Give correct answer."

)

def csv_explorer():
    s.markdown("File Upload")
    uploaded_file = s.file_uploader("Upload your CSV file", type=["csv"])
    s.session_state.uploaded_file = uploaded_file

    if s.session_state.uploaded_file is None:
        s.info("Please upload a CSV file to proceed.")
    else:
        df = pd.read_csv(uploaded_file)
        s.session_state.df = df
        # showing datarame and CSVs schema
        s.subheader("CSV Data")
        s.dataframe(df)
        s.subheader("CSV Schema")
        schema_df = df.dtypes.reset_index()
        schema_df.columns = ["Column Name", "Data Type"]
        s.dataframe(schema_df)



    user_input = s.chat_input("Ask questions about your CSV data...")
    if user_input:
        s.session_state.conversation.append({"role":"user", "content": user_input})

        agent_input = f"""
                Table name : data
                Table schema = {schema_df}
                Question = {user_input}
                Instruction:
                        You are SQLite expert developer with extensive knowledge of SQL queries and 10 years of experience.
                        Write SQL query for above question.
                        Generate SQL query only without any explanation in plain text format without markdown formatting and nothing else.
                        Always use case-insensitive matching for text columns by applying LOWER() on both column name and value.
                        if you cannot generate SQL query for the question, then reply with 'Error: please ask right question.
                """
        
        
        agent_output = agent.invoke(
            {
                "messages": [
                    { "role": "user", "content": agent_input}
                ]
            }
        )
        result = agent_output["messages"][-1]
        query = result.content.strip()
        s.write("Query : ", query)
        # s.session_state.conversation.append({"role": "assistant", "content": llm_output})

        if query.startswith("Error"):
            s.info("Error: please ask right question.")
            response = "Error: please ask right question."

        else:
            try:
                response = ps.sqldf(query, {"data": s.session_state.df})

                if response.empty:
                    s.info("Query executed successfully but returned no results.")
                    # response = "response is empty."
                else:
                    s.dataframe(response)
            except Exception as e:
                s.error("Error: Please ask right question.")

        # explain the query output in simple english using LLM
        explanation_input = f"""
                Table name : data
                Table schema = {schema_df}
                user question = {user_input}
                SQL Query = {query}
                Query Output = {response}
                Instruction:
                        You are data analyst expert with extensive knowledge of SQL queries and 10 years of experience.
                        explain the query output in language, so that anyone can understand.
                        don't explain format of query output.
                        explain query output which gives answer to users question.
                        don't explain it as query output, explain it as answer to the users question
                """
        agent_output = agent.invoke(
            {
                "messages": [
                    { "role": "user", "content": explanation_input}
                ]
            }
        )
        explanation_result = agent_output["messages"][-1]
        explanation_output = explanation_result.content.strip()
        s.session_state.conversation.append({"role":"assistant", "content": explanation_output})
        # s.subheader("Explanation of Query Output")
        # s.write(explanation_output)

        for msg in s.session_state.conversation:
            with s.chat_message(msg["role"]):
                s.markdown(msg["content"])

def web_scrapping():
    s.title("Sunbeam programs explorer")

    # load_data_btn = s.button("Load Sunbeam Data", type = "primary")

    # if load_data_btn:
    #     df1 = get_intern_info()
    #     df2 = get_intern_prog()

    #     s.markdown("Sunbeam internship info: ")
    #     s.dataframe(df1)

    #     s.markdown("Sunbeam internship programs:")
    #     s.dataframe(df2)

    user_question = s.chat_input("Ask questions about Sunbeam: ")
    s.session_state.conversation.append({"role":"user", "content":user_question})

    if user_question:

        agent_input = f"""
                user question = {user_question}
                Instruction:
                use the intership program data and internship batch info of sunbeam infotech.
                and give answers to the users question in simple english.
                if you don't have answer, then say "please ask right question".
            """

        
        
        agent_output = agent.invoke(
            {
                # "messages": [
                #     { "role": "user", "content": user_question}
                # ]
                "messages": s.session_state.conversation
            }
        )

        result = agent_output["messages"][-1]
        output = result.content.strip()
        s.session_state.conversation.append({"role":"assistant", "content":output})
        # s.write(output)
        for chat in s.session_state.conversation:
            with s.chat_message(chat["role"]):
                s.markdown(chat["content"])





if s.session_state.view == 'CSV_EXP':  
    csv_explorer()

if s.session_state.view == 'WB_SCRAPPING':
    web_scrapping()
