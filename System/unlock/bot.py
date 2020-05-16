# Discrod import
import discord
from discord.ext import commands

# Setting Django environment
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'unlock.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'
django.setup()

# Django imports
from home.models import MissionDetail
from infoboard.models import RulesAndRegulation, EmergencyContact
from django.utils import timezone

# Python modules
import datetime

TOKEN = 'NzA5NjI5NjYxODA5OTk5OTcy.XrosZA.oGKP0dACsI33vLZQG7NhdbUmbVY'

client = commands.Bot(command_prefix='!')

currentDT = datetime.datetime.now().strftime("_%a, %d-%m-%Y, %I:%M:%S%p_")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        # Help Message
        if message.content.strip().lower() == '!help':
            help_message = f'欢迎来到《绝密追查》社交媒体多人连线游戏\n{currentDT}\n\nReply with commands below\n\n!rank - show the latest ranking 📊️\n!mission - show the mission details 🗒️\n!schedule - show the mission schedule ⌛\n!rules - show the rules and regulations ⛔\n!emergency - show emergency contacts ☎️\n!help - show this help message 🔢'
            print('Help messages sent.')
            await message.channel.send(help_message)

        # Ranking
        if message.content.strip().lower().startswith('!rank'):
            dev_message = 'This feature is currently under development.'
            print('Ranking sent.')
            await message.channel.send(dev_message)

        # Schedule
        # if message.content.strip().lower() == '!schedule' or message.content.strip().lower() == '!timeline':
        #     title_MissionSchedule = f'*Mission Schedule ⌛*\n'
        #     list_of_missions = ''           

        #     for mission in MissionDetail.objects.all().order_by('start_time'):
        #         list_of_missions += 


        # Mission Details
        if message.content.strip().lower() == '!mission':
            # title_MissionDetail = f'Mission Details 🗒️\n'
            # list_of_missions = ''

            # for mission in MissionDetail.objects.all().order_by('start_time'):
            #     list_of_missions += f'{mission.id}. {mission.mission_title_chi} {mission.mission_title_eng}\n'

            # title_MissionDetail += list_of_missions
            # command_example = '\neg: !mission 3'
            # title_MissionDetail += command_example

            # print('Mission List sent.')

            # await message.channel.send(title_MissionDetail)
            await message.channel.send("This feature is under development.")
        elif message.content.strip().lower().startswith('!mission'):
            idx = message.content.strip().split()[1]

            mission = MissionDetail.objects.all().filter(id=idx)[0]

            # Cleaning the description
            clean_desc_chi = mission.mission_description_chi.replace('-','').split('\r\n')
            clean_desc_eng = mission.mission_description_eng.replace('-','').split('\r\n')
            clean_desc_chi = list(filter(lambda x: x != '', clean_desc_chi))
            clean_desc_eng = list(filter(lambda x: x != '', clean_desc_eng))
            clean_desc_chi = '\n'.join(clean_desc_chi)
            clean_desc_eng = '\n'.join(clean_desc_eng)

            start_time = timezone.localtime(mission.start_time).strftime("%I:%M%p %d/%m(%a)")
            end_time = timezone.localtime(mission.end_time).strftime("%I:%M%p %d/%m(%a)")
            duration = mission.end_time - mission.start_time

            mission_message = f"《{mission.mission_title_chi} {mission.mission_title_eng}》\n\n{clean_desc_chi}\n{clean_desc_eng}\n\nStart Time: {start_time}\nEnd Time: {end_time}\nDuration: {duration}"

            print(f'Mission {idx} details sent.')

            await message.channel.send(mission_message)

        # Rule and Regulations
        if message.content.strip().lower() == '!rule' or message.content.strip().lower() == '!rules':
            title_RulesAndRegulation = f'Rules and Regulations ⛔\n'

            for rule in RulesAndRegulation.objects.all():
                rule_msg = f'{rule.id}. {rule.rule_chi} {rule.rule_eng}\n'
                title_RulesAndRegulation += rule_msg

            print('Rules sent.')

            await message.channel.send(title_RulesAndRegulation)
    
        # Emergency Contact
        if message.content.strip().lower() == '!emergency':
            title_EmergencyContact = f'Emergency Contact ☎️\nContact only if there is any enquiries on games or rules and regulations.\n'

            for contact in EmergencyContact.objects.all():
                contact_msg = f'{contact.id}. {contact.name_chi} {contact.name_eng} {contact.phone_number}\n'
                title_EmergencyContact += contact_msg

            print('Emergency contacts sent.')

            await message.channel.send(title_EmergencyContact)

        # Clear Messages
        if message.content.strip().lower().startswith('!clear'):
            if len(message.content.strip().lower().split()) > 1:
                amount = message.content.strip().lower().split()[1]

            amount = 100
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=amount):
                messages.append(message)
            await channel.delete_messages(messages)
            await ctx.send(f'{amount} messages deleted.')

