# Google Sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setting Django environment
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'unlock.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'
django.setup()

# Django Models
from django.contrib.auth.models import User
from home.models import Inspector

# Python Libraries
import random
import string
from pandas import DataFrame

# Set Up Google Sheets
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("unlock2020-service-account.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Unlock_Grouping").sheet1
data = sheet.get_all_records()

# Generate random password
def randomPassword(lettersCount=4, digitsCount=4):
    sampleStr = ''.join((random.choice(string.ascii_lowercase) for i in range(lettersCount)))
    sampleStr += ''.join((random.choice(string.digits) for i in range(digitsCount)))
    return sampleStr

# Set variables
listNumber = []
listFirstName = []
listUsername = []
listPassword = []
listSatellite = []

for i in range(len(data)):
    username = data[i]['Group Name']
    password = randomPassword()
    email = data[i]['Email Address']
    firstName = data[i]['Group Leader']
    satellite = data[i]['Cluster/Satellites']

    listNumber.append(i+1)
    listFirstName.append(firstName)
    listUsername.append(username)
    listPassword.append(password)
    listSatellite.append(satellite)
    
    try:
        # User Model
        newUser = User(username=username, email=email, first_name=firstName)
        newUser.set_password(password)
        newUser.save()

        # Inpestor Model
        newInspector = Inspector(user=newUser, name=username, satellite=satellite)
        newInspector.save()

        print(f'Successfully created - {username}')
    except:
        print(f'Error Occured - {username}')

# Export to CSV using pandas DataFrame
accountInfo = {'No.': listNumber,
                'Group Leader': listFirstName,
                'Username': listUsername,
                'Password': listPassword,
                'Cluster/Satellites': listSatellite,
    }

df = DataFrame(accountInfo, columns=['No.', 'Group Leader', 'Username', 'Password', 'Cluster/Satellites'])
export_csv = df.to_csv(r'accountInfo_v2.csv', index=None, header=True)
print(df)