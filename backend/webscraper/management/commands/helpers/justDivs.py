import requests
from bs4 import BeautifulSoup
import re
import datetime
def removeDuplicates(inputDict):
    uniqueLinks = set()
    nonEmptyHeadlines = {}
    
    for item in inputDict:
        link = item['link']
        headline = item['headline']
        # problem, resetting nonEmptyHeadlines instead of adding it to a list. to check previous headlines as well.
        
        if link in uniqueLinks:
            if headline and link not in nonEmptyHeadlines:
                nonEmptyHeadlines[link] = headline
        else:
            uniqueLinks.add(link)
            if headline:
                nonEmptyHeadlines[link] = headline
    
    uniqueDicts = [{'headline': headline, 'link': link} for link, headline in nonEmptyHeadlines.items()]
    
    return uniqueDicts
    
   

def divScraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pressReleases = []
    
    divs = soup.find_all('div')  # Find all <div> elements
    date_patterns = [
                    re.compile(r'(\d{2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4})', re.IGNORECASE),  # 05 Jun 2023
                    re.compile(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2},\s\d{4}', re.IGNORECASE),  # Aug 08, 2023
                    re.compile(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{2},\s\d{4}', re.IGNORECASE),  # August 08, 2023
                    re.compile(r'(\d{2}/\d{2}/\d{4})')  # mm/dd/yyyy
                ]
    for div in divs:
        try:
            date = ""
            headline = ""
            link = ""
            date_element = ''

            linkElement = div.find('a', href=True)  # Find <a> elements with href attribute
            if linkElement:
                link = linkElement['href']
                headline = linkElement.get_text().strip()
               # Extract date using regular expressions from the headline
                extracted_date = None
                
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
                                

                if not date:
                    date_element = div.find(class_=lambda x: x and "date" in x.lower(), recursive=False)
                    if date_element:
                        date = date_element.get_text().strip()  # Replace with actual extraction logic

                if not date:
                    date_elements = div.find_all(class_=re.compile(r'\bdate\b', flags=re.IGNORECASE))
                    for i in range(1,4):
                        if not date_elements:
                            pp = div.find_parent()
                            date_elements = pp.find_all(class_=re.compile(r'\bdate\b', flags=re.IGNORECASE))
                            div = pp
                            
                    if date_elements:
                        date = date_elements[0].get_text().strip()
                pressRelease = {
                    'headline': headline,
                    'link': link,
                    'date': date
                }
                if len(headline.split()) >= 5:
                    pressReleases.append(pressRelease)
        except (AttributeError, KeyError):
            pass
    return pressReleases

# url = 'https://ir.schrodinger.com/news-and-events/press-releases'
# linkPrefix = ''

# pressReleases = divScraper(url)

# uniquePressReleases = removeDuplicates(pressReleases)





# for pressRelease in uniquePressReleases:
#     print("Title:", pressRelease['headline'])
#     print("Link:", pressRelease['link'])
#     print('\n')
