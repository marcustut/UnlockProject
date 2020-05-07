from django.contrib import admin

# Register your models here.
from .models import *

class RulesAndRegulationsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Rule Description',    {'fields': ['rule_chi', 'rule_eng']}),
        ('Date Information',    {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('rule_chi', 'rule_eng', 'pub_date', 'was_added_recently')
    list_filter = ['pub_date']
    search_fields = ['rule_eng']


class EmergencyContactAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Emergency Contact',            {'fields': ['name_chi', 'name_eng', 'phone_number']}),
    ]
    list_display = ('name_chi', 'name_eng', 'phone_number')
    search_fields = ['name_eng']

admin.site.register(RulesAndRegulation, RulesAndRegulationsAdmin)
admin.site.register(EmergencyContact, EmergencyContactAdmin)