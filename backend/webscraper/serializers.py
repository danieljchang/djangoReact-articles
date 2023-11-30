from rest_framework import serializers
from .models import Company, Headlines

class HeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headlines
        fields = ['link', 'company', 'headlines', 'date', 'seen']

class CompanySerializer(serializers.ModelSerializer):
    headlines = HeadlineSerializer(many=True, read_only=True)
    class Meta:
        model = Company
        fields = ['id', 'name', 'home_url', 'headlines']


# class ScrapeSerialzer(serializers.ModelSerializer):
#     class Meta:
#         model = Scrape
#         fields = ['id', 'lastScraped']
