from selenium import webdriver
import logging
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import os
import shutil
import pandas as pd
import time
import requests
import urllib.parse
import re
# from bs4 import BeautifulSoup
from itertools import product

options = webdriver.ChromeOptions() 
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--no-sandbox")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
options.add_argument("--window-size=1920x1080")



driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)


def appendProduct(file_path2, data):
    temp_file = 'temp_file.csv'
    if os.path.isfile(file_path2):
        df = pd.read_csv(file_path2, encoding='utf-8')
    else:
        df = pd.DataFrame()

    df_new_row = pd.DataFrame([data])
    df = pd.concat([df, df_new_row], ignore_index=True)

    try:
        df.to_csv(temp_file, index=False, encoding='utf-8')
    except Exception as e:
        print(f"An error occurred while saving the temporary file: {str(e)}")
        return False

    try:
        os.replace(temp_file, file_path2)
    except Exception as e:
        print(f"An error occurred while replacing the original file: {str(e)}")
        return False
    
    return True





# driver.get("https://www.sydney.edu.au/research/our-researchers/find-a-researcher.html?HDR=true")
# time.sleep(5)

# profiles = []
# page_count = 1

# try:
#     for _ in range(651):  
#         profiles_xp = driver.find_elements(By.XPATH, "//div[@class='grid']/div/a")
#         for profile in profiles_xp:
#             link = profile.get_attribute('href')
#             if link is not None:
#                 profiles.append(link)
#         try:
#             cookie_banner_close = WebDriverWait(driver, 2).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "b-cookie-banner__button-close"))
#             )
#             cookie_banner_close.click()
#         except:
#             pass
#         print(f"Page {page_count} done")
#         print(len(profiles))

#         next_page = driver.find_element(By.XPATH, "//a[@class='pagination__item pagination__item--highlight pagination__item--next']")
#         next_page.click()
#         time.sleep(4)
#         page_count += 1

# except NoSuchElementException:
    
#     pass

# # print(profiles)

# with open('links.txt', 'w') as f:
#     for link in profiles:
#         f.write(link + '\n')



with open('links_hamza.txt', 'r') as f:
    profiles = f.readlines()
    
    

for profile_link_idx in range(len(profiles)):
    driver.get(profiles[profile_link_idx].strip())
    if profile_link_idx == 0:
        try:
            cookie_banner_close = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "b-cookie-banner__button-close")))
            cookie_banner_close.click()
        except:
            pass
    time.sleep(3)
    
    try:
        name = driver.find_element(By.XPATH,"//h1[@class='pageTitle ']/div/strong").text
    except:
        try:
            name = driver.find_element(By.XPATH,"//h1[@class='pageTitle ']").text
        except:
            continue

    try:
        faculty = driver.find_element(By.CSS_SELECTOR,"div.b-contact-information__strapline>em").get_attribute('innerHTML')
        try:
            faculty = faculty.split('<br>')[1]
        except:
            faculty = faculty
    except:
        faculty = ''

    try:
        phone = driver.find_element(By.XPATH,"//div[.='                             Phone                         ']/following-sibling::div/div").text
    except:
        phone = ''

    try:
        email = driver.find_element(By.XPATH,"//div[.='                             Email                         ']/following-sibling::div/a").text
    except:
        try:
            email= driver.find_element(By.XPATH,"//div[.='Email']/following-sibling::ul//li/a").text
        except:
            email = ''
    try:
        address = driver.find_element(By.XPATH,"//div[.='                             Address                         ']/following-sibling::div/a").text
    except:
        try:
            address=driver.find_element(By.XPATH,"(//div[normalize-space()='Address'])[1]/following-sibling::div[1]").text
        except:
            address = ''

    try:
        website = driver.find_element(By.XPATH,"//div[.='                             Websites                         ']/following-sibling::div/div/a").get_attribute('href')
    except:
        website = ''

    try:
        details = driver.find_element(By.XPATH,"//div[.='                             Details                         ']/following-sibling::div/div/div").text
    except:
        details =  ' '

    try:
        bio = driver.find_element(By.XPATH,"//div[@id='b-js-profile-biography']/p[1]").text
    except:
        bio = ''

    data = {
        "Name": name,
        "Profile Link": profiles[profile_link_idx],
        "Faculty": faculty,
        "Details": details,
        "Bio": bio,
        "Location": address,
        "Phone": phone,
        "Email": email,
        "Wesbite": website        
    }
    print(data)
    appendProduct('sydney_new.csv',data)