from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
mm = 0
data = pd.read_excel('矿点整理.xlsx').values
res = []
q = data[0][0] + ',' + data[0][1]
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get(f'https://www.google.com.hk/search?q={q}')
over_time_flag = 0
clear_time_flag = 0
try:
    while mm < len(data):
        try:
            if clear_time_flag == 100:
                clear_time_flag = 0
                driver.quit()
                q = data[0][0] + ',' + data[0][1]
                driver = webdriver.Chrome(executable_path='chromedriver.exe')
                driver.get(f'https://www.google.com.hk/search?q={q}')
            time.sleep(5)
            print(mm)
            row = data[mm]
            mm += 1
            q = row[0] + ',' + row[1]
            driver.find_element(by=By.XPATH, value='//*[@id="APjFqb"]').clear()
            driver.find_element(by=By.XPATH, value='//*[@id="APjFqb"]').send_keys(q)
            action = ActionChains(driver)
            action.key_down(Keys.RETURN).key_up(Keys.RETURN).perform()
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(1)
            for i in driver.find_elements(by=By.CLASS_NAME, value=f'yuRUbf'):
                title = i.find_element(by=By.TAG_NAME, value='h3').text
                url = i.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
                res.append([q, title, url])
                print(res[-1])
            over_time_flag = 0
            clear_time_flag += 1
        except:
            over_time_flag += 1
            if over_time_flag == 10:
                break
            driver.quit()
            q = data[0][0] + ',' + data[0][1]
            driver = webdriver.Chrome(executable_path='chromedriver.exe')
            driver.get(f'https://www.google.com.hk/search?q={q}')
except:
    pass



with open('res.csv','w',newline='',encoding='utf8') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(res)