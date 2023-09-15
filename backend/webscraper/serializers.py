from rest_framework import serializers
from .models import Company, Headlines

class HeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headlines
        fields = ['id', 'company', 'headlines', 'link', 'date', 'seen']

class CompanySerializer(serializers.ModelSerializer):
    headlines = HeadlineSerializer(many=True, read_only=True)
    class Meta:
        model = Company
        fields = ['id', 'name', 'home_url', 'headlines']


