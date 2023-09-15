from django.contrib import admin
from .models import Headlines, Company

class HeadlineAdmin(admin.ModelAdmin):
    list_display = ('company', 'headlines','link','date', 'seen')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'home_url')

admin.site.register(Company, CompanyAdmin)  # Register the Company model with custom admin options
admin.site.register(Headlines, HeadlineAdmin)  # Register the Headline model with the custom admin options defined earlier
