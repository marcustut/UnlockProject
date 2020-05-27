from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.forms import modelform_factory
from django.utils import timezone

import datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .models import MissionDetail, Inspector, QuanMinScreenshot
from control.models import Control
from .forms import ScreenshotForm

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from googleapiclient.http import MediaFileUpload
# Create your views here.

# # time info
tz = pytz.timezone('Asia/Kuala_Lumpur')
# now = Control.objects.all().first().game_time.replace(tzinfo=tz)

# Google Drive Info
# define path variables
credentials_file_path = 'home/credentials/credentials.json'
clientsecret_file_path = 'home/credentials/client_secret.json'

# define API scope
SCOPE = 'https://www.googleapis.com/auth/drive'

# define store
store = file.Storage(credentials_file_path)
credentials = store.get()

# get access token
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(clientsecret_file_path, SCOPE)
    flags = tools.argparser.parse_args(args=[])
    credentials = tools.run_flow(flow, store, flags)

# define API service
http = credentials.authorize(Http())
drive = discovery.build('drive', 'v3', http=http)

# Game Global Variables
# Carcam Question
Timecode = [
    '',
    '',
    '4:02',
    '',
    '',
    '3:48',
    '',
    '',
    '4:23 - 4:24',
    '',
    '',
    '',
    '2:29',
    '3:30',
    '0:30 - 0:39',
    '1:18',
    '1:27',
    '',
    '1:25',
    '4:30',
]
CarcamQuesChi = [
    ('', '一路上有多少个红绿灯？'),
    ('', '一路上一共有多少个摩托车骑士？'),
    ('4:02', '左边在同步直行的车是什么车？'),
    ('', '一共拐了多少个左？'),
    ('', '一共拐了多少个右？'),
    ('3:48', '左边的店的英文全名？（tip: XXX xxxxxxx (XX) SDN. BHD）'),
    ('', '一共经过了多少个bump?'),
    ('', '最后一个拐的方向是？'),
    ('4:23 - 4:24', '左边一共有多少辆车在parking着？'),
    ('', '有一个banner写着SAFETY FIRST, 接下一句'),
    ('', '第三个拐的方向是？'),
    ('', '在哪一分钟哪一秒可以看见3Q的招牌？(eg. 1:27)（tip: 注意左边）'),
    ('2:29', '迎面而来的车想要转的方向是？'),
    ('3:30', '迎面而来的车是什么颜色？'),
    ('0:30 - 0:39', '左边有多少个架构相识的建筑物？'),
    ('1:18', '啰哩前面的车是什么颜色'),
    ('1:27', '迎面而来的车是什么颜色？'),
    ('', '第一个拐的方向'),
    ('1:25', '左边的铁门是什么颜色？'),
    ('4:30', '有辆车转向左还是右？'),
]
CarcamQuesEng = [
    'How many red lights are there throughout the entire journey?',
    'In the entire journey how many motorcyclists are there?',
    'In <kbd>4:02</kbd>, what is the car model on the left?',
    'How many times did the driver turn left in the journey?',
    'How many times did the driver turn right in the journey?',
    'In <kbd>3:48</kbd>, what is the name of the shop on the left? (Tip: XXX xxxxxxx (XX) SDN. BHD)',
    'How many bumps have the driver passed by?',
    'Which is the last turn made by the driver?',
    'In <kbd>4:23 – 4:24</kbd>, how many cars are parking at the left side of the road?',
    'There is a banner written “SAFETY FIRST”, please continue the next sentence.',
    'What is the third turn that was made by the driver?',
    'At which specific time frame can you see the 3Q signboard?',
    'In <kbd>2:29</kbd>, the car that is coming towards the screen is heading to which direction?',
    'In <kbd>3:30</kbd>, what colour is the car that is coming towards the screen?',
    'How many buildings are there that looks similarly to each other on the left side of the video??',
    'What colour is the vehicle in front of the lorry? ',
    'What is the colour of the car at the opposite of the road?',
    'The first turn was towards which direction?',
    'What is the colour of the gate on the left?',
    'In <kbd>4:30</kbd>, what direction is the other car turning in to?',
]

# functions to be used
def newline_aware(mission):
    mission.mission_description_chi = mission.mission_description_chi.replace(
        '\n', '<br>')
    mission.mission_description_eng = mission.mission_description_eng.replace(
        '\n', '<br>')
    return mission


