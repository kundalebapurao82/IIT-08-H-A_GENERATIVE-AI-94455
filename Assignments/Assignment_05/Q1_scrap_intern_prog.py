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

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# define driver wait strategy
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)
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
    print(info_new)
df2 = pd.DataFrame(data_list2)
df2.to_csv("internship_programs_info.csv", index=False)


# close the session
driver.quit()