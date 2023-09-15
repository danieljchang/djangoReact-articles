

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
from django.conf import settings


# Importing other python local files
from ..helpers import removeDuplicates, URLParser, justDivs, selentest, useOnlyAlinks, individual

# ##############################################################################
# def scrapePressReleases(url, articleTag, strings):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     pressReleases = []
#     pattern = re.compile(r'\b(?:' + '|'.join(strings) + r')\b', flags=re.IGNORECASE)

#     for i in articleTag:
#         articles = soup.find_all(i)
#         if articles:
#             if '403 Forbidden' in articles[0]:
#                 return [{
#                         'headline': '403 Status, Blocked, Not Available',
#                         'link': url
#                     }]
#         for article in articles:
#             try:
#                 elements = article.find_all()
#                 for element in elements:
#                     headline = ""
#                     link = ""
#                     if element.name == "a" and "href" in element.attrs:
#                         link = element["href"]
#                         if element.get_text():
#                             headline = element.get_text().strip()
                    
                    
#                     if headline and link and pattern.search(link):
                       
#                         pressRelease = {
#                             'headline': headline,
#                             'link': link
#                         }
#                         # Adding a min word count to avoid things like "blog", "news", and other filler words that are links to a new page. Usually news articles are more than 5 letters.
#                         if '\n' not in headline and len(headline.split()) > 6:
#                             pressReleases.append(pressRelease)
                    

#             except (AttributeError, KeyError):
#                 pass

#     return pressReleases
file = 'urls.csv'
filePath = os.path.join(settings.BASE_DIR, "webscraper", "management", "commands", "helpers", file)
# C:\Users\Daniel Chang\Documents\SearchFul\djangoReact-articles\backend\webscraper\management\commands\helpers\urls.csv

def scrapeWeb():
    print('scraping')
    print(settings.BASE_DIR)
    print(filePath)
    strings = ['news', 'headline', 'update', 'report', 'coverage', 'press', 'blog', 'announcement', 'media', 'feature', 'stories', 'analysis', 'commentary', 'breaking', 'trending', 'event', 'interview', 'opinion', 'editorial','pdf','gov','article','journal','team', 'conference']
    headers = ['li','ul', 'article', 'section', 'h2', 'h3', 'h4', 'h5', 'h6', 'h1']
    urls = []
    all = []
    count = 0
    pressReleases = []
    if os.path.isfile(filePath):
        with open(filePath, 'r') as csvFile:
            csvReader = csv.DictReader(csvFile)
            for row in csvReader:
                company = row['company']
                url = row['url']
                dic = {'company': company, 'url': url}
                urls.append(dic)
    else:
        print("nothing sadge")
    for url in urls:
        
        alinks = useOnlyAlinks.aLinkScraper(url['url'],strings)
        div = justDivs.divScraper(url['url'])
        pressReleases = individual.scrapePressReleases(url['url'], headers, strings)
        
        pressReleases = removeDuplicates.remove(pressReleases)
        div = removeDuplicates.remove(div)
        alinks = removeDuplicates.remove(alinks)

        checked = False
        if len(pressReleases) < len(div):
            pressReleases = div
        # If both fail, try selenium.
        
        elif len(pressReleases) < 1 and len(div) < 1:
            pressReleases = alinks
        elif len(pressReleases) == 1:
            if "403 Status" in pressReleases[0]['headline']:
                print("403 status forbidden", url['url'])
                pressReleases = selentest.selenScrape(url['url'])
                checked = True
        if len(pressReleases) ==  0 and not checked:
            pressReleases = selentest.selenScrape(url['url'])
            
        pressReleases = removeDuplicates.remove(pressReleases)

        prefix = URLParser.parseURL(url['url'])
        if len(pressReleases) == 0:
            pressRelease = {'headline': 'None', 'link': prefix, 'date': ''}
            pressReleases.append(pressRelease)
        for data in pressReleases:
            if 'https://' not in data['link']:
                data['link'] = prefix + data['link']
            data['company'] = url['company']
            data['headline'] = data['headline'].replace('\n', ' ')
            data['homeurl'] = prefix
            count += 1
        all.extend(pressReleases)
        # for pressRelease in pressReleases:
        #     # Checking if the link is an absolute link or relative to the website. if it is relative, 
        #     # then we concatenate the rest of the url together with the home link.
        #     # 
        #     if 'https://' not in pressRelease['link']:
        #         pressRelease['link'] = prefix + pressRelease['link']
        #     print("Title:", pressRelease['headline'])
        #     print("Link:", pressRelease['link'])
        #     print('\n')
        
    print("number of headlines", count)
    return all                    
                
            