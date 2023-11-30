from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from webscraper.models import Company, Headlines
import datetime
import os
from email.message import EmailMessage
import ssl
import smtplib
class Command(BaseCommand):
    def handle(self, *args, **options):
        
        try:
            # old = Headlines.objects.filter(seen=False)
            # for old_headlines in old:
            #     old_headlines.seen = True
            #     old_headlines.save()
                
            new_headlines = Headlines.objects.filter(seen=False)

            company_headlines = {}

            
            # Creating a dictionary with values of all the headlines of that company
            for headline in new_headlines:
                company_name = headline.company.name
                if company_name in company_headlines:
                    company_headlines[company_name].append((headline.headlines, headline.link))
                else:
                    company_headlines[company_name] = [(headline.headlines, headline.link)]


            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            day = today.strftime("%B %d, %Y")
            week = week_ago.strftime("%B %d, %Y")

            email_sender = 'danieljchang01@gmail.com'
            email_password = 'kdtb oink ebrf clol'
            email_recevier = ['danielchang0000@gmail.com']
            subject = 'New Company Update on Competitive Intelligence ' + week + ' to ' + day

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_recevier
            em['Subject'] = subject

            html_content = '<html><body>'
            for company_name, headlines in company_headlines.items():
                html_content += f'<p><strong>{company_name}</strong></p>'
                for i, (headline, link) in enumerate(headlines, start=1):

                    html_content += f'<p>{i}. <a href="{link}">{headline}</a></p>'

            html_content += '</body></html>'


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

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
    