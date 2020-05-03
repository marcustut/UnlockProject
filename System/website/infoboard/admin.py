from django.contrib import admin

# Register your models here.
from .models import EmergencyContact

class EmergencyContactAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',            {'fields': ['name']}),
        ('Phone Number',    {'fields': ['phone_number']}),
    ]
    list_display = ('name', 'phone_number')
    search_fields = ['name']

admin.site.register(EmergencyContact, EmergencyContactAdmin)