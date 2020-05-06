import django
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import datetime

# Create your models here.
class RulesAndRegulation(models.Model):
    rule = models.TextField(unique=True, default='Insert Rules Here.', editable=True)
    pub_date = models.DateTimeField('Date Added', default=django.utils.timezone.now)
	
    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        
    was_added_recently.admin_order_field = 'pub_date'
    was_added_recently.boolean = True
    was_added_recently.short_description = 'Added recently?'

    def __str__(self):
        return self.rule

class EmergencyContact(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.name
