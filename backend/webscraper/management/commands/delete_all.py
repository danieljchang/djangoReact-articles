
from django.core.management.base import BaseCommand
from webscraper.models import Headlines,Company  # Replace 'your_app' with the actual name of your app

class Command(BaseCommand):
    help = 'Deletes all records in the Company and Headlines model'

    def handle(self, *args, **kwargs):
        try:
            Headlines.objects.all().delete()
            Company.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted all records in the Company and Headlines model.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
