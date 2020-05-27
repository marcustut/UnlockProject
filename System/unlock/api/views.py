from django.shortcuts import render
from django.http import JsonResponse

from home.models import Inspector, MissionDetail

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import InspectorSerializer

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
  api_urls = {
    'Inspector List': '/inspector-list',
    'Inspector View': '/inspector-view/<str:name>',
    'Ranking': '/ranking',
  }
  return Response(api_urls)

@api_view(['GET'])
def inspectorList(request):
  inspector = Inspector.objects.filter(name__startswith='UL')
  serializer = InspectorSerializer(inspector, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def inspectorView(request, name):
  inspector = Inspector.objects.get(name=name)
  serializer = InspectorSerializer(inspector, many=False)
  return Response(serializer.data)

@api_view(['GET'])
def ranking(request):
  # Taking all inspector sorted by highest points and reverse it
  topInspector = Inspector.objects.order_by('points', '-m1_time_used', 'm1_trials', '-m2_a_time_used', '-m2_b_time_used', '-m3_time_used', '-m4_time_used', '-m5_time_used', 'm5_trials', '-m6_time_used')[::1]
  topInspector.reverse()

  sortedInspector = []

  # Take only if 'UL' is present in name
  for inspector in topInspector:
      if inspector.name[:2] == 'UL':
          sortedInspector.append(inspector)

  group = [inspector.name for inspector in sortedInspector]
  satellite = [inspector.satellite for inspector in sortedInspector]
  points = [inspector.points for inspector in sortedInspector]

  # Ranking algorithmn
  sortedList = sorted(set(points))
  sortedList.reverse()
  rankdict = {v: k for k,v in enumerate(sortedList)}
  ranked = [rankdict[a] for a in points]

  # context to be passed as JSON
  context = {
      'group': group,
      'satellite': satellite,
      'points': points,
      'rankIndex': ranked,
  }

  return Response(context)