# Setting Django environment
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'unlock.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'
django.setup()

import random

# Import models
from home.models import Inspector
from django.contrib.auth.models import User

inspectors = Inspector.objects.all().filter(name__startswith='Game Tester')

for inspector in inspectors:

    try:
        print(f"{inspector.name} Points: {inspector.points} {inspector.m1} {inspector.m2} {inspector.m3} {inspector.m4} {inspector.m5} {inspector.m6}")
    except:
        print(f"Something Wrong! Name: {inspector.name}")