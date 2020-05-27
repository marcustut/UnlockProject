# Setting Django environment
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'unlock.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'
django.setup()

# Django Models
from home.models import Inspector

# Python Modules
import pandas as pd


# query 
groupsNotSubmit = Inspector.objects.filter(points=0)

# set variables
listNumber = []
listUsername = []
listSatellites = []
listPoints = []

for i in range(len(groupsNotSubmit)):
    username = groupsNotSubmit[i].name
    satellite = groupsNotSubmit[i].satellite
    points = groupsNotSubmit[i].points

    listNumber.append(i+1)
    listUsername.append(username)
    listSatellites.append(satellite)
    listPoints.append(points)

# Export to CSV using pandas DataFrame
Game1Info = {'No.': listNumber,
             'Group Name': listUsername,
             'Cluster/Satellites': listSatellites,
             'Points': listPoints,
    }

df = pd.DataFrame(Game1Info, columns=['No.', 'Group Name', 'Points', 'Cluster/Satellites'])
export_csv = df.to_csv(r'Game1.csv', index=None, header=True)
print(df)
