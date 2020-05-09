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

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from googleapiclient.http import MediaFileUpload
# Create your views here.

# time info
tz = pytz.timezone('Asia/Kuala_Lumpur')
now = datetime.datetime(2020, 6, 2, 16, 0, 0).replace(tzinfo=tz)

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

@login_required(login_url='login:login')
def home(request):
    return render(request, 'home/home.html')

@method_decorator(login_required(login_url='login:login'), name='dispatch')
class MissionSubmission(View):
    missions = MissionDetail.objects.all().order_by('start_time')
    missions = list(map(change_tz_kl, missions))

    def get(self, request):
        context = {'now': now, 'missions': self.missions}
        return render(request, 'home/mission.html', context)

@method_decorator(csrf_exempt, name='dispatch')
class Submit(MissionSubmission):
    def get(self, request, mission_id):
        mission = MissionDetail.objects.all().filter(id=mission_id)[0]
        mission = newline_aware(mission)

        if now > mission.start_time:
            return render(request, 'home/submit.html', {'mission': mission})
        else:
            return render(request, 'home/locked.html', {'mission': mission})


    def post(self, request, mission_id):
        request.upload_handlers = [TemporaryFileUploadHandler(request=request)]
        return self._post(request, mission_id)

    @method_decorator(csrf_protect)
    def _post(self, request, mission_id):
        mission = MissionDetail.objects.all().filter(id=mission_id)[0]
        mission = newline_aware(mission)

        uploaded_file = request.FILES['filename']

        # Renaming uploaded files to CG Name.
        user = Inspector.objects.all().filter(user__username__startswith=request.user.username)[0]

        uploaded_file.name = user.pastoral_cg
        print(uploaded_file.name)
        print(uploaded_file.size)
        print(uploaded_file.temporary_file_path())
        print(uploaded_file.content_type)

        try:
            if mission_id == 1:
                # Limit file size to be at max 5MB
                if uploaded_file.size > 5242880:
                    messages.warning(request, "Your file has exceeded the 5MB limit. Please upload a smaller file.")
                    return render(request, 'home/submit.html', {'mission': mission})
                else:
                    file_metadata = {'name': uploaded_file.name, 'parents': ['1NvwJXfpicegTPYKOUtHw_F3q76O3Rh5t']}
                    media = MediaFileUpload(uploaded_file.temporary_file_path(),
                                            mimetype=uploaded_file.content_type)
                    file = drive.files().create(body=file_metadata,
                                                        media_body=media,
                                                        fields='id').execute()
            elif mission_id == 2:
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
                file_metadata = {'name': uploaded_file.name, 'parents': ['1aTq0ixgl0-0FVbACGsgB1sXDdVBxcqFw']}
                media = MediaFileUpload(uploaded_file.temporary_file_path(),
                                        mimetype=uploaded_file.content_type)
                file = drive.files().create(body=file_metadata,
                                                    media_body=media,
                                                    fields='id').execute()
            elif mission_id == 4:
                file_metadata = {'name': uploaded_file.name, 'parents': ['1hkn8jmCcvaJHnkyjIwW4JhI4SZxvobB1']}
                media = MediaFileUpload(uploaded_file.temporary_file_path(),
                                        mimetype=uploaded_file.content_type, resumable=True)
                file = drive.files().create(body=file_metadata,
                                                    media_body=media,
                                                    fields='id').execute()
            elif mission_id == 5:
                # Limit file size to be at max 5MB
                if uploaded_file.size > 5242880:
                    messages.warning(request, "Your file has exceeded the 5MB limit. Please upload a smaller file.")
                    return render(request, 'home/submit.html', {'mission': mission})
                else:
                    file_metadata = {'name': uploaded_file.name, 'parents': ['1Xx3SBrW48N3ofjKTgH9kwHDjHFjA6F2n']}
                    media = MediaFileUpload(uploaded_file.temporary_file_path(),
                                            mimetype=uploaded_file.content_type)
                    file = drive.files().create(body=file_metadata,
                                                        media_body=media,
                                                        fields='id').execute()
            return render(request, 'home/success.html', {'cg': user.pastoral_cg, 'mission': mission})
        except:
            return render(request, 'home/error.html', {'cg': user.pastoral_cg, 'mission': mission})
