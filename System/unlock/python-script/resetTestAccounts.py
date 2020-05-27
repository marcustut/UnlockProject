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
        inspector.points = 0
        inspector.m1 = False
        inspector.m2 = False
        inspector.m3 = False
        inspector.m4 = False
        inspector.m5 = False
        inspector.m6 = False
        inspector.save()

        print(f"Success! Name: {inspector.name} Points: {inspector.points} {inspector.m1} {inspector.m2} {inspector.m3} {inspector.m4} {inspector.m5} {inspector.m6}")
    except:
        print(f"Something Wrong! Name: {inspector.name}")