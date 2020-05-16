# Django
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from django.shortcuts import render, redirect

# Twilio
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# Python Modules
import datetime

# Credentials
from .credentials.twilio_cred import account_sid, auth_token

# Models
from .models import *

# Global Variables
client = Client(account_sid, auth_token)

# Class-based views
@method_decorator(csrf_exempt, name='dispatch')
class WhatsAppInfoboard(View):
    def get(self, request):
        return HttpResponse('Use our WhatsApp Bot!')

    def post(self, request):
        # Setting Variables
        incoming_msg = request.POST.get('Body', '')
        resp = MessagingResponse()
        msg = resp.message()
        currentDT = datetime.datetime.now().strftime("_%a, %d-%m-%Y, %I:%M:%S%p_")

        # Main Menu
        if incoming_msg == '0' or incoming_msg == '🔢':
            msg.body(f'*欢迎来到《绝密追查》社交媒体多人连线游戏*\n{currentDT}\n\n_*Reply with the number below(or emoji)*_\n\n1. Show the latest Ranking 📊️\n2. Mission Details 🗒️\n3. Mission Schedule ⌛\n4. Rules and Regulations ⛔\n5. Emergency Contact 📞\n0. Main Menu 🔢')

        # Ranking
        if incoming_msg == '1' or incoming_msg == '📊️':
            msg.body(f'This feature is under development.')

        # Mission Details
        if incoming_msg == '2' or incoming_msg == '🗒️':
            msg_MissionDetail = f'*Mission Details 🗒️*\n\n'
            idx = 1
            for mission in MissionDetail.objects.all().order_by('start_time'):
                mission_detail_msg = f'*{idx}. {mission.mission_title}*\n_{mission.mission_description}_\nStart Time: {timezone.localtime(mission.start_time).strftime("_%a, %d-%m-%Y, %I:%M:%S%p_")}\nEnd Time: {timezone.localtime(mission.end_time).strftime("_%a, %d-%m-%Y, %I:%M:%S%p_")}\n\n'
                msg_MissionDetail += mission_detail_msg
                idx += 1
            
            msg.body(msg_MissionDetail)

        # Mission Schedule
        if incoming_msg == '3' or incoming_msg == '⌛':
            msg_MissionSchedule = f'*Mission Schedule ⌛*\n\n'
            mission_schedule_msg1 = f'*Week 1: 23/5(Saturday) - 29/5(Friday)*\n'
            mission_schedule_msg3 = f'\n*Week 2: 30/5(Saturday) - 05/6(Friday)*\n'

            start_date = datetime.date(2020, 5, 23)
            end_date = datetime.date(2020, 5, 29)
            date_delta = datetime.timedelta(days=1)
            
            msg_MissionSchedule += mission_schedule_msg1

            while start_date <= end_date:
                mission_schedule_msg2 = f'{start_date.strftime("%A (%d/%-m)")} - '
                schedule = [obj for obj in MissionDetail.objects.all() if obj.check_date(start_date.year, start_date.month, start_date.day) == True]
                if schedule != []:
                    if len(schedule) > 1:
                        for x in schedule:
                            mission_schedule_msg2 += f'*{x.mission_title}* & '
                        mission_schedule_msg2 = mission_schedule_msg2[:-3]
                        mission_schedule_msg2 += '\n'
                    else:
                        mission_schedule_msg2 += f'*{schedule[0].mission_title}*\n'
                else:
                    mission_schedule_msg2 += '_No Mission_\n'
                msg_MissionSchedule += mission_schedule_msg2
                print(schedule)
                start_date += date_delta

            end_date = datetime.date(2020, 6, 5)
            msg_MissionSchedule += mission_schedule_msg3

            while start_date <= end_date:
                mission_schedule_msg2 = f'{start_date.strftime("%A (%d/%-m)")} - '
                schedule = [obj for obj in MissionDetail.objects.all() if obj.check_date(start_date.year, start_date.month, start_date.day) == True]
                if schedule != []:
                    if len(schedule) > 1:
                        for x in schedule:
                            mission_schedule_msg2 += f'*{x.mission_title}* & '
                        mission_schedule_msg2 = mission_schedule_msg2[:-3]
                        mission_schedule_msg2 += '\n'
                    else:
                        mission_schedule_msg2 += f'*{schedule[0].mission_title}*\n'
                else:
                    mission_schedule_msg2 += '_No Mission_\n'
                msg_MissionSchedule += mission_schedule_msg2
                
                start_date += date_delta
            
            msg.body(msg_MissionSchedule)

        # Rules and Regulation
        if incoming_msg == '4' or incoming_msg == '⛔':
            msg_RulesAndRegulation = f'*Rules and Regulations ⛔*\n\n'
            idx = 1
            for rule in RulesAndRegulation.objects.all():
                rule_msg = f'{idx}. {rule.rule}\n'
                msg_RulesAndRegulation += rule_msg
                idx += 1

            msg.body(msg_RulesAndRegulation)

        # Emergency Contact
        if incoming_msg == '5' or incoming_msg == '📞':
            msg_EmergencyContact = f'*Emergency Contact 📞*\n_Contact only if there is any enquiries on games or rules and regulations._\n\n'
            for contact in EmergencyContact.objects.all():
                contact_msg = f'{contact.name} {contact.phone_number}\n'
                msg_EmergencyContact += contact_msg
            
            msg.body(msg_EmergencyContact)

        return HttpResponse(str(resp))

def infoboard(request):
    return render(request, 'infoboard/infoboard.html')