from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth as django_auth
import pyrebase

# Firebase Config
config = {
    'apiKey': "AIzaSyAXYyxxAUC3twzfRBMMd5WLlqVxSc_J17M",
    'authDomain': "unlock2020.firebaseapp.com",
    'databaseURL': "https://unlock2020.firebaseio.com",
    'projectId': "unlock2020",
    'storageBucket': "unlock2020.appspot.com",
    'messagingSenderId': "826459049639",
    'appId': "1:826459049639:web:e56e964ae0a291d4029582",
    'measurementId': "G-3PL9VWKPM1"
};

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

def register(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        auth.create_user_with_email_and_password(email, password)
        message = "Your account has been successfully registered."
    except:
        message = "There's an issue creating your account."
        return render(request, "login/login.html", {"message": message})

    return render(request, "login/login.html", {"message": message})