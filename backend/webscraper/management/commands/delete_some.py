
from django.core.management.base import BaseCommand
from webscraper.models import Headlines,Company  # Replace 'your_app' with the actual name of your app

class Command(BaseCommand):
    help = 'Deletes all records in the Company and Headlines model'

    def handle(self, *args, **kwargs):
        try:
            Headlines.objects.filter(link='https://www.arcutis.com/arcutis-announces-positive-results-from-integument-ped-pivotal-phase-3-trial-of-roflumilast-cream-0-05-for-the-treatment-of-atopic-dermatitis-in-children-ages-2-to-5/').delete()
            # Company.objects.filter(link=136).delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted all records in the Company and Headlines model.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
