#v import necessary packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# start selenium browser session

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options = chrome_options)


driver = webdriver.Chrome()

# initiating driver
driver.get("https://duckduckgo.com/")

# define wait strategy
# Wait for search box
driver.implicitly_wait(10)
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "searchbox_input"))
)

search_box.send_keys("Who is current President of America?")
search_box.send_keys(Keys.RETURN)

# Wait for the Search Assistant
answer_div = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div[data-testid='duckassist-answer-content']")
    )
)

# accessing p tag inside div tag
answer_para = answer_div.find_element(By.TAG_NAME, "p")

print("Answer:")
print(answer_para.text)

driver.quit()
