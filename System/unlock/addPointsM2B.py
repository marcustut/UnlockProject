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

while True:
    # query Database for latest results
    try:
        groupsVerified = Inspector.objects.filter(~Q(m2_b_time_used=datetime.timedelta(0, 21600)) & Q(name__startswith='UL'))
    except:
        raise QueryError("Unable to query the database.")

    # Logging
    log = open(r"m2_log.txt", "a")

    # Update the points
    for group in groupsVerified:
        if group.m2_a and group.m2_b and group.m2_b_time_used != datetime.timedelta(0, 21600) and group.points == 75:
            group.points += 25
            group.save()
            log_msg = f'Updated(Add Points) - {group.name}: {group.points - 25} to {group.points}'
            log.write(log_msg)
            print(log_msg)
        elif group.m2_a and group.m2_b and group.m2_b_time_used != datetime.timedelta(0, 21600) and group.points == 25:
            group.points += 25
            group.save()
            log_msg = f'Updated(Add Points) - {group.name}: {group.points - 25} to {group.points}'
            log.write(log_msg)
            print(log_msg)


    log.close()

    # Run every second
    time.sleep(1)
    
