from django.core.management.base import BaseCommand
from django.conf import settings
from .helpers.mainscrape import scrapeWeb
from webscraper.serializers import CompanySerializer, HeadlineSerializer
from webscraper.models import Company, Headlines
import datetime
from django.core.mail import send_mail
import os
from email.message import EmailMessage
import ssl
import smtplib
class Command(BaseCommand):
    
    help = 'Scrape news or press releases from websites, update database, send an email to recipients on any updates.'

    def handle(self, *args, **kwargs):
        print("scraping")
        try:
            # Scraping the web
            results = scrapeWeb()
            old = Headlines.objects.filter(seen=False)
            for old_headlines in old:
                old_headlines.seen = True
                old_headlines.save()
        
            print('Done scraping')
            # Checking if the company is already in the database, and in this case this should always be true, but in case we want to add websites that we want to scrape,
            for result in results:
                
                companyObj, createdCompany = Company.objects.get_or_create(
                    name = result['company'],
                    home_url = result['homeurl']
                    
                )
                if not createdCompany:
                    companyObj.name= result['company']
                    companyObj.home_url = result['homeurl']
                    companyObj.save()
                if result['date']:
                    try:
                        date = datetime.datetime.strptime(result['date'], "%B %d, %Y")
                    except ValueError:
                        try:
                            return datetime.datetime.strptime(result['date'], "%m/%d/%Y").date()
                        except ValueError:
                            date = None
                # Format the date as "YYYY-MM-DD"
                    if date is not None:
                        formatted = date.strftime("%Y-%m-%d")
                # Getting or creating a new object with these values, since we have changed the primary key to be the link
                # if the link already exists this should throw and error. 
                headlineObj, createdHeadline = Headlines.objects.get_or_create(
                    company = companyObj,
                    headlines = result['headline'],
                    link = result['link'],
                    date = formatted,
                    #seen = False
                )
                # If the headline is already in the article then we just update it.
                if not createdHeadline:
                    headlineObj.headlines = result['headline']
                    headlineObj.link = result['link']
                    headlineObj.date = formatted
                    # Only thing i changed
                    headlineObj.seen = True
                    headlineObj.save()
                    
            print('getheadline')
            new_headlines = Headlines.objects.filter(seen=False)
            print('gets')
            company_headlines = {}

            
            # Creating a dictionary with values of all the headlines of that company
            for headline in new_headlines:
                company_name = headline.company.name
                if company_name in company_headlines:
                    company_headlines[company_name].append((headline.headlines, headline.link))
                else:
                    company_headlines[company_name] = [(headline.headlines, headline.link)]

            # Getting the dates that we are scraping.
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            day = today.strftime("%B %d, %Y")
            week = week_ago.strftime("%B %d, %Y")
            
            
            
            ################################################################################################
            # Replace with own email.
            email_sender = 'danieljchang01@gmail.com'
            # NEED TO INPUT PASSWORD FOR A APPLICATION
            email_password = ''
            email_recevier = ['danielchang0000@gmail.com']
            # email_recevier = ['soujanya@gen1elifesci.com', 'sham@gen1elifesci.com', 'rishabh@gen1elifesci.com']
            
            ################################################################################################
            
            
            subject = 'New Company Update on Competitive Intelligence ' + week + ' to ' + day
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_recevier
            em['Subject'] = subject

            print('emailer')
            # Formatting the email to be 
            # Company Name 1
            # 1. Headline
            # 2. Headline
            # 3. Headline
            # Company 2
            # 1. Headline 
            #  ...
            html_content = '<html><body>'
            for company_name, headlines in company_headlines.items():
                
                html_content += f'<p><strong>{company_name}</strong></p>'
                for i, (headline, link) in enumerate(headlines, start=1):
                    print(headline)
                    html_content += f'<p>{i}. <a href="{link}">{headline}</a></p>'
            html_content += '\nLink to the dataset of all links, http://54.151.13.7:8000\n'

            html_content += '</body></html>'
            print('formatted')

            # Sending gmail messages so the smtp that we are using is this.
            # The account is created through https://myaccount.google.com/apppasswords
            if company_headlines:
                em.add_alternative(html_content, subtype='html')
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender,email_password)
                    smtp.sendmail(email_sender,email_recevier, em.as_string())
            else:
                message ='No updates this week.'
                em.set_content(message)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender,email_password)
                    smtp.sendmail(email_sender,email_recevier, em.as_string())

            self.stdout.write(self.style.SUCCESS('Successfully Scraped the web'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
    