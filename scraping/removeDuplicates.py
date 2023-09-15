def remove(inputDict):
    uniqueLinks = set()
    nonEmptyHeadlines = {}
    
    for item in inputDict:
        link = item['link']
        headline = item['headline']
        date = item['date']
        if 'download' in headline.lower():
            continue
        
        if link in uniqueLinks:
            if headline and link not in nonEmptyHeadlines:
                nonEmptyHeadlines[link] = {'headline': headline, 'date': date}  # Include date
        else:
            uniqueLinks.add(link)
            if headline:
                nonEmptyHeadlines[link] = {'headline': headline, 'date': date}  # Include date
    
    uniqueDicts = [{'headline': data['headline'], 'link': link, 'date': data['date']} for link, data in nonEmptyHeadlines.items()]
    
    return uniqueDicts