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

for i in range(1, 51):
    username = 'testGame' + str(i)
    password = 'cycunlock'
    name = 'Game Tester ' + str(i)
    phone_number = '+601630668' + str(random.randint(10,99))

    try:
        user = User.objects.create_user(username=username, password=password)
        user.is_superuser = False
        user.is_staff = False
        user.save()

        inspector = Inspector(user=user,
                            name=name,
                            phone_number=phone_number,
                            satellite='KL',
                            pastoral_team='Hiro Team',
                            pastoral_cg='CYC 01J - Game Test')
        inspector.save()

        print(f'Inspector created {inspector.user} {inspector.name}')
    except:
        print('something wrong')



