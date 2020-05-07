from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View

import datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import MissionDetail
# Create your views here.

tz = pytz.timezone('Asia/Kuala_Lumpur')
now = datetime.datetime(2020, 5, 29, 0, 0, 0).replace(tzinfo=tz)

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

class Submit(MissionSubmission):
    def get(self, request, mission_id):
        mission = MissionDetail.objects.all().filter(id=mission_id)[0]
        mission = newline_aware(mission)

        return render(request, 'home/submit.html', {'mission': mission})
