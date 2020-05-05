from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth as django_auth
import pyrebase

# Firebase Config
config = {
    "apiKey": "AIzaSyB6L2YFRF0_MBQ015peiSG_9WaUXMKToDk",
    "authDomain": "quickstart-1588101344876.firebaseapp.com",
    "databaseURL": "https://quickstart-1588101344876.firebaseio.com",
    "projectId": "quickstart-1588101344876",
    "storageBucket": "quickstart-1588101344876.appspot.com",
    "messagingSenderId": "788784957362",
    "appId": "1:788784957362:web:6d49b59fc2716acf0d06ab",
    "measurementId": "G-KDPE0NY6Z4",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Create your views here.

def login(request):
    return render(request, 'login/login.html')

def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except:
        message = "Wrong Email or Password."
        return render(request, "login/login.html", {"message": message})
    print(user['idToken'])

    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    return HttpResponseRedirect(reverse('home:home'))

def logout(request):
    django_auth.logout(request)
    return render(request, 'login/login.html')