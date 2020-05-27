from django.db import models
from django import forms
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils.html import mark_safe, format_html
import datetime

# Functions to be used

def audio_upload_path(instance, filename):
    return f'inspectors/{instance.name}/audios/{filename}'

def screenshot_upload_path(instance, filename):
    return f'inspectors/{instance.name}/sreenshots/{filename}'

# Create your models here.

class MissionDetail(models.Model):
    mission_title_chi = models.CharField(max_length=200, default='输入任务主题')
    mission_title_eng = models.CharField(max_length=200, default='Insert Mission Title here.')
    mission_description_chi = models.TextField(default='输入任务资料')
    mission_description_eng = models.TextField(default='Insert Mission Details Here.')
    start_time = models.DateTimeField('Start Time')
    end_time = models.DateTimeField('End Time')

    def check_date(self, year, month, day):
        start_time = datetime.datetime(year, month, day, 0, 0, tzinfo=None)
        end_time = datetime.datetime(year, month, day, 23, 59, tzinfo=None)
        return start_time <= self.start_time.replace(tzinfo=None) <= end_time

    def nearest_mission(self):
        now = datetime.datetime.now().astimezone()
        return now >= self.end_time

    nearest_mission.admin_order_field = 'end_time'
    nearest_mission.boolean = True
    nearest_mission.short_description = 'Mission Finished'

    def __str__(self):
        return self.mission_title_chi + ' ' + self.mission_title_eng

