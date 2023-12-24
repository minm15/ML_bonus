from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import json

def signIn():
    teamname_input = driver.find_element(By.ID, 'teamname')
    passwd_input = driver.find_element(By.ID,'passwd')

    teamname_input.send_keys('lalala')
    passwd_input.send_keys('a3bfd7') 

    passwd_input.send_keys(Keys.RETURN)

    driver.implicitly_wait(5)


    print("Title: ", driver.title)
    print("URL: ", driver.current_url)
    
def get_links():
    links = driver.find_elements(By.XPATH, '//ul/li/a')
    #links = list(links)
    link = links[2]
    href = link.get_attribute('href')
    text = link.text
    print(f"text: {text}, href: {href}")
    return href

def set_chat_config():
    with open('config.json', 'r') as file:
        config_content = file.read()

    textarea = driver.find_element(By.ID, 'llm_config')
    textarea.send_keys(config_content)
    submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
    submit_button.click()
    driver.implicitly_wait(5)
    
    print("Title: ", driver.title)
    print("URL: ", driver.current_url)
    
def chat():
    cnt = 0
    with open('prompt.txt', 'r') as file:
        prompt_content = file.readlines()
    
    for prompt in prompt_content:
        chat_type, prompt = prompt.split('@')
        textarea = driver.find_element(By.ID, 'userinput')
        target_subject = "Should marijuana be legalized in Taiwan?"
        print(chat_type)
        if chat_type == 'subject':
            prompt = prompt.format(subject=target_subject)
        elif chat_type == 'refineA':
            message_elements = driver.find_elements(By.CLASS_NAME, 'agentBmessage')
            message_element = message_elements[-1]
            message_text = message_element.text
            prompt = prompt.format(topicB=message_text)
        elif chat_type == 'refineB':
            message_elements = driver.find_elements(By.CLASS_NAME, 'agentAmessage')
            refineA_element = message_elements[-1]
            refineA_text = refineA_element.text
            topicA_elements = message_elements[-2]
            topicA_text = topicA_elements.text
            prompt = prompt.format(refineA=refineA_text, topicA=topicA_text)
        elif chat_type == 'debateA1':
            message_elements = driver.find_elements(By.CLASS_NAME, 'agentBmessage')
            message_element = message_elements[-1]
            message_text = message_element.text
            prompt = prompt.format(refineB=message_text, subject=target_subject)
        elif chat_type == 'debateB1':
            message_elements = driver.find_elements(By.CLASS_NAME, 'agentAmessage')
            message_element = message_elements[-1]
            message_text = message_element.text
            prompt = prompt.format(subject=target_subject, argumentA=message_text)
        elif chat_type == 'debateA2':
            message_elements = driver.find_elements(By.CLASS_NAME, 'agentBmessage')
            message_element = message_elements[-1]
            message_text = message_element.text
            prompt = prompt.format(subject=target_subject, argumentB=message_text)
        elif chat_type == 'debateB2':
            message_elements = driver.find_elements(By.CLASS_NAME, 'agentAmessage')
            message_element = message_elements[-1]
            message_text = message_element.text
            prompt = prompt.format(subject=target_subject, argumentA=message_text)
        
        textarea.send_keys(prompt)
        submit_button = driver.find_element(By.ID, 'sendbtn')
        submit_button.click()
        
        # wait until the input is avaliable
        wait = WebDriverWait(driver, 200)
        wait.until(EC.element_to_be_clickable((By.ID, 'userinput')))
        wait.until(EC.element_to_be_clickable((By.ID, 'sendbtn')))
        
        # switch between A and B
        cnt+=1
        agent = 'Agent-A' if cnt%2==0 else 'Agent-B'
        select_element = driver.find_element(By.ID, 'action')
        select = Select(select_element)
        select.select_by_visible_text(agent)
    
    # Export
    select_element = driver.find_element(By.ID, 'action')
    select = Select(select_element)
    select.select_by_visible_text('Export')
    textarea = driver.find_element(By.ID, 'userinput')
    textarea.send_keys('export')
    submit_button = driver.find_element(By.ID, 'sendbtn')
    submit_button.click()
    
    wait = WebDriverWait(driver, 60)
    wait.until(EC.invisibility_of_element_located((By.ID, 'userinput')))

if __name__ == "__main__":
    driver = webdriver.Chrome() 

    url = 'http://140.112.90.203:7832'
    driver.get(url)
    
    signIn()
    chat_link = get_links()
    driver.get(chat_link)
    set_chat_config()
    
    # - - - ready to chat - - - #
    chat()

    driver.quit()
