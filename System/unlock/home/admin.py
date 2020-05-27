from django.contrib import admin
from .forms import ScreenshotForm

from .models import MissionDetail, Inspector, QuanMinScreenshot
from django.utils.html import mark_safe
# Register your models here.

class InspectorScreenshotAdmin(admin.TabularInline):
    model = QuanMinScreenshot
    verbose_name = '全民Party Screenshot'
    verbose_name = '全民Party Screenshots'
    max_num = 10

    readonly_fields = ['showScreenshot']

    def showScreenshot(self, model):
        try:
            return mark_safe(f'<img src="{model.images.url}" style="width: 100%; max-width: 100px; height:auto;"/>')
        except:
            return 'Screenshot is not uploaded yet'
    
    showScreenshot.short_description = 'Screenshot'

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
    search_fields = ['mission_title_chi', 'mission_title_eng']


class InspectorAdmin(admin.ModelAdmin):
    # inlines = [InspectorScreenshotAdmin]

    readonly_fields = ['showAudio']

    fieldsets = [
        ('Inspector Details',   {'fields': [
         'name', 'points', 'satellite']}),
        ('Mission 2',    {'fields': [
         'm2_a', 'm2_a_time_used', 'm2_b', 'm2_b_time_used', 'showAudio']}),
    ]

    # fieldsets = [
    #     ('Inspector Details',   {'fields': [
    #      'user', 'name', 'points', 'satellite']}),
    #     ('Mission 1',    {'fields': [
    #      'm1', 'm1_trials', 'm1_time_used']}),
    #     ('Mission 2',    {'fields': [
    #      'm2_a', 'm2_a_time_used', 'm2_b', 'm2_b_time_used', 'showAudio']}),
    #     ('Mission 3',    {'fields': [
    #      'm3', 'm3_time_used']}),
    #     ('Mission 4',    {'fields': [
    #      'm4', 'm4_time_used']}),
    #     ('Mission 5',    {'fields': [
    #      'm5', 'm5_trials', 'm5_time_used']}),
    #     ('Mission 6',    {'fields': [
    #      'm6', 'm6_time_used']}),
    # ]

    list_display = ('name', 'satellite', 'points', 'm2_b', 'm2_b_time_used', 'is_m2_b_submitted')
    list_filter = ['satellite']
    search_fields = ['name', 'satellite']

    show_full_result_count = False


admin.site.register(MissionDetail, MissionDetailsAdmin)
admin.site.register(Inspector, InspectorAdmin)
