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
      groupsSubmitted = Inspector.objects.filter(~Q(m2_b_time_used=datetime.timedelta(0, 21600)) & Q(name__startswith='UL'))
    except:
      raise QueryError("Unable to query the database.")

    # Logging
    log = open(r"m2_progress.txt", "w+")

    verifiedGroups = []

    # Update the points
    for group in groupsSubmitted:
      if group.m2_a and group.m2_b and group.m2_b_time_used != datetime.timedelta(0, 21600) and group.points == 100:
        verifiedGroups.append(group)
      elif group.m2_a and group.m2_b and group.m2_b_time_used != datetime.timedelta(0, 21600) and group.points == 50:
        verifiedGroups.append(group)

    groupsNotSubmitted = 328 - len(groupsSubmitted)
    currentProgress = len(verifiedGroups)/len(groupsSubmitted) * 100
    submissionProgress = len(groupsSubmitted)/328 * 100

    log_msg = f'*Mission 2 Progress({datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})*\nGroups Submitted: {len(groupsSubmitted)}\nGroups Verified: {len(verifiedGroups)}\nVerification Progress: {len(verifiedGroups)}/{len(groupsSubmitted)} ({currentProgress:.2f}%)\nSubmission Progress: {len(groupsSubmitted)}/329 ({submissionProgress:.2f}%)\n'
    log.write(log_msg)
    print(log_msg)

    log.close()

    # Run every second
    time.sleep(60)
    
