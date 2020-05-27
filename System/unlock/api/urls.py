from django.urls import path
from . import views

urlpatterns = [
  path('', views.apiOverview, name='api-overview'),
  path('inspector-list/', views.inspectorList, name='inspector-list'),
  path('inspector-view/<str:name>', views.inspectorView, name='inspector-view'),
  path('ranking/', views.ranking, name='ranking'),
]