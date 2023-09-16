#################################################################
# Building a webscraper to scrape the news from a companies webiste.
# This main.py file focuses on the files that are separated by proper elements, while the justDivs.py 
# covers the cases when the website is using only div tags with custom css. Although this is not 100% accurate at
# grabbing the title and link, it is enough for the purpose of recognizing that something has changed.

#################################################################
# importing libraries
import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import os
import datetime


# Importing other python local files
from ..helpers import removeDuplicates, URLParser, justDivs, selentest, useOnlyAlinks, individual

##############################################################################
def scrapePressReleases(url, articleTag, strings):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pressReleases = []
    pattern = re.compile(r'\b(?:' + '|'.join(strings) + r')\b', flags=re.IGNORECASE)

    for i in articleTag:
        articles = soup.find_all(i)
        if articles:
            if '403 Forbidden' in articles[0]:
                return [{
                        'headline': '403 Status, Blocked, Not Available',
                        'link': url,
                        'date': ''
                    }]
        for article in articles:
            try:
                elements = article.find_all()
                
                for element in elements:
                    headline = ""
                    link = ""
                    date = ""
                    if element.name == "a" and "href" in element.attrs:
                        link = element["href"]
                        if element.get_text():
                            headline = element.get_text().strip()
                    
                    
                    if headline and link and pattern.search(link):
                        
                        commonParent = element.find_parent()
                       
                        
                        extracted_date = None
                        
                        # Updated date patterns
                        date_patterns = [
                                    re.compile(r'(\d{2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4})', re.IGNORECASE),  # 05 Jun 2023
                                    re.compile(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2},\s\d{4}', re.IGNORECASE),  # Aug 08, 2023
                                    re.compile(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{2},\s\d{4}', re.IGNORECASE),  # August 08, 2023
                                    re.compile(r'(\d{2}/\d{2}/\d{4})')  # mm/dd/yyyy
                                ]
                        
                        for pattern in date_patterns:
                            match = pattern.search(headline)
                            if match:
                                if pattern == date_patterns[0]:
                                    extracted_date = datetime.datetime.strptime(match.group(0), '%d %b %Y').date()
                                elif pattern == date_patterns[1]:
                                    extracted_date = datetime.datetime.strptime(match.group(0), '%b %d, %Y').date()
                                elif pattern == date_patterns[2]:
                                    extracted_date = datetime.datetime.strptime(match.group(0), '%B %d, %Y').date()
                                elif pattern == date_patterns[3]:
                                    extracted_date = datetime.datetime.strptime(match.group(0), '%m/%d/%Y').date()
                                date = extracted_date.strftime('%B %d, %Y')  # Convert date to a standard format
                                break
                        if not extracted_date:
                            
                            date_elements = commonParent.find_all(class_=re.compile(r'\bdate\b', flags=re.IGNORECASE))
                            for i in range(1,4):
                                if not date_elements:
                                    pp = commonParent.find_parent()
                                    date_elements = pp.find_all(class_=re.compile(r'\bdate\b', flags=re.IGNORECASE))
                                    commonParent = pp
                            if date_elements:
                                # Extract text from all date elements and concatenate
                                date = date_elements[0].get_text().strip()


                        # if not date_element:
                        #     # If not found as a direct child, look for it among the descendants of the current element
                        #     date_element = element.find(class_=lambda x: x and "date" in x.lower())

                        # if date_element:
                        #     date = date_element.get_text()  # Replace with actual extraction logic

                        pressRelease = {
                            'headline': headline,
                            'link': link,
                            'date': date
                        }

                        # Adding a min word count to avoid things like "blog", "news", and other filler words that are links to a new page. Usually news articles are more than 5 letters.
                        if '\n' not in headline and len(headline.split()) >= 5:
                            pressReleases.append(pressRelease)
                    

            except (AttributeError, KeyError):
                pass
    # su("main")
    return pressReleases




# strings = ['news', 'headline', 'update', 'report', 'coverage', 'press', 'blog', 'announcement', 'media', 'feature', 'stories', 'analysis', 'commentary', 'breaking', 'trending', 'event', 'interview', 'opinion', 'editorial','pdf','gov','article','journal','team', 'conference']

# headers = ['li','ul', 'article', 'section', 'h2', 'h3', 'h4', 'h5', 'h6', 'h1']

# urls = []

# url = 'https://www.atomwise.com/in-the-news/'
# pressReleases = scrapePressReleases(url, headers, strings)

# alinks = useOnlyAlinks.aLinkScraper(url,strings)
# print(alinks)

# pressReleases = removeDuplicates.remove(pressReleases)
# alinks = removeDuplicates.remove(alinks)

# div = justDivs.divScraper(url)
# div = removeDuplicates.remove(div)
    
# checked = False
# if len(pressReleases) < len(div):
#     pressReleases = div
#     print("using div")
# # If both fail, try selenium.

# elif len(pressReleases) < 1 and len(div) < 1:
#     print("using alinks")
#     pressReleases = alinks
    
# elif len(pressReleases) == 1:
#     if "403 Status" in pressReleases[0]['headline']:
#         print("403 status forbidden", url)
#         pressReleases = selentest.selenScrape(url)
#         checked = True
# if len(pressReleases) ==  0 and not checked:
#     pressReleases = selentest.selenScrape(url)
# pressReleases = removeDuplicates.remove(pressReleases)

# prefix = URLParser.parseURL(url)

# count = 0
# for pressRelease in pressReleases:
#     # Checking if the link is an absolute link or relative to the website. if it is relative, 
#     # then we concatenate the rest of the url together with the home link.
#     # 
#     count += 1
#     if 'https://' not in pressRelease['link']:
#         pressRelease['link'] = prefix + pressRelease['link']
#     print("Title:", pressRelease['headline'])
#     print("Link:", pressRelease['link'])
#     print("Date:", pressRelease['date'])
#     print('\n')
    
# print(count)
    