def check_mission_completed(user, mission_id):
    if mission_id == 1:
        return user.m1
    elif mission_id == 2:
        return user.m2_a and user.m2_b
    elif mission_id == 3:
        return user.m3
    elif mission_id == 4:
        return user.m4
    elif mission_id == 5:
        return user.m5
    else:
        return user.m6

def check_spot_ans(ans, q_no):
    if q_no == 1:
        if ans == '1':
            return True
        else:
            return False
    elif q_no == 2:
        if ans == '1':
            return True
        else:
            return False
    elif q_no == 3:
        if ans == '1':
            return True
        else:
            return False
    elif q_no == 4:
        if ans == '5':
            return True
        else:
            return False

def check_carcam_ans(ans, q_no):
    if q_no == 1:
        if ans == '2' or ans.lower() == 'two' or ans == '二':
            return True
        else:
            return False
    elif q_no == 2:
        if ans == '21' or ans.lower() == 'twenty one' or ans == '二十一':
            return True
        else:
            return False
    elif q_no == 3:
        if ans.lower() == 'lorry' or ans.lower() == 'white lorry' or ans == '啰哩' or ans == '货车' or ans == '卡车' or ans == '白色啰哩' or ans == '白色货车' or ans == '白色卡车':
            return True
        else:
            return False
    elif q_no == 4:
        if ans == '5' or ans.lower() == 'five' or ans == '五':
            return True
        else:
            return False
    elif q_no == 5:
        if ans == '1' or ans.lower() == 'one' or ans == '一':
            return True
        else:
            return False
    elif q_no == 6:
        answers = [
            'yhl trading (kl) sdn bhd',
            'yhl trading (kl) sdn.bhd',
            'yhl trading (kl) sdn. bhd',
            'yhl trading (kl) sdn.bhd.',
            'yhl trading (kl) sdn. bhd.',
            'yhl trading (k.l) sdn bhd',
            'yhl trading (k.l) sdn.bhd',
            'yhl trading (k.l) sdn. bhd',
            'yhl trading (k.l) sdn.bhd.',
            'yhl trading (k.l) sdn. bhd.',
            'yhl trading (k.l.) sdn bhd',
            'yhl trading (k.l.) sdn.bhd',
            'yhl trading (k.l.) sdn. bhd',
            'yhl trading (k.l.) sdn.bhd.',
            'yhl trading (k.l.) sdn. bhd.',
        ]
        if ans.lower() in answers:
            return True
        else:
            return False
    elif q_no == 7:
        if ans == '5' or ans.lower() == 'five' or ans == '五':
            return True
        else:
            return False
    elif q_no == 8:
        if ans.lower() == 'right' or ans.lower() == 'right side' or ans.lower() == 'turn right' or ans.lower() == 'right turn' or ans.lower() == 'to the right' or ans == '右' or ans == '右边':
            return True
        else:
            return False
    elif q_no == 9:
        if ans == '7' or ans.lower() == 'seven' or ans == '七':
            return True
        else:
            return False
    elif q_no == 10:
        if ans.lower() == 'keep this place clean and orderly':
            return True
        else:
            return False
    elif q_no == 11:
        if ans.lower() == 'left' or ans.lower() == 'left side' or ans == '左' or ans == '左边':
            return True
        else:
            return False
    elif q_no == 12:
        if ans == '4:46' or ans == '4:45' or ans == '4:47':
            return True
        else:
            return False
    elif q_no == 13:
        if ans.lower() == 'left' or ans.lower() == 'left side' or ans == '左' or ans == '左边':
            return True
        else:
            return False
    elif q_no == 14:
        if ans == '白' or ans == '白色' or ans.lower() == 'white' or ans.lower() == 'white color':
            return True
        else:
            return False
    elif q_no == 15:
        if ans == '3' or ans.lower() == 'three' or ans == '三':
            return True
        else:
            return False
    elif q_no == 16:
        if ans == '黑' or ans == '黑色' or ans.lower() == 'black' or ans.lower() == 'black color':
            return True
        else:
            return False
    elif q_no == 17:
        if ans == '白' or ans == '白色' or ans.lower() == 'white' or ans.lower() == 'white color':
            return True
        else:
            return False
    elif q_no == 18:
        if ans.lower() == 'left' or ans.lower() == 'left side' or ans == '左' or ans == '左边':
            return True
        else:
            return False
    elif q_no == 19:
        if ans == '蓝' or ans == '蓝色' or ans.lower() == 'blue' or ans.lower() == 'blue color':
            return True
        else:
            return False
    elif q_no == 20:
        if ans.lower() == 'right' or ans.lower() == 'right side' or ans == '右' or ans == '右边':
            return True
        else:
            return False
    else:
        return 'Wrong Question Number.'


