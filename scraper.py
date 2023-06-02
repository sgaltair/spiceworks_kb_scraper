from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import json

# Modify these variables to suit your needs.
username = 'YOUR USERNAME'
password = 'YOUR PASSWORD'
swURL = 'http://URL:PORT/' # Use this format exactly, ending with a forward slash.
urlLogin = swURL + 'pro_users/login'
bottomRange = 0
topRange = 100

# XPATHs for the article parts
titleXPATH = '//*[@id="article_title"]'
introXPATH = '//*[@id="article_intro"]'
stepsXPATH = '//*[@id="xbb_content"]/div/ol'
conclusionXPATH = '//*[@id="article_conclusion"]'
referencesXPATH = '//*[@id="xbb_content"]/div/div[5]'
errorXPATH = '//*[@id="xbb_error_message"]'

# Adding options and then initializing the browser.
# Chromedriver.exe here is in the same directory as this script. 
# Chromedriver sourced here: https://chromedriver.chromium.org/downloads
options = webdriver.ChromeOptions()
options.add_argument('--headless=new') 
driver = webdriver.Chrome("chromedriver", options=options)

# Nav to the login page and enter user, pass, click button
driver.get(urlLogin)

driver.find_element('id', 'pro_user_email').send_keys(username)
driver.find_element('id', 'pro_user_password').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="login_form"]/div[7]/div/button').click()

# Wait for the dashboard to load
sleep(5)

for i in range(bottomRange, topRange):
    url = f'{swURL}knowledge_base#show?i={i}&local=true'
    textDict = {}
    driver.get(url)
    # Little time for the page to load
    sleep(5)
    
    if '404' not in driver.find_element(By.XPATH, errorXPATH).text:
        textDict['url'] = driver.current_url
        textDict['title'] = driver.find_element(By.XPATH, titleXPATH).text
        textDict['intro'] = driver.find_element(By.XPATH, introXPATH).text
        textDict['steps'] = driver.find_element(By.XPATH, stepsXPATH).text
        textDict['conclusion'] = driver.find_element(By.XPATH, conclusionXPATH).text
        textDict['references'] = driver.find_element(By.XPATH, referencesXPATH).text
        print(f"Article '{textDict['title']}' found at {textDict['url']}" )

        try:
            keepCharacters = (' ','.','_')
            filename = f"{textDict['title']}"
            safeFilename = "".join([c for c in filename if c.isalnum() or c in keepCharacters]).rstrip()
            with open(f"kbs\{safeFilename}.txt", 'w') as file:
                file.write(json.dumps(textDict, indent = 2))
        except:
            print(f'Problem writing {filename} with file name {safeFilename}. Aborting!')
            break
    else:
        print(f'No article found at {url}')