from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def redirectToLogin(request):
    return HttpResponseRedirect(reverse('login:login'))

def home(request):
    return render(request, 'home/home.html')