from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('mission/', views.MissionSubmission.as_view(), name='mission'),
    path('mission/submit/<int:mission_id>', views.Submit.as_view(), name='submit'),
    path('mission/submit/<int:mission_id>/spot', views.spot, name='spot'),
]