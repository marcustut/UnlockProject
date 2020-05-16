from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.contrib import messages 

import datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .models import MissionDetail, Inspector
from control.models import Control

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from googleapiclient.http import MediaFileUpload
# Create your views here.

# # time info
tz = pytz.timezone('Asia/Kuala_Lumpur')
# now = Control.objects.all().first().game_time.replace(tzinfo=tz)

# Google Drive Info
# define path variables
credentials_file_path = 'home/credentials/credentials.json'
clientsecret_file_path = 'home/credentials/client_secret.json'

# define API scope
SCOPE = 'https://www.googleapis.com/auth/drive'

# define store
store = file.Storage(credentials_file_path)
credentials = store.get()

# get access token
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(clientsecret_file_path, SCOPE)
    flags = tools.argparser.parse_args(args=[])
    credentials = tools.run_flow(flow, store, flags)

# define API service
http = credentials.authorize(Http())
drive = discovery.build('drive', 'v3', http=http)

# functions to be used
def change_tz_kl(mission):
    mission.start_time = mission.start_time.replace(tzinfo=tz)
    return mission

def newline_aware(mission):
    mission.mission_description_chi = mission.mission_description_chi.replace('\n', '<br>')
    mission.mission_description_eng = mission.mission_description_eng.replace('\n', '<br>')
    return mission

def check_mission_completed(user, mission_id):
    if mission_id == 1:
        return user.m1
    elif mission_id == 2:
        return user.m2
    elif mission_id == 3:
        return user.m3
    elif mission_id == 4:
        return user.m4
    elif mission_id == 5:
        return user.m5
    else:
        return user.m6

def check_carcam_ans(ans, q_no):
    if q_no == 1:
        if ans == '3' or ans == 'three' or ans == '三':
            return True
        else:
            return False
    elif q_no == 2:
        if ans == 'black' or ans == '黑色' or ans == '黑':
            return True
        else:
            return False
    elif q_no == 3:
        if ans == 'white' or ans == '白色' or ans == '白':
            return True
        else:
            return False
    elif q_no == 4:
        if ans == 'left' or ans == 'left side' or ans == '左' or ans == '左边':
            return True
        else:
            return False
    elif q_no == 5:
        if ans == 'blue' or ans == '蓝色' or ans == '蓝':
            return True
        else:
            return False
    else:
        return 'Wrong Question Number.'


@login_required(login_url='login:login')
def home(request):
    return render(request, 'home/home.html')

@method_decorator(login_required(login_url='login:login'), name='dispatch')
class MissionSubmission(View):
    missions = MissionDetail.objects.all().order_by('start_time')
    missions = list(map(change_tz_kl, missions))
    now = Control.objects.all().first().game_time.replace(tzinfo=tz)

    def get(self, request):
        user = Inspector.objects.all().filter(user__username__startswith=request.user.username)[0]
        now = Control.objects.all().first().game_time.replace(tzinfo=tz)

        context = {'now': now, 'missions': self.missions, 'user': user,}
        return render(request, 'home/mission_test.html', context)

