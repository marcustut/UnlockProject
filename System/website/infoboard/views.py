# Django
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

# Twilio
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# Python Modules
import datetime

# Credentials
from .credentials.twilio_cred import account_sid, auth_token

# Models
from .models import EmergencyContact

# Global Variables
client = Client(account_sid, auth_token)

# Class-based views
@method_decorator(csrf_exempt, name='dispatch')
class InfoBoard(View):
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
            msg.body(f'This feature is under development.')

        # Timeline
        if incoming_msg == '3' or incoming_msg == '⌛':
            msg.body(f'This feature is under development.')

        # Rules and Regulation
        if incoming_msg == '4' or incoming_msg == '⛔':
            msg.body(f'This feature is under development.')

        # Emergency Contact
        if incoming_msg == '5' or incoming_msg == '📞':
            msg_template = f'*Emergency Contact 📞*\n_Contact only if there is any enquiries on games or rules and regulations._\n\n'
            for contact in EmergencyContact.objects.all():
                contact_msg = f'{contact.name} {contact.phone_number}\n'
                msg_template += contact_msg
            
            msg.body(msg_template)

        return HttpResponse(str(resp))
