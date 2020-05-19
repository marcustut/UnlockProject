from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.contrib import messages

import datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .models import MissionDetail, Inspector
from control.models import Control

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
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    'How many buildings are there that looks similarly to each other on the left side of the video?',
    'What colour is the vehicle in front of the lorry?',
    'What is the colour of the car at the opposite of the road?',
    'The first turn was towards which direction?',
    'What is the colour of the gate on the left?',
    '',
]

# functions to be used
def change_tz_kl(mission):
    mission.start_time = mission.start_time.replace(tzinfo=tz)
    return mission


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
        if ans == '0':
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
        if ans.lower() == 'lorry' or ans == '啰哩':
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
        if ans.lower() == 'right' or ans.lower() == 'right side' or ans == '右' or ans == '右边':
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
        if ans == '等待着那句 我愿意' or ans == '等待着那句我愿意' or ans == '等待著那句 我願意' or ans == '等待著那句我願意':
            return True
        else:
            return False
    elif q_no == 2:
        if ans == '做我永远的依靠' or ans == '做我永遠的依靠':
            return True
        else:
            return False
    elif q_no == 3:
        if ans == '我找不到出口':
            return True
        else:
            return False
    elif q_no == 4:
        if ans.lower() == 'let the storm rage on':
            return True
        else:
            return False
    elif q_no == 5:
        if ans == '有换季的颜色' or ans == '有換季的顏色':
            return True
        else:
            return False


@login_required(login_url='login:login')
def home(request):
    return render(request, 'home/home.html')


@method_decorator(login_required(login_url='login:login'), name='dispatch')
class MissionSubmission(View):
    missions = MissionDetail.objects.all().order_by('start_time')
    missions = list(map(change_tz_kl, missions))
    now = Control.objects.all().first().game_time.replace(tzinfo=tz)

    def get(self, request):
        user = Inspector.objects.all().filter(
            user__username__startswith=request.user.username)[0]
        now = Control.objects.all().first().game_time.replace(tzinfo=tz)

        context = {'now': now, 'missions': self.missions, 'user': user, }
        return render(request, 'home/mission.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class Submit(MissionSubmission):
    def get(self, request, mission_id):
        mission = MissionDetail.objects.all().filter(id=mission_id)[0]
        mission = newline_aware(mission)
        user = Inspector.objects.all().filter(
            user__username__startswith=request.user.username)[0]
        now = Control.objects.all().first().game_time
        # now = datetime.datetime(2020, 6, 2, 16).replace(tzinfo=tz)


        if check_mission_completed(user, mission_id):
            return render(request, 'home/locked.html', {'mission': mission, 'condition': 'mission already completed'})
        elif now > mission.start_time and now < mission.end_time:
            if mission_id == 2:
                if user.m2_a == True:
                    return HttpResponseRedirect(reverse('home:audio', args=(mission_id,)))
                else:
                    return render(request, 'home/submit.html', {'mission': mission})
            elif mission.id == 5:
                if user.m5_trials > 0:
                    return render(request, 'home/submit.html', {'mission': mission, 'CarcamQuesChi': CarcamQuesChi, 'CarcamQuesEng': CarcamQuesEng, 'Timecode': Timecode})
                else:
                    return render(request, 'home/locked.html', {'mission': mission, 'numTrials': 10 - user.m5_trials, 'condition': 'ran out of trials'})
            else:
                return render(request, 'home/submit.html', {'mission': mission})
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
        now = Control.objects.all().first().game_time
        # now = datetime.datetime(2020, 6, 2, 16).replace(tzinfo=tz)

        # Try submit answer
        # try:
        if mission_id == 1:
            # Password JS Box
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
                # Set time-attack rule
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

                user.m1 = True
                user.save()
            else:
                messages.error(
                    request, "Your answer(s) is incorrect, please check again.")
                return render(request, 'home/submit.html', context)

        elif mission_id == 2:
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
                    # Set time-attack rule
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

                    user.m2_a = True
                    user.save()
                    return HttpResponseRedirect(reverse('home:audio', args=(mission_id,)))
                else:
                    messages.error(
                        request, "Your answer(s) is incorrect, please check again.")
                    return render(request, 'home/submit.html', context)

        elif mission_id == 3:
            # Handle File Uploads
            uploaded_file = request.FILES['filename']

            uploaded_file.name = f'{user.name} ({user.satellite})'
            print(uploaded_file.name)
            print(uploaded_file.size)
            print(uploaded_file.temporary_file_path())
            print(uploaded_file.content_type)
            print(now-mission.start_time)

            file_metadata = {'name': uploaded_file.name, 'parents': [
                '1aTq0ixgl0-0FVbACGsgB1sXDdVBxcqFw']}
            media = MediaFileUpload(uploaded_file.temporary_file_path(),
                                    mimetype=uploaded_file.content_type)
            file = drive.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

        elif mission_id == 4:
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
                # Set time-attack rule
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

                user.m4 = True
                user.save()
            else:
                messages.error(
                    request, "Your answer(s) is incorrect, please check again.")
                return render(request, 'home/submit.html', context)

        elif mission_id == 5:
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
                # Set time-attack rule
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
        else:
            # Finale Escape Game
            pass
        return render(request, 'home/success.html', {'user': user, 'mission': mission})
        # except:
        #     return render(request, 'home/error.html', {'cg': user.pastoral_cg, 'mission': mission})


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
    now = Control.objects.all().first().game_time

    if request.method == 'GET':
        if user.m2_a == True and user.m2_b == True:
            return render(request, 'home/locked.html', {'mission': mission, 'condition': 'mission already completed'})
        elif user.m2_a == True:
            return render(request, 'home/audio.html')
        else:
            return HttpResponseRedirect(reverse('home:submit', args=(mission_id,)))
        
    elif request.method == 'POST':
        # Handle File Uploads
        uploaded_file = request.FILES['filename']

        uploaded_file.name = f'{user.name} ({user.satellite})'
        print(uploaded_file.name)
        print(uploaded_file.size)
        print(uploaded_file.temporary_file_path())
        print(uploaded_file.content_type)
        print(now-mission.start_time)
        # Limit file size to be at max 5MB
        if uploaded_file.size > 5242880:
            messages.warning(
                request, "Your file has exceeded the 5MB limit. Please upload a smaller file.")
            return render(request, 'home/submit.html', {'mission': mission})
        else:
            file_metadata = {'name': uploaded_file.name, 'parents': [
                '1m1VPLAaBG5ZcacuyvoPGWfSxvNznyYHP']}
            media = MediaFileUpload(uploaded_file.temporary_file_path(),
                                    mimetype=uploaded_file.content_type)
            file = drive.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

@login_required(login_url='login:login')
def crossword(request, mission_id):
    mission = MissionDetail.objects.all().filter(id=mission_id)[0]
    mission = newline_aware(mission)
    user = Inspector.objects.all().filter(
        user__username__startswith=request.user.username)[0]
    now = Control.objects.all().first().game_time

    if request.method == "GET":
        if mission_id == 4:
            return render(request, 'home/crossword.html', {'user': user, 'mission': mission})
        else:
            return render(request, 'home/error.html', {'cg': user.pastoral_cg, 'mission': mission})
    elif request.method == "POST":

        return render(request, 'home/error.html', {'cg': user.pastoral_cg, 'mission': mission})
    else:
        return render(request, 'home/error.html', {'cg': user.pastoral_cg, 'mission': mission})