# Mission Details
@client.command()
async def mission(ctx, *args):
    if str(args) == '()':
        title_MissionDetail = f'Mission Details 🗒️\n'
        list_of_missions = ''

        for mission in MissionDetail.objects.all().order_by('start_time'):
            list_of_missions += f'{mission.id}. {mission.mission_title_chi} {mission.mission_title_eng}\n'

        title_MissionDetail += list_of_missions
        command_example = '\neg: !mission 3'
        title_MissionDetail += command_example

        print('Mission List sent.')

        await ctx.send(title_MissionDetail)
    else:
        idx = args[0]

        mission = MissionDetail.objects.all().filter(id=idx)[0]

        # Cleaning the description
        clean_desc_chi = mission.mission_description_chi.replace('-','').split('\r\n')
        clean_desc_eng = mission.mission_description_eng.replace('-','').split('\r\n')
        clean_desc_chi = list(filter(lambda x: x != '', clean_desc_chi))
        clean_desc_eng = list(filter(lambda x: x != '', clean_desc_eng))
        clean_desc_chi = '\n'.join(clean_desc_chi)
        clean_desc_eng = '\n'.join(clean_desc_eng)

        start_time = timezone.localtime(mission.start_time).strftime("%I:%M%p %d/%m(%a)")
        end_time = timezone.localtime(mission.end_time).strftime("%I:%M%p %d/%m(%a)")
        duration = mission.end_time - mission.start_time

        message = f"《{mission.mission_title_chi} {mission.mission_title_eng}》\n\n{clean_desc_chi}\n{clean_desc_eng}\n\nStart Time: {start_time}\nEnd Time: {end_time}\nDuration: {duration}"

        print(f'Mission {idx} details sent.')

        await ctx.send(message)

# Rules and Regulations
@client.command()
async def rules(ctx):
    title_RulesAndRegulation = f'Rules and Regulations ⛔\n'

    for rule in RulesAndRegulation.objects.all():
        rule_msg = f'{rule.id}. {rule.rule_chi} {rule.rule_eng}\n'
        title_RulesAndRegulation += rule_msg

    await ctx.send(title_RulesAndRegulation)

@client.command()
async def rule(ctx):
    title_RulesAndRegulation = f'Rules and Regulations ⛔\n'

    for rule in RulesAndRegulation.objects.all():
        rule_msg = f'{rule.id}. {rule.rule_chi} {rule.rule_eng}\n'
        title_RulesAndRegulation += rule_msg

    await ctx.send(title_RulesAndRegulation)

# Emergency Contact
@client.command()
async def emergency(ctx):
    title_EmergencyContact = f'Emergency Contact ☎️\nContact only if there is any enquiries on games or rules and regulations.\n'

    for contact in EmergencyContact.objects.all():
        contact_msg = f'{contact.id}. {contact.name_chi} {contact.name_eng} {contact.phone_number}\n'
        title_EmergencyContact += contact_msg

    await ctx.send(title_EmergencyContact)

@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount):
        messages.append(message)
    await channel.delete_messages(messages)
    await ctx.send(f'{amount} messages deleted.')

client.run(TOKEN)