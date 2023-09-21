"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from webscraper import views


router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet, 'company')
router.register(r'headlines', views.HeadlineViewSet, 'headlines')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),

    path('delete/<int:resource_id>/', views.delete_resource, name='delete_resource'),
    path('run-custom-command/', views.run_custom_command, name='run_custom_command'),
    path('process-csv/', views.process_csv, name='process_csv'),
    path('get-headlines/<int:company_id>/', views.get_headlines, name='get_headlines'),
    path('get-company/<int:company_id>/', views.get_company, name='get_company'),


    # Other URL patterns...
]
