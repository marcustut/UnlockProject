from django import forms
from .models import Inspector, MissionDetail, QuanMinScreenshot
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe

class ScreenshotForm(forms.ModelForm):

    class Meta:
        model = QuanMinScreenshot
        fields = ('images',)
