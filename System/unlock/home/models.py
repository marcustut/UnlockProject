from django.db import models
from django import forms
from django.utils import timezone
import datetime
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

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
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.start_time <= now

    nearest_mission.admin_order_field = 'start_time'
    nearest_mission.boolean = True
    nearest_mission.short_description = 'Today\'s Mission'

    def __str__(self):
        return self.mission_title_chi + ' ' + self.mission_title_eng

class Inspector(models.Model):
    SATELLITE_CHOICES = [
        ('KL', 'Kuchai Lama'),
        ('PUC', 'Puchong'),
        ('STP', 'Setapak'),
        ('RW', 'Rawang'),
        ('PJ', 'Petaling Jaya'),
        ('USJ', 'UEP Subang Jaya'),
        ('KLG', 'Klang'),
        ('KP', 'Kepong'),
        ('SB', 'Seremban'),
        ('SD', 'Serdang'),
        ('KJ', 'Kajang'),
        ('SGL', 'Sungai Long'),
    ]

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, default="+60")
    satellite = models.CharField(max_length=200, choices=SATELLITE_CHOICES)
    pastoral_team = models.CharField(max_length=200)
    pastoral_cg = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    m1 = models.BooleanField(verbose_name='m1 completed', default=False)
    m2 = models.BooleanField(verbose_name='m2 completed', default=False)
    m3 = models.BooleanField(verbose_name='m3 completed', default=False)
    m4 = models.BooleanField(verbose_name='m4 completed', default=False)
    m5 = models.BooleanField(verbose_name='m5 completed', default=False)
    m6 = models.BooleanField(verbose_name='m6 completed', default=False)

    def __str__(self):
        return self.name