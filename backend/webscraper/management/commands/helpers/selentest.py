import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os
from ..helpers import datesSearch

def selenScrape(url, keywords = []):
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    chrome_driver_path = './chrome/chromedriver'
    os.environ['PATH'] = f"{os.environ['PATH']}:{chrome_driver_path}"

    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Edge(options=options)

    driver.get(url)

    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))


    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    pattern = re.compile(r'\b(?:' + '|'.join(keywords) + r')\b', flags=re.IGNORECASE)

    pressReleases = []
    link_elements = soup.find_all('a', href=True)  # Find all <a> elements with href attribute

    for link_element in link_elements:
        link = link_element['href']
        headline = link_element.get_text().strip()
        date = ""
        if pattern.search(link) and len(headline.split()) >= 5:
            commonParent = link_element.find_parent()

            date_elements = commonParent.find_all(class_=re.compile(r'\bdate\b', flags=re.IGNORECASE))
            for i in range(1,4):
                if not date_elements or date:
                    pp = commonParent.find_parent()
                    date_elements = pp.find_all(class_=re.compile(r'\bdate\b', flags=re.IGNORECASE))
                    commonParent = pp
                    text = pp.get_text().strip()
                    date = datesSearch.inText(text)
            if date_elements and not date:
                # Extract text from all date elements and concatenate
                date = ' '.join([date_element.get_text().strip() for date_element in date_elements])

            pressRelease = {
                'headline': headline,
                'link': link,
                'date': date
            }
            if len(headline.split()) >= 5:
                pressReleases.append(pressRelease)

    return pressReleases

# url = 'https://www.atomwise.com/in-the-news/'
# pressReleases = selenScrape(url)

# for pressRelease in pressReleases:
#     print("Title:", pressRelease['headline'])
#     print("Link:", pressRelease['link'])
#     print('\n')
