from django.conf import settings
import django
import os
import sys
import subprocess


#* * * * * /usr/bin/python3 djangoReact-articles/backend/manage.py sendEmail 



command_name = 'sendEmail'
# Execute the management command using subprocess
subprocess.run(['python3', 'manage.py', command_name])
print("running from the cronjob scraping news")
