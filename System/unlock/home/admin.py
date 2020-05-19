from django.contrib import admin

from .models import *
# Register your models here.


class MissionDetailsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Mission Details',     {'fields': ['mission_title_chi',
                                            'mission_title_eng',
                                            'mission_description_chi',
                                            'mission_description_eng',
                                            'start_time',
                                            'end_time']})
    ]
    list_display = ('mission_title_chi', 'mission_title_eng', 'start_time',
                    'end_time', 'nearest_mission')
    list_filter = ['start_time']
    search_fields = ['mission_title_chi', 'mission_title_eng']


class InspectorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Inspector Details',   {'fields': [
         'user', 'name', 'phone_number', 'points']}),
        ('Pastoral Details',    {'fields': [
         'satellite', 'pastoral_team', 'pastoral_cg']}),
        ('Mission Progress',    {'fields': [
         'm1', 'm2_a', 'm2_b', 'm3', 'm4', 'm5', 'm5_trials', 'm6']})
    ]
    list_display = ('user', 'name', 'phone_number', 'satellite', 'pastoral_cg')
    list_filter = ['satellite']
    search_fields = ['name', 'satellite', 'pastoral_cg']


admin.site.register(MissionDetail, MissionDetailsAdmin)
admin.site.register(Inspector, InspectorAdmin)
