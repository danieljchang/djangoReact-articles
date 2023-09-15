from django.core.management.base import BaseCommand
from django.conf import settings
from .helpers.mainscrape import scrapeWeb
from webscraper.serializers import CompanySerializer, HeadlineSerializer
from webscraper.models import Company, Headlines
import datetime
class Command(BaseCommand):
    help = 'Scrape news or press releases from websites'

    def handle(self, *args, **kwargs):
        try:
            results = scrapeWeb()
            
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

                headlineObj, createdHeadline = Headlines.objects.get_or_create(
                    company = companyObj,
                    headlines = result['headline'],
                    link = result['link'],
                    date = formatted,
                    seen = False
                )
                if not createdHeadline:
                    headlineObj.headlines = result['headline']
                    headlineObj.link = result['link']
                    headlineObj.date = formatted
                    headlineObj.seen = True
                    headlineObj.save()
                
            self.stdout.write(self.style.SUCCESS('Successfully Scraped the web'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
    