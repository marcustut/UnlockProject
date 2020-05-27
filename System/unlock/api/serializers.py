from rest_framework import serializers
from home.models import Inspector, MissionDetail

class InspectorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Inspector
    exclude = ('user',)