@method_decorator(csrf_exempt, name='dispatch')
class Submit(MissionSubmission):
    def get(self, request, mission_id):
        mission = MissionDetail.objects.all().filter(id=mission_id)[0]
        mission = newline_aware(mission)
        user = Inspector.objects.all().filter(user__username__startswith=request.user.username)[0]
        now = Control.objects.all().first().game_time
        # now = datetime.datetime(2020, 6, 2, 16).replace(tzinfo=tz)

        if check_mission_completed(user, mission_id):
            return render(request, 'home/locked.html', {'mission': mission, 'condition': 'mission already completed'})
        elif now > mission.start_time and now < mission.end_time:
            return render(request, 'home/submit.html', {'mission': mission})
        elif now > mission.start_time:
            return render(request, 'home/locked.html', {'mission': mission, 'condition': 'time limit exceeded'})
        else:
            return render(request, 'home/locked.html', {'mission': mission, 'condition': 'mission in future'})


    def post(self, request, mission_id):
        request.upload_handlers = [TemporaryFileUploadHandler(request=request)]
        return self._post(request, mission_id)

    @method_decorator(csrf_protect)
    def _post(self, request, mission_id):
        # Taking models
        mission = MissionDetail.objects.all().filter(id=mission_id)[0]
        mission = newline_aware(mission)
        user = Inspector.objects.all().filter(user__username__startswith=request.user.username)[0]
        now = Control.objects.all().first().game_time
        # now = datetime.datetime(2020, 6, 2, 16).replace(tzinfo=tz)
        box1_invalid = None
        box2_invalid = None
        box3_invalid = None
        box4_invalid = None
        inputQ1_invalid = None
        inputQ2_invalid = None
        inputQ3_invalid = None
        inputQ4_invalid = None
        inputQ5_invalid = None

        print(now - mission.start_time)

        # Try submit answer
        try:
            if mission_id == 1:
                # Password JS Box
                time_used = now - mission.start_time

                # Validate answers
                if request.POST.get('box1') == '1' and request.POST.get('box2') == '0' and request.POST.get('box3') == '1' and request.POST.get('box4') == '5':
                    _pass = True
                else:
                    if request.POST.get('box1') != '1':
                        box1_invalid = True
                    elif request.POST.get('box1') == None:
                        box1_invalid = None
                    else:
                        box1_invalid = False

                    if request.POST.get('box2') != '0':
                        box2_invalid = True
                    elif request.POST.get('box2') == None:
                        box1_invalid = None
                    else:
                        box2_invalid = False

                    if request.POST.get('box3') != '1':
                        box3_invalid = True
                    elif request.POST.get('box3') == None:
                        box1_invalid = None
                    else:
                        box3_invalid = False

                    if request.POST.get('box4') != '5':
                        box4_invalid = True
                    elif request.POST.get('box4') == None:
                        box1_invalid = None
                    else:
                        box4_invalid = False

                    _pass = False

                # Pass the variables
                context = {
                    'mission': mission,
                    'box1_invalid': box1_invalid,
                    'box2_invalid': box2_invalid,
                    'box3_invalid': box3_invalid,
                    'box4_invalid': box4_invalid,
                    'box1': request.POST.get('box1'),
                    'box2': request.POST.get('box2'),
                    'box3': request.POST.get('box3'),
                    'box4': request.POST.get('box4'),
                }

                if _pass:
                    # Set time-attack rule
                    if time_used < datetime.timedelta(minutes=10):
                        user.points += 5
                    elif time_used < datetime.timedelta(minutes=20):
                        user.points += 4
                    elif time_used < datetime.timedelta(minutes=30):
                        user.points += 3
                    elif time_used < datetime.timedelta(minutes=40):
                        user.points += 2
                    else:
                        user.points += 1

                    user.m1 = True
                    user.save()
                else:
                    messages.error(request, "Your answers is incorrect, please check again.")
                    return render(request, 'home/submit.html', context)
            elif mission_id == 2:
                # Handle File Uploads
                uploaded_file = request.FILES['filename']

                uploaded_file.name = f'{user.name} ({user.satellite})'
                print(uploaded_file.name)
                print(uploaded_file.size)
                print(uploaded_file.temporary_file_path())
                print(uploaded_file.content_type)
                print(now-mission.start_time)
                # Limit file size to be at max 5MB
                if uploaded_file.size > 5242880:
                    messages.warning(request, "Your file has exceeded the 5MB limit. Please upload a smaller file.")
                    return render(request, 'home/submit.html', {'mission': mission})
                else:
                    file_metadata = {'name': uploaded_file.name, 'parents': ['1m1VPLAaBG5ZcacuyvoPGWfSxvNznyYHP']}
                    media = MediaFileUpload(uploaded_file.temporary_file_path(),
                                            mimetype=uploaded_file.content_type)
                    file = drive.files().create(body=file_metadata,
                                                        media_body=media,
                                                        fields='id').execute()
            elif mission_id == 3:
                # Handle File Uploads
                uploaded_file = request.FILES['filename']

                uploaded_file.name = f'{user.name} ({user.satellite})'
                print(uploaded_file.name)
                print(uploaded_file.size)
                print(uploaded_file.temporary_file_path())
                print(uploaded_file.content_type)
                print(now-mission.start_time)

                file_metadata = {'name': uploaded_file.name, 'parents': ['1aTq0ixgl0-0FVbACGsgB1sXDdVBxcqFw']}
                media = MediaFileUpload(uploaded_file.temporary_file_path(),
                                        mimetype=uploaded_file.content_type)
                file = drive.files().create(body=file_metadata,
                                                    media_body=media,
                                                    fields='id').execute()
            elif mission_id == 4:
                # Crossword JS Box
                pass
            elif mission_id == 5:
                # Carcam Form
                time_used = now - mission.start_time

                # Validate answers
                if check_carcam_ans(request.POST.get('inputQ1').strip().lower(), 1) and check_carcam_ans(request.POST.get('inputQ2').strip().lower(), 2) and check_carcam_ans(request.POST.get('inputQ3').strip().lower(), 3) and check_carcam_ans(request.POST.get('inputQ4').strip().lower(), 4) and check_carcam_ans(request.POST.get('inputQ5').strip().lower(), 5):
                    _pass = True
                else:
                    if not check_carcam_ans(request.POST.get('inputQ1').lower(), 1):
                        inputQ1_invalid = True
                    elif request.POST.get('inputQ1') == None:
                        inputQ1_invalid = None
                    else:
                        inputQ1_invalid = False

                    if not check_carcam_ans(request.POST.get('inputQ2').lower(), 2):
                        inputQ2_invalid = True
                    elif request.POST.get('inputQ2') == None:
                        inputQ2_invalid = None
                    else:
                        inputQ2_invalid = False

                    if not check_carcam_ans(request.POST.get('inputQ3').lower(), 3):
                        inputQ3_invalid = True
                    elif request.POST.get('inputQ3') == None:
                        inputQ3_invalid = None
                    else:
                        inputQ3_invalid = False

                    if not check_carcam_ans(request.POST.get('inputQ4').lower(), 4):
                        inputQ4_invalid = True
                    elif request.POST.get('inputQ4') == None:
                        inputQ4_invalid = None
                    else:
                        inputQ4_invalid = False

                    if not check_carcam_ans(request.POST.get('inputQ5').lower(), 5):
                        inputQ5_invalid = True
                    elif request.POST.get('inputQ5') == None:
                        inputQ5_invalid = None
                    else:
                        inputQ5_invalid = False

                    _pass = False

                # Pass the variables
                context = {
                    'mission': mission,
                    'inputQ1_invalid': inputQ1_invalid,
                    'inputQ2_invalid': inputQ2_invalid,
                    'inputQ3_invalid': inputQ3_invalid,
                    'inputQ4_invalid': inputQ4_invalid,
                    'inputQ5_invalid': inputQ5_invalid,
                    'inputQ1': request.POST.get('inputQ1'),
                    'inputQ2': request.POST.get('inputQ2'),
                    'inputQ3': request.POST.get('inputQ3'),
                    'inputQ4': request.POST.get('inputQ4'),
                    'inputQ5': request.POST.get('inputQ5'),
                }

                if _pass:
                    # Set time-attack rule
                    if time_used < datetime.timedelta(minutes=10):
                        user.points += 5
                    elif time_used < datetime.timedelta(minutes=20):
                        user.points += 4
                    elif time_used < datetime.timedelta(minutes=30):
                        user.points += 3
                    elif time_used < datetime.timedelta(minutes=40):
                        user.points += 2
                    else:
                        user.points += 1

                    user.m5 = True
                    user.save()
                else:
                    messages.error(request, "Your answers is incorrect, please check again.")
                    return render(request, 'home/submit.html', context)
            else:
                # Finale Escape Game
                pass
            return render(request, 'home/success.html', {'cg': user.pastoral_cg, 'mission': mission})
        except:
            return render(request, 'home/error.html', {'cg': user.pastoral_cg, 'mission': mission})

@login_required(login_url='login:login')
def spot(request, mission_id):
    return render(request, 'home/spot.html')