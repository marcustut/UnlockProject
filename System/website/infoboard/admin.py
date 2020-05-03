from django.contrib import admin

# Register your models here.
from .models import *

class MissionDetailsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Mission Details',     {'fields': ['mission_title', 'mission_description', 'start_time', 'end_time']})
    ]
    list_display = ('mission_title', 'start_time', 'end_time', 'nearest_mission')
    list_filter = ['start_time']
    search_fields = ['mission_title']

class RulesAndRegulationsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Rule Description',    {'fields': ['rule']}),
        ('Date Information',    {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('rule', 'pub_date', 'was_added_recently')
    list_filter = ['pub_date']
    search_fields = ['rule']


class EmergencyContactAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Emergency Contact',            {'fields': ['name', 'phone_number']}),
    ]
    list_display = ('name', 'phone_number')
    search_fields = ['name']

admin.site.register(MissionDetail, MissionDetailsAdmin)
admin.site.register(RulesAndRegulation, RulesAndRegulationsAdmin)
admin.site.register(EmergencyContact, EmergencyContactAdmin)