def check_crossword_ans(ans, q_no):
    if q_no == 1:
        if ans == 'idyllic':
            return True
        else:
            return False
    elif q_no == 2:
        if ans == 'schizophrenia':
            return True
        else:
            return False
    elif q_no == 3:
        if ans == 'quixotic':
            return True
        else:
            return False
    elif q_no == 4:
        if ans == 'glockenspiel':
            return True
        else:
            return False
    elif q_no == 5:
        if ans == 'eidos':
            return True
        else:
            return False
    elif q_no == 6:
        if ans == 'mississippi':
            return True
        else:
            return False
    elif q_no == 7:
        if ans == 'sgraffito':
            return True
        else:
            return False
    elif q_no == 8:
        if ans == 'zaftig':
            return True
        else:
            return False
    elif q_no == 9:
        if ans == 'paraphernalia':
            return True
        else:
            return False
    elif q_no == 10:
        if ans == 'larynx':
            return True
        else:
            return False

def check_song_ans(ans, q_no):
    if q_no == 1:
        if ans == '推理爱情 最难解的谜' or ans == '推理爱情最难解的谜' or ans == '推理愛情 最難解的謎' or ans == '推理愛情最難解的謎' or ans.lower() == 'then you take my hand' or ans.lower() == 'thenyoutakemyhand':
            return True
        else:
            return False
    elif q_no == 2:
        if ans == '做我永远的依靠' or ans == '做我永遠的依靠' or ans.lower() == 'i think your love would be too much' or ans.lower() == 'ithinkyourlovewouldbetoomuch':
            return True
        else:
            return False
    elif q_no == 3:
        if ans == '我找不到出口' or ans.lower() == 'why don\'t you say so' or ans.lower() == 'why dont you say so' or ans.lower() == 'whydontyousayso' or ans.lower() == 'whydon\'tyousayso':
            return True
        else:
            return False
    elif q_no == 4:
        if ans.lower() == 'let the storm rage on' or ans.lower() == 'letthestormrageon':
            return True
        else:
            return False
    elif q_no == 5:
        if ans == '我希望你快乐' or ans == '我希望你快樂' or ans == '我想给你快乐' or ans == '我想給你快樂' or ans.lower() == 'and you let it burn' or ans.lower() == 'andyouletitburn':
            return True
        else:
            return False

def time_attack_rule(time_used):
    pass


@login_required(login_url='login:login')
def home(request):
    return render(request, 'home/home.html')


