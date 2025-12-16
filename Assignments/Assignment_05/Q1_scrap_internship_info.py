# import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd

# start selenium browser session
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options = chrome_options)

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
    print(info)

# insert retrieved data into csv file using pandas
df = pd.DataFrame(data_list)
df.to_csv("internship_batch_schedules.csv", index=False)


# close the session
driver.quit()