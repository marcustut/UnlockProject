from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import MissionDetail

import datetime

# Create your views here.


def redirectToLogin(request):
    return HttpResponseRedirect(reverse('login:login'))


def home(request):
    if request.session['uid'] != None:
        now = datetime.datetime(2020, 5, 29).date()
        missions = MissionDetail.objects.all().order_by('start_time')

        return render(request, 'home/home.html', {'now': now, 'missions': missions})
    else:
        return HttpResponseRedirect(reverse('login:login'))
