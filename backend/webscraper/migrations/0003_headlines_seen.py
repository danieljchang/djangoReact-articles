# Generated by Django 4.2.2 on 2023-09-08 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webscraper', '0002_headlines_delete_headline'),
    ]

    operations = [
        migrations.AddField(
            model_name='headlines',
            name='seen',
            field=models.BooleanField(default=True),
        ),
    ]
