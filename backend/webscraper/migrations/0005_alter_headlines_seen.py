# Generated by Django 4.2.2 on 2023-10-13 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webscraper', '0004_alter_headlines_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headlines',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]