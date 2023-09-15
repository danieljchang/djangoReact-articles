from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    home_url = models.URLField()
    
    def __str__(self):
        return self.name

class Headlines(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    headlines = models.CharField(max_length=200)
    link = models.URLField()
    date = models.DateField(null=True, blank=True)
    seen = models.BooleanField(default=True)
    def __str__(self):
        return self.headlines
