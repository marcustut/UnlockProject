from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.redirectToLogin, name='redirectToLogin'),
    path('home/', views.home, name='home'),
]