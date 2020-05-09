from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.login, name='login'),
    path('postsign/', views.postsign, name='postsign'),
    path('logout/', views.logout, name='logout'),
]