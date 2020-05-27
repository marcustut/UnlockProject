from django.contrib import admin
from .models import Control

# Register your models here.


class ControlAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Game Control',    {'fields': ['game_time', 'ranking_switcher']})]
    list_display = ('game_time', 'ranking_switcher', 'is_game_time_now')


admin.site.register(Control, ControlAdmin)
