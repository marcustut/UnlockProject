# Setting Django environment
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'unlock.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'
django.setup()

# Django Models
from home.models import Inspector
from django.db.models import Q

# Python Modules
import datetime
import time

# Parsing data from .txt file
allLines = [[], [], []]

with open('deductPointsM2B.txt') as f:
    for line in f:
        line_stripped = line.strip()

        if 'fail' in line_stripped.lower():
            appendTo = allLines[0]
            continue
        elif '5 marks' in line_stripped.lower():
            appendTo = allLines[1]
            continue
        elif '10 marks' in line_stripped.lower():
            appendTo = allLines[2]
            continue
        
        if line_stripped == '':
            continue

        appendTo.append(line_stripped)

fail = allLines[0]
d5marks = allLines[1]
d10marks = allLines[2]

# Query
for name in d5marks:
    inspector = Inspector.objects.get(name=name)
    inspector.points -= 5
    inspector.save()

    print(f'D5: {name} - {inspector.points}')

for name in d10marks:
    inspector = Inspector.objects.get(name=name)
    inspector.points -= 10
    inspector.save()

    print(f'D10: {name} - {inspector.points}')