@method_decorator(login_required(login_url='login:login'), name='dispatch')
class MissionSubmission(View):
    missions = MissionDetail.objects.all().order_by('start_time')

    def get(self, request):
        user = Inspector.objects.all().filter(
            user__username__startswith=request.user.username)[0]
        now = datetime.datetime.now().astimezone()

        context = {'now': now, 'missions': self.missions, 'user': user,}
        return render(request, 'home/mission.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class Submit(MissionSubmission):
    ScreenshotFormSet = modelform_factory(QuanMinScreenshot, form=ScreenshotForm, error_messages="Error Occured")

    def get(self, request, mission_id):
        mission = MissionDetail.objects.all().filter(id=mission_id)[0]
        mission = newline_aware(mission)
        user = Inspector.objects.all().filter(
            user__username__startswith=request.user.username)[0]
        now = datetime.datetime.now().astimezone()
        
        form = ScreenshotForm(instance=request.user)

        # return render(request, 'home/submit.html', {'mission':mission, 'CarcamQuesChi': CarcamQuesChi, 'CarcamQuesEng': CarcamQuesEng, 'Timecode': Timecode})

        if check_mission_completed(user, mission_id):
            return render(request, 'home/locked.html', {'mission': mission, 'condition': 'mission already completed'})
        elif now >= mission.start_time and now <= mission.end_time:
            if mission_id == 1:
                if user.m1_trials > 0:
                    return render(request, 'home/submit.html', {'mission': mission})
                else:
                    return render(request, 'home/locked.html', {'mission': mission, 'numTrials': 10 - user.m1_trials, 'condition': 'ran out of trials'})
            elif mission_id == 2:
                if user.m2_a == True:
                    return HttpResponseRedirect(reverse('home:audio', args=(mission_id,)))
                else:
                    return render(request, 'home/submit.html', {'mission': mission})
            elif mission_id == 5:
                if user.m5_trials > 0:
                    return render(request, 'home/submit.html', {'mission': mission, 'CarcamQuesChi': CarcamQuesChi, 'CarcamQuesEng': CarcamQuesEng, 'Timecode': Timecode})
                else:
                    return render(request, 'home/locked.html', {'mission': mission, 'numTrials': 10 - user.m5_trials, 'condition': 'ran out of trials'})
            else:
                return render(request, 'home/submit.html', {'mission': mission, 'form': form,})
        elif now > mission.start_time:
            return render(request, 'home/locked.html', {'mission': mission, 'condition': 'time limit exceeded'})
        else:
            return render(request, 'home/locked.html', {'mission': mission, 'condition': 'mission in future'})

    def post(self, request, mission_id):
        request.upload_handlers = [TemporaryFileUploadHandler(request=request)]
        return self._post(request, mission_id)

    @method_decorator(csrf_protect)
    def _post(self, request, mission_id):
        # Taking models
        mission = MissionDetail.objects.all().filter(id=mission_id)[0]
        mission = newline_aware(mission)
        user = Inspector.objects.all().filter(
            user__username__startswith=request.user.username)[0]
        now = datetime.datetime.now().astimezone()

        # Try submit answer
        try:
            if mission_id == 1:
                # Check if user ran out of trials
                if user.m1_trials <= 0:
                    return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))

                # Check if time is up
                if now >= mission.end_time:
                    return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))

                time_used = now - mission.start_time

                SpotAnswers = [request.POST.get(f'box{i+1}') for i in range(0, 4)]
                SpotResults = [check_spot_ans(SpotAnswers[x], (x+1)) for x in range(0, 4)]

                # Validate answers
                if False not in SpotResults:
                    _pass = True
                else:
                    _pass = False

                # Pass the variables
                context = {
                    'mission': mission,
                    'SpotAnswers' : SpotAnswers,
                    'SpotResults': SpotResults,
                }

                if _pass:
                    # Achivement Points System (Add 50 Points if passed)
                    user.points += 50
                    # Register time used to complete the mission
                    user.m1_time_used = time_used

                    user.m1 = True
                    user.m1_trials -= 1
                    user.save()
                else:
                    user.m1_trials -= 1
                    user.save()

                    # Check if user ran out of trials
                    if user.m1_trials <= 0:
                        return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))

                    messages.error(
                        request, f"Your answer(s) is incorrect, please check again.<p style='margin: 0; font-size: x-large;'><b>{user.m1_trials} trials left.</b></p>")
                    return render(request, 'home/submit.html', context)

            elif mission_id == 2:
                # Check if time is up
                if now >= mission.end_time:
                    return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))

                # Check if first part is done
                if user.m2_a == True:
                    return HttpResponseRedirect(reverse('home:audio', args=(mission_id,)))
                else:
                    time_used = now - mission.start_time

                    # Get user input
                    SongAnswers = [request.POST.get(f'audioInput{i+1}').strip() for i in range(0, 5)]
                    SongResults = [check_song_ans(SongAnswers[x], (x+1)) for x in range(0,5)]

                    # Validate answers
                    if False not in SongResults:
                        _pass = True
                    else:
                        _pass = False

                    # Pass the variables
                    context = {
                        'mission': mission,
                        'SongAnswers': SongAnswers,
                        'SongResults': list(map(str, SongResults)),
                    }

                    if _pass:
                        # Achivement Points System (Add 25 Points if passed)
                        user.points += 25

                        # Register time used to complete Part A
                        user.m2_a_time_used = time_used
                        # Set Part A mission complete to True
                        user.m2_a = True

                        user.save()
                        return HttpResponseRedirect(reverse('home:audio', args=(mission_id,)))
                    else:
                        messages.error(
                            request, "Your answer(s) is incorrect, please check again.")
                        return render(request, 'home/submit.html', context)

            elif mission_id == 3:
                # Check if user ran out of trials
                if user.m5_trials <= 0:
                    return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))

                # Check if time is up
                if now >= mission.end_time:
                    return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))

                # Carcam Form
                time_used = now - mission.start_time

                CarcamAnswers = [request.POST.get(f'inputQ{i+1}').strip() for i in range(0,20)]
                CarcamResults = [check_carcam_ans(CarcamAnswers[x], (x+1)) for x in range(0, 20)]

                # Validate answers
                if False not in CarcamResults:
                    _pass = True
                else:
                    _pass = False

                # Pass the variables
                context = {
                    'mission': mission,
                    'CarcamResults': list(map(str, CarcamResults)),
                    'CarcamAnswers' : CarcamAnswers,
                    'CarcamQuesChi': CarcamQuesChi,
                    'CarcamQuesEng': CarcamQuesEng,
                    'Timecode': Timecode,
                }

                if _pass:
                    # Set time-attack rule (Need to WORK on)
                    if time_used < datetime.timedelta(minutes=10):
                        user.points += 5
                    elif time_used < datetime.timedelta(minutes=20):
                        user.points += 4
                    elif time_used < datetime.timedelta(minutes=30):
                        user.points += 3
                    elif time_used < datetime.timedelta(minutes=40):
                        user.points += 2
                    else:
                        user.points += 1

                    # Register time used to complete mission
                    user.m5_time_used = time_used
                    # Set mission complete to True
                    user.m5 = True
                    user.save()
                else:
                    user.m5_trials -= 1
                    user.save()
                    # Check if user ran out of trials
                    if user.m5_trials <= 0:
                        return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))

                    messages.error(
                        request, f"Your answer(s) is incorrect, please check again.<p style='margin: 0; font-size: x-large;'><b>{user.m5_trials} trials left.</b></p>")
                    return render(request, 'home/submit.html', context)

            elif mission_id == 4:
                # Check if time is up
                if now >= mission.end_time:
                    return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))

                # Crossword JS Box
                time_used = now - mission.start_time

                CrosswordAnswers = [request.POST.get(f'crosswordQ{i+1}').strip().lower() for i in range(0, 10)]
                CrosswordResults = [check_crossword_ans(CrosswordAnswers[x], (x+1)) for x in range(0, 10)]

                if False not in CrosswordResults:
                    _pass = True
                else:
                    _pass = False

                context = {
                    'mission': mission,
                    'CrosswordAnswers': CrosswordAnswers,
                    'CrosswordResults': list(map(str, CrosswordResults)),
                }

                if _pass:
                    # Set time-attack rule (Need to WORK on)
                    if time_used < datetime.timedelta(minutes=10):
                        user.points += 5
                    elif time_used < datetime.timedelta(minutes=20):
                        user.points += 4
                    elif time_used < datetime.timedelta(minutes=30):
                        user.points += 3
                    elif time_used < datetime.timedelta(minutes=40):
                        user.points += 2
                    else:
                        user.points += 1

                    # Register time used to complete mission
                    user.m4_time_used = time_used
                    # Set mission complete to True
                    user.m4 = True
                    user.save()
                else:
                    messages.error(
                        request, "Your answer(s) is incorrect, please check again.")
                    return render(request, 'home/submit.html', context)

            elif mission_id == 5:
                # Check if time is up
                if now >= mission.end_time:
                    return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))

                if len(request.FILES) != 8:
                    messages.error(request, "You have not selected all 8 screenshots, please check again.")
                    return render(request, 'home/submit.html', {'mission': mission})
                else:
                    response_data = {}

                    if request.POST.get('action') == 'QuanMinScreenshot':
                        screenshots = [request.FILES.get(f'QuanMin{i+1}') for i in range(8)]

                        response_data['screenshots'] = screenshots

                        for i in range(len(screenshots)):
                            inspectorScreenshot = QuanMinScreenshot(inspector=request.user.inspector, images=screenshots[i])
                            inspectorScreenshot.save()
                        
                        return JsonResponse(response_data)
            else:
                # Finale Escape Game
                pass
            return render(request, 'home/success.html', {'user': user, 'mission': mission})
        except:
            return render(request, 'home/error.html', {'cg': user.pastoral_cg, 'mission': mission})


