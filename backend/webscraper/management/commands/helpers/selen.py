import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

import removeDuplicates


   

def selenScrape(url):
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run browser in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration (needed in headless mode)
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    time.sleep(5)  # Adjust the sleep time as needed

    # Get the page source after dynamic content has loaded
    page_source = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page_source, 'html.parser')
    
    pressReleases = []
    divs = soup.find_all('div')  # Find all <div> elements
    
    for div in divs:
        try:
            linkElement = div.find('a', href=True)  # Find <a> elements with href attribute
            if linkElement:
                link = linkElement['href']
                headline = linkElement.get_text().strip()
                
                pressRelease = {
                    'headline': headline,
                    'link': link,
                    'date': ''
                }
                if len(headline.split()) >= 5:
                    pressReleases.append(pressRelease)
        except (AttributeError, KeyError):
            pass
    
    return pressReleases

# url = 'https://www.atomwise.com/in-the-news/'
# linkPrefix = ''
# pressReleases = selenScrape(url)

# uniquePressReleases = removeDuplicates.remove(pressReleases)

# for pressRelease in uniquePressReleases:
#     print("Title:", pressRelease['headline'])
#     print("Link:", pressRelease['link'])
#     print('\n')