class Inspector(models.Model):
    SATELLITE_CHOICES = [
        ('KLMV', 'KL Move'),
        ('KLV', 'KL Voice'),
        ('KLH', 'KL Heart'),
        ('KLMD', 'KL Mind'),
        ('KLF', 'KL Force'),
        ('KLS', 'KL Strike'),
        ('PUC', 'Puchong'),
        ('STP', 'Setapak'),
        ('RW', 'Rawang'),
        ('PJ', 'Petaling Jaya'),
        ('USJ', 'USJ'),
        ('KLG', 'Klang'),
        ('KP', 'Kepong'),
        ('SB', 'Seremban'),
        ('SD', 'Serdang'),
        ('KJ', 'Kajang'),
        ('SGL', 'Sungai Long'),
    ]

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    satellite = models.CharField(max_length=200, choices=SATELLITE_CHOICES)
    points = models.IntegerField(default=0)

    m1 = models.BooleanField(verbose_name='m1 completed', default=False)
    m1_trials = models.IntegerField(verbose_name='m1 trials', default=15)
    m1_time_used = models.DurationField(verbose_name='m1 time used', default=datetime.timedelta(hours=1))

    m2_a = models.BooleanField(verbose_name='m2_a(guess song) completed', default=False)
    m2_a_time_used = models.DurationField(verbose_name='m2_a time used', default=datetime.timedelta(hours=6))

    m2_b = models.BooleanField(verbose_name='m2_b(translate song) completed', default=False)
    m2_b_time_used = models.DurationField(verbose_name='m2_b time used', default=datetime.timedelta(hours=6))

    m3 = models.BooleanField(verbose_name='m3 completed', default=False)
    m3_time_used = models.DurationField(verbose_name='m3 time used', default=datetime.timedelta(hours=2.5))

    m4 = models.BooleanField(verbose_name='m4 completed', default=False)
    m4_time_used = models.DurationField(verbose_name='m4 time used', default=datetime.timedelta(hours=2.5))

    m5 = models.BooleanField(verbose_name='m5 completed', default=False)
    m5_trials = models.IntegerField(verbose_name='m5 trials', default=10)
    m5_time_used = models.DurationField(verbose_name='m5 time used', default=datetime.timedelta(hours=12))

    m6 = models.BooleanField(verbose_name='m6 completed', default=False)
    m6_time_used = models.DurationField(verbose_name='m6 time used', default=datetime.timedelta(hours=3))

    m2_b_audio1 = models.FileField(upload_to=audio_upload_path, default='/game/audio/CorruptedAudioChinese.mp3')
    m2_b_audio2 = models.FileField(upload_to=audio_upload_path, default='/game/audio/CorruptedAudioChinese.mp3')
    m2_b_audio3 = models.FileField(upload_to=audio_upload_path, default='/game/audio/CorruptedAudioChinese.mp3')
    m2_b_audio4 = models.FileField(upload_to=audio_upload_path, default='/game/audio/CorruptedAudioChinese.mp3')
    m2_b_audio5 = models.FileField(upload_to=audio_upload_path, default='/game/audio/CorruptedAudioChinese.mp3')
    m2_b_audio6 = models.FileField(upload_to=audio_upload_path, default='/game/audio/CorruptedAudioChinese.mp3')
    m2_b_audio7 = models.FileField(upload_to=audio_upload_path, default='/game/audio/CorruptedAudioChinese.mp3')
    m2_b_audio8 = models.FileField(upload_to=audio_upload_path, default='/game/audio/CorruptedAudioChinese.mp3')


    def is_m2_b_submitted(self):
        return self.m2_b_time_used != datetime.timedelta(hours=6)
    
    is_m2_b_submitted.admin_order_field = '-m2_b_time_used'
    is_m2_b_submitted.boolean = True
    is_m2_b_submitted.short_description = 'm2_b submitted?'

    def showAudio(self):
        if 'CorruptedAudioChinese.mp3' in self.m2_b_audio1.name:
            return format_html('<div style="display: flex; text-align: center; justify-content: center; flex-wrap: wrap; padding: 5px;"><div style="margin: 5px;"><h1 style="color: #D32F2F;"><b>This group hasn\'t submit yet.</b></h1></div>')

        html_audio = ''
        audio = [self.m2_b_audio1, self.m2_b_audio2, self.m2_b_audio3, self.m2_b_audio4, self.m2_b_audio5, self.m2_b_audio6, self.m2_b_audio7, self.m2_b_audio8]
        audio_name = []

        for i in range(len(audio)):
            audio_name.append(audio[i].name.split('/')[-1])

        return format_html((
                            '<div style="display: flex; text-align: center; justify-content: center; flex-wrap: wrap; padding: 5px;"><div style="margin: 5px;"><p><b>{0}</b></p><audio controls><source src="{1}"></audio></div>'
                            '<div style="margin: 5px;"><p><b>{2}</b></p><audio controls><source src="{3}"></audio></div>'
                            '<div style="margin: 5px;"><p><b>{4}</b></p><audio controls><source src="{5}"></audio></div>'
                            '<div style="margin: 5px;"><p><b>{6}</b></p><audio controls><source src="{7}"></audio></div>'
                            '<div style="margin: 5px;"><p><b>{8}</b></p><audio controls><source src="{9}"></audio></div>'
                            '<div style="margin: 5px;"><p><b>{10}</b></p><audio controls><source src="{11}"></audio></div>'
                            '<div style="margin: 5px;"><p><b>{12}</b></p><audio controls><source src="{13}"></audio></div>'
                            '<div style="margin: 5px;"><p><b>{14}</b></p><audio controls><source src="{15}"></audio></div></div>'),
                            audio_name[0],
                            audio[0].url,
                            audio_name[1],
                            audio[1].url,
                            audio_name[2],
                            audio[2].url,
                            audio_name[3],
                            audio[3].url,
                            audio_name[4],
                            audio[4].url,
                            audio_name[5],
                            audio[5].url,
                            audio_name[6],
                            audio[6].url,
                            audio_name[7],
                            audio[7].url,
                            )

    showAudio.short_description = 'Uploaded Audios'
    showAudio.allow_tags = True

    def __str__(self):
        return self.name

class QuanMinScreenshot(models.Model):
    inspector = models.ForeignKey(Inspector, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='screenshots/')

    def __str__(self):
        return self.inspector.name

class TranslatedAudio(models.Model):
    inspector = models.ForeignKey(Inspector, default=None, on_delete=models.CASCADE)
    audios = models.FileField(upload_to='audios/')

    def __str__(self):
        return self.inspector.name
