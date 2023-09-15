import requests
from bs4 import BeautifulSoup
import re
import datetime
import removeDuplicates
import datesSearch


def findRelatedText(element):
    parent = element.find_parent()
    siblingTags = ['h2', 'h3', 'h4', 'h5', 'h6', 'p', 'section', 'article', 'div']

    if parent:
        for child in parent.find_all():
            if child.name in siblingTags and child != element:
                if child.get_text(strip=True) != '':
                    return child.get_text(strip=True)

    return ''


def aLinkScraper(url, keywords):
    response = requests.get(url)
    content = response.content
    # searching for anything with certain strings to identify them as news articles and not just random links.
    pattern = re.compile(r'\b(?:' + '|'.join(keywords) + r')\b', flags=re.IGNORECASE) 
    date_patterns = [
                    re.compile(r'(\d{2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4})', re.IGNORECASE),  # 05 Jun 2023
                    re.compile(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2},\s\d{4}', re.IGNORECASE),  # Aug 08, 2023
                    re.compile(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{2},\s\d{4}', re.IGNORECASE),  # August 08, 2023
                    re.compile(r'(\d{2}/\d{2}/\d{4})')  # mm/dd/yyyy
                ]
                

    soup = BeautifulSoup(content, 'html.parser')

    results = []
    for aTag in soup.find_all('a'):
        link = aTag.get('href')
        if link and '#' not in link:  # Reject links with '#'
            text = aTag.get_text(strip=True)
            
            if text.lower() == 'read more':
                text = findRelatedText(aTag)
                result = {'headline': text, 'link': link, 'date': ''}
            else:
                result = {'headline': text, 'link': link, 'date': ''}
            # Split on 5 words not 5 characters
            if pattern.search(link) and len(text.split()) >= 5:
                date = ''
                extracted_date = None
                
                # Updated date patterns
               
                for tempPattern in date_patterns:
                    match = tempPattern.search(text)
                    if match:
                        if tempPattern == date_patterns[0]:
                            extracted_date = datetime.datetime.strptime(match.group(0), '%d %b %Y').date()
                        elif tempPattern == date_patterns[1]:
                            extracted_date = datetime.datetime.strptime(match.group(0), '%b %d, %Y').date()
                        elif tempPattern == date_patterns[2]:
                            extracted_date = datetime.datetime.strptime(match.group(0), '%B %d, %Y').date()
                        elif tempPattern == date_patterns[3]:
                            extracted_date = datetime.datetime.strptime(match.group(0), '%m/%d/%Y').date()
                        date = extracted_date.strftime('%B %d, %Y')  # Convert date to a standard format
                        break
                
                date = datesSearch.getDates(aTag)
                
                result['date'] = date
                results.append(result)
    return results

# keywords = ['news', 'headline', 'update', 'report', 'coverage', 'press', 'blog', 'announcement', 'media', 'feature', 'stories', 'analysis', 'commentary', 'breaking', 'trending', 'event', 'interview', 'opinion', 'editorial', 'pdf', 'gov', 'article', 'journal', 'team', 'conference']

# url = 'https://www.gen1e.com/news'
# scrapedData = aLinkScraper(url, keywords)

# scrapedData = removeDuplicates.remove(scrapedData)
# count = 0
# for entry in scrapedData:
#     count += 1
#     print(entry['headline'])
#     print(entry['link'])
#     print()

# print(count)
