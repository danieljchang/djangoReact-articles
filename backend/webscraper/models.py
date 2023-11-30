from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    home_url = models.URLField()
    
    def __str__(self):
        return self.name

class Headlines(models.Model):
    link = models.URLField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    headlines = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    def __str__(self):
        return self.headlines

# class Scrape(models.Model):
#     last_scraped = models.DateField()
#     def __str__(self):
#         return self.last_scraped

