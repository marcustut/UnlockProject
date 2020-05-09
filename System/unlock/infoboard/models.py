import django
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import datetime

# Create your models here.
class RulesAndRegulation(models.Model):
    rule_chi = models.TextField(unique=True, default='输入游戏规则')
    rule_eng = models.TextField(unique=True, default='Insert Rules Here.')
    pub_date = models.DateTimeField('Date Added', default=django.utils.timezone.now)
	
    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        
    was_added_recently.admin_order_field = 'pub_date'
    was_added_recently.boolean = True
    was_added_recently.short_description = 'Added recently?'

    def __str__(self):
        return self.rule_chi + ' ' + self.rule_eng

class EmergencyContact(models.Model):
    name_chi = models.CharField(max_length=200, default='输入联络人名字')
    name_eng = models.CharField(max_length=200, default='Insert English Name Here.')
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.name_chi + ' ' + self.name_eng
