from django.shortcuts import render

from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from .serializers import CompanySerializer, HeadlineSerializer
from .models import Company, Headlines
from .views import *
import requests
from django.http import JsonResponse
from django.http import HttpResponse
import subprocess
from django.shortcuts import render
from django.http import HttpResponseRedirect
import csv
# Create your views here.

def index(request):
    return render(request, 'index.html')


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class HeadlineViewSet(viewsets.ModelViewSet):
    serializer_class = HeadlineSerializer
    queryset = Headlines.objects.all()


def get_headlines(request, company_id):
    try:
        # Attempt to convert company_id to an integer
        company_id = int(company_id)
        headlines = Headlines.objects.filter(company_id=company_id)
        # Your code to serialize headlines to JSON
        serialized = HeadlineSerializer(headlines, many=True).data

        return JsonResponse(serialized, safe=False)
    except ValueError:
        # Handle the case where company_id is not a valid integer
        return JsonResponse({'error': 'Invalid companyId'}, status=400)


def inputData(request):
    company = CompanyViewSet
    
def delete_resource(request, resource_id):
    # Make the DELETE request to the API endpoint
    api_endpoint = f'http://localhost:8000/company/{resource_id}/'
    response = requests.delete(api_endpoint)

    if response.status_code == 204:
        return JsonResponse({'message': 'Deletion successful'})
    else:
        return JsonResponse({'error': 'Failed to delete'}, status=500)
    
    # views.py


@csrf_exempt
def process_csv(request):
    print("processing")
    try:
        request.FILES.get('csv_file')
        csv_file = request.FILES['csv_file']
        csv_bytes = csv_file.read()

            # Decode the bytes to text (assuming it's UTF-8 encoded)
        csv_text = csv_bytes.decode('utf-8')

        # Now you can work with the CSV content as a string
        csv_reader = csv.DictReader(csv_text.splitlines(), delimiter='|')
        if csv_reader:
            print("something inside")
        for result in csv_reader:
            print(result['company'], result['date'], result['headline'])
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
                    headlineObj, createdHeadline = Headlines.objects.get_or_create(
                        company = companyObj.id,
                        headlines = result['headline'],
                        link = result['link'],
                        date = result['date'],
                        seen = False
                    )
                    if not createdHeadline:
                        headlineObj.headlines = result['headline']
                        headlineObj.link = result['link']
                        headlineObj.date = result['date']
                        headlineObj.seen = True
                        headlineObj.save()
                except ValueError:
                    print(f'Invalid date format: {result["date"]}')

            else:
                print("sadge")
    
        print("done")
        return HttpResponseRedirect('/success/')
    except Exception as e:
        print(e)
        return HttpResponse(f'Error: {str(e)}')


def run_custom_command(request):
    try:
        command_name = 'scrapeNews'
        
        # Execute the management command using subprocess
        subprocess.run(['python', 'manage.py', command_name])
        # result will have:
        # fieldnames = ["company", "headline", "link", 'homeurl', 'date']

        
        
        return HttpResponse('Command executed successfully.')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
