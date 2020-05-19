from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth as django_auth
from django.contrib import messages 
# import pyrebase

from .forms import CreateUserForm

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
}

# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    else:
        return render(request, 'login/login.html')

def postsign(request):
    # email = request.POST.get('email')
    # password = request.POST.get('password')

    # try:
    #     user = auth.sign_in_with_email_and_password(email, password)
    # except:
    #     message = "Wrong Email or Password."
    #     return render(request, "login/login.html", {"message": message})
    # print(user['idToken'])

    # session_id = user['idToken']
    # request.session['uid'] = str(session_id)

    # return HttpResponseRedirect(reverse('home:home'))
    if request.user.is_authenticated:
        return redirect('home:home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = django_auth.authenticate(request, username=username, password=password)

            if user is not None:
                django_auth.login(request, user)
                # Django default redirect (LOGIN_REDIRECT_URL set in settings.py)
            else:
                messages.info(request, 'Username or Password is incorrect')
                return redirect('login:login')

            return redirect('home:home')
        else:
            messages.error(request, 'Wrong HTTP Method - ' + request.method)
            return render(request, 'login/error.html')

def logout(request):
    django_auth.logout(request)
    messages.info(request, "You are logged out.")
    # return render(request, 'login/login.html', {"message": "You're logged out."})
    return redirect('login:login')

def register(request):
    # email = request.POST.get('email')
    # password = request.POST.get('password')

    # try:
    #     user = auth.create_user_with_email_and_password(email, password)
    #     message = "Your account has been successfully registered."
    #     user['idToken']
    # except:
    #     message = "There's an issue creating your account."
    #     return render(request, "login/login.html", {"message": message})

    # return render(request, "login/login.html", {"message": message})
    if request.user.is_authenticated:
        return redirect('home:home')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)

                return redirect('login:login')

        return render(request, 'login/register.html', {"form": form})