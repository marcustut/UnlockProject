from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Ranking(models.Model):
    pass

class MissionDetails(models.Model):
    pass

class MissionSchedule(models.Model):
    pass

class RulesAndRegulations(models.Model):
    pass

class EmergencyContact(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.name