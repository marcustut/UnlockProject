from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from infoboard.models import MissionDetail

import datetime

# Create your views here.


def redirectToLogin(request):
    return HttpResponseRedirect(reverse('login:login'))


def home(request):
    now = datetime.datetime.now().date() 
    missions = MissionDetail.objects.all().order_by('start_time')

    return render(request, 'home/home.html', {'now': now, 'missions': missions})
