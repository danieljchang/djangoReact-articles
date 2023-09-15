import re
import datetime
def inText(headline):
    extracted_date = None
    date = ''            
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
    return date

def getDates(element):
    commonParent = element.find_parent()
    date = ""
    date_elements = commonParent.find_all(class_=lambda class_: class_ and "date" in class_.lower())
    # date_elements = commonParent.find_all(class_=re.compile(r'\bdate\b', flags=re.IGNORECASE))
    for i in range(1,4):
        if not date_elements:
            pp = commonParent.find_parent()
            # date_elements = pp.find_all(class_=re.compile(r'\bdate\b', flags=re.IGNORECASE))
            date_elements = commonParent.find_all(class_=lambda class_: class_ and "date" in class_.lower())
            commonParent = pp
            
      

    if date_elements:
        # Extract text from all date elements and concatenate
        date = date_elements[0].get_text().strip()
        
        
    if not date: #Still hasn't worked so now i am going to get the text and then just parse any text for dates.
        commonParent = element.find_parent()
        parentparent = commonParent.find_parent()
        
        date = inText(parentparent.get_text().strip())

    return date