# Games
@login_required(login_url='login:login')
def spot(request, mission_id):
    return render(request, 'home/spot.html')

@login_required(login_url='login:login')
def audio(request, mission_id):
    mission = MissionDetail.objects.all().filter(id=mission_id)[0]
    mission = newline_aware(mission)
    user = Inspector.objects.all().filter(
        user__username__startswith=request.user.username)[0]
    now = datetime.datetime.now().astimezone()

    if request.method == 'GET':
        if user.m2_a == True and user.m2_b == True:
            return render(request, 'home/locked.html', {'mission': mission, 'condition': 'mission already completed'})
        elif user.m2_a == True:
            return render(request, 'home/audio.html')
        else:
            return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))
        
    elif request.method == 'POST':
        # Check if time is up
        if now >= mission.end_time:
            return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))

        # Check if user has uploaded all 8 audios
        if len(request.FILES) != 8:
            messages.error(request, "You have not selected all 8 audios, please check again.")
            return render(request, 'home/audio.html', {'mission': mission})
        else:
            # Calculate time used to pass the mission
            time_used = now - mission.start_time

            # Storing logic
            uploaded_audios = [request.FILES.get('translatedAudio' + str(i+1)) for i in range(8)]
            file_name_list = ['泰语_Thai', ' 德语_German', '日语_Japanese', '俄语_Russian', '淡米尔文_Tamil', '葡萄牙语_Portugese', '韩语_Korean', '法文_French']

            extension_list_2 = ['.au']
            extension_list_3 = ['.mp3', '.wav', '.ogg', '.aac', '.m4a', '.wma', '.mid', '.oga', '.amr', '.mp4']
            extension_list_4 = ['.flac', '.opus', '.webm', '.weba', '.aiff', '.mpeg', '.3gpp']

            try:
                # Renaming
                for i in range(len(uploaded_audios)):
                    if uploaded_audios[i].name[-5:] in extension_list_4:
                        uploaded_audios[i].name = file_name_list[i] + uploaded_audios[i].name[-5:]
                    elif uploaded_audios[i].name[-4:] in extension_list_3:
                        uploaded_audios[i].name = file_name_list[i] + uploaded_audios[i].name[-4:]
                    elif uploaded_audios[i].name[-3:] in extension_list_2:
                        uploaded_audios[i].name = file_name_list[i] + uploaded_audios[i].name[-3:]
                    else:
                        messages.error(request, '<p>Possible Causes of Error:<br>1. You are uploading video files instead of audio files.(eg. .mp4 or .mpeg)<br>2. Slow internet connection.(try uploading again)</p>')
                        return render(request, 'home/error.html', {'mission': mission})
            except:
                messages.error(request, '<p>Possible Causes of Error:<br>1. You are uploading video files instead of audio files.(eg. .mp4 or .mpeg)<br>2. Slow internet connection.(try uploading again)</p>')
                return render(request, 'home/error.html', {'mission': mission})

            # Writing uploaded files to database
            user.m2_b_audio1 = uploaded_audios[0]
            user.m2_b_audio2 = uploaded_audios[1]
            user.m2_b_audio3 = uploaded_audios[2]
            user.m2_b_audio4 = uploaded_audios[3]
            user.m2_b_audio5 = uploaded_audios[4]
            user.m2_b_audio6 = uploaded_audios[5]
            user.m2_b_audio7 = uploaded_audios[6]
            user.m2_b_audio8 = uploaded_audios[7]

            # Achivement Points System (Add 25 Points if passed)
            # user.points += 25

            # Register time used to complete Part A
            user.m2_b_time_used = time_used

            # Set Part A mission complete to True
            # user.m2_b = True
            user.save()

            return render(request, 'home/pending.html', {'user': user, 'mission': mission})
            

@login_required(login_url='login:login')
def crossword(request, mission_id):
    mission = MissionDetail.objects.all().filter(id=mission_id)[0]
    mission = newline_aware(mission)
    user = Inspector.objects.all().filter(
        user__username__startswith=request.user.username)[0]
    # now = Control.objects.all().first().game_time
    now = timezone.now().replace(tzinfo=tz)

    if request.method == "GET":
        if mission_id == 4:
            return render(request, 'home/crossword.html', {'user': user, 'mission': mission})
        else:
            return render(request, 'home/error.html', {'cg': user.pastoral_cg, 'mission': mission})
    elif request.method == "POST":

        return render(request, 'home/error.html', {'cg': user.pastoral_cg, 'mission': mission})
    else:
        return render(request, 'home/error.html', {'cg': user.pastoral_cg, 'mission': mission})

def error_404_view(request, exception):
    return render(request, 'home/error404.html')

def error_500_view(request):
    return render(request, 'home/error500.html')