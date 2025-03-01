# Setting Django environment
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'unlock.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'
django.setup()

import random
import time, sys, select

# Import models
from home.models import Inspector
from django.contrib.auth.models import User

while True:
    inspectors = Inspector.objects.all().filter(name__startswith='Lee Kai Yang')

    for inspector in inspectors:
        try:
            print(f"{inspector.name} Points: {inspector.points} {inspector.m1} {inspector.m2_a} {inspector.m2_b} {inspector.m3} {inspector.m4} {inspector.m5} {inspector.m6}")
        except:
            print(f"Something Wrong! Name: {inspector.name}")
    time.sleep(1)
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    if i == [sys.stdin]: break
print("End Checking Admin Accounts")
