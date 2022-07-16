import discord
from discord.ext import commands, tasks
import gspread_asyncio
import aiohttp, asyncio
import json
import time
import re
import random
from bot_utils.roleId import Roles

from google.oauth2.service_account import Credentials

def get_creds():
    creds = Credentials.from_service_account_file("/home/container/cogs/JSON credentials/credentials_patrol.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

def deEmojify(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'',text)

rules = {
	"A1":"[A1] Be respectful and do not harass members of the group or discord. This includes inside AND outside the server, etc Discord DMs and ROBLOX PMs.",
	"A2":"[A2] Chat or use commands in the proper channels. If you’re going to have a public, general conversation you are to talk in the #general-channel. Misusing a channel will result in first a verbal (typed) warning to go to the proper channel; failure to do so will result in a warning.",
	"A3":"[A3] Spamming is prohibited in ALL channels of the Robloxian Adventures Discord. Doing this can result in being warned, kicked, or banned based on the severity of the situation.",
	"A4":"[A4] Swearing is now allowed but limited and moderated. You’re not allowed to use any racial/offensive slurs or anything to insult someone.",
	"A5":"[A5] Do not argue in public chatrooms. This can include provoking and/or targeting. If you want to argue, take it to your DMs.",
	"A6":"[A6] Raiding the RA, or any RA affiliated discord servers will result in an immediate ban. You will not be warned. (Ex: RATA, EIC, PO, and S&R).",
	"A7":"[A7] Links that break our rules or contain malicious content are not allowed and will be taken down. IP Grabbers are against Discord guidelines.",
	"A8":"[A8] You are prohibited from pinging (@ Username) or ( @ role) without a valid reason. Pinging any member without a valid reason will result in a warn, report random pings only if you're the one getting pinged.",
	"A9": "[A9] Advertising is not allowed. (YOU MAY NOT ADVERTISE THE FOLLOWING: Groups, games, clothing, Discord servers, or giveaways.) DM advertising is also strictly prohibited.",
	"A10": "[A10] We do not allow any ‘selfbots.’ Adding bots will result in those accounts being kicked/banned and your main Discord account being kicked/banned.",
	"A11": "[A11] Impersonation is a bannable offense here. If you believe someone is impersonating you please contact a Moderator + to resolve the issue.",
	"A12": "[A12] Arguing with staff about previous moderation action taken against you, OR A FRIEND, will result in further moderated punishment. You are entitled to ask why moderation was taken against you, but that does not allow you to argue about it.",
	"A13": "[A13] Slightly religious, political, or controversial topics are allowed for discussion as long as they do not get out of hand. A moderator will take action if it does.",
	"A14": "[A14] Trolling is prohibited at this server. Trolling includes anything that could disrupt any ongoing group operations.",
	"A15": "[A15] You may not post/upload cracked programs or programs that are not free for the general public.",
	"A16": "[A16] NSFW content is strictly prohibited with 0 tolerance. (links, profile pictures, pictures, videos, etc.)",
	"A17": "[A17] You may not expose anyone’s personal information without their consent. This includes, but is not limited to: social media, phone numbers, addresses, face reveals, private family matters, pictures, or videos.",
	"A18": "[A18] English is the only mode of communication to be used in channels, voice channels, images and videos. Prolonged usage of any other language will result in a warn.",
	"B1": "[B1] Playing annoying entertainment, sounds, or music is considered ‘mic spamming.’ If you want to play music, go to the music channel.",
	"B2": "[B2] We have music bots for a reason, so do not play music through your microphone.",
	"B3": "[B3] Swearing is allowed in voice chats. However, racial slurs, severe insults, and disrespect towards a member (refer to A1) will not be tolerated and is strictly enforced. The same applies to any audio played through music bots.",
	"B4": "[B4] Do not spam move into different channels. Discord gives a sound notification when someone joins a voice channel, you are not allowed to spam that notification.",
	"B5": "[B5] You are not allowed to use voice changers.",
	"B6": "[B6] Recording/streaming other users without their permission is a federal offence. Doing so will result in removal from Robloxian Adventures and the Discord.",
	"B7": "[B7] Yelling/screaming into your microphone is not allowed.",
	"B8": "[B8] As stated in A18, English is the only language allowed as a mode of communication in VC's. Prolonged use of any other language will result in a warn.", 
	"C1": "[C1] Do not ask for trainings.",
	"C2": "[C2] Do not be disruptive during trainings.",
	"C3": "[C3] The max amount of spectators in a training is 6. Head Instructor+ do not count as a spectator.",
	"C4": "[C4] The use of exploits/hacks at the training facility is strictly prohibited and will result in a blacklist.",
	"C5": "[C5] Disrespecting an individual during a training will result in a kick from the training and a discord warning.",
	"C6": "[C6] Voting for a training and not attending will result in a warn."

}

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )
    
stats_intervals = (
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    )

def inmodcmds(ctx):
    return ctx.channel.id == 427012742789070849

def time_convert_mod(sec):
    mins = sec // 60
    sec = round(sec % 60)
    if int(sec) == 60:
        sec = 0
        mins+=1
    return f"{int(mins):02} minutes | {int(sec):02} seconds"

def time_convert_special(sec):
    mins = sec // 60
    sec = round(sec % 60)
    if int(sec) == 60:
        sec = 0
        mins+=1
    return f"[{int(mins):02}:{round(sec):02}]"

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    return ', '.join(result[:granularity])

# ------------------------------------
# Button Classes

class IASConfirmView(discord.ui.View):
    def __init__(self, author : discord.Member, *, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return True
        else:
            return False 

    @discord.ui.button(label='Confirm Presence', style=discord.ButtonStyle.gray, emoji='<:yes:614538082774941716>')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Presence confirmed!', ephemeral=True)
        self.value = True
        self.stop()

class ON_DMAlertsView(discord.ui.View):
    def __init__(self, author : discord.Member, *, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return True
        else:
            return False 
    
    @discord.ui.button(label='Enable', style=discord.ButtonStyle.green, emoji='<:yes:614538082774941716>')
    async def enable(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()
    @discord.ui.button(label='Cancel Prompt', style=discord.ButtonStyle.gray, emoji='✖️')
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

class OFF_DMAlertsView(discord.ui.View):
    def __init__(self, author : discord.Member, *, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return True
        else:
            return False 
    
    @discord.ui.button(label='Disable', style=discord.ButtonStyle.red, emoji='⛔')
    async def disable(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()
    @discord.ui.button(label='Cancel Prompt', style=discord.ButtonStyle.gray, emoji='✖️')
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()




# ------------------------------------
# Cog Start

class PatrolCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.activityPinger.start()

    @commands.Cog.listener()
    async def on_ready(self):
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Patrol Commands cog healthy.")

    @tasks.loop(seconds=30)
    async def activityPinger(self):
        curTime = time.time()
        async def one_iter(modId):
            if self.client.activityDB[modId] != None:
                timeDiff = curTime - self.client.activityDB[modId]
                #-----------------------------------------------------------------
                cursor = await self.client.db.execute(f"SELECT next_ias FROM patrol WHERE id='{modId}'")
                data = await cursor.fetchone()
                if data != None:
                    next_ias = data[0]
                else:
                    next_ias = 1200 # 20 mins
                await cursor.close()
                #-----------------------------------------------------------------
                if timeDiff >= next_ias:
                    modChannel = self.client.get_channel(941735460298952734)
                    guild = self.client.get_guild(427007974947553280)
                    mod = guild.get_member(modId)
                    self.client.activityDB[modId] = None
                    #-----------------------------------------------------------------
                    cursor = await self.client.db.execute(f"SELECT ias_dm_toggle FROM patrol WHERE id='{modId}'")
                    data = await cursor.fetchone()
                    if data != None:
                        dm_toggle = data[0]
                    else:
                        dm_toggle = False
                    await cursor.close()
                    #-----------------------------------------------------------------
                    embed = discord.Embed(title="Inactivity Alert System", description=f"You have been flagged for inactivity for over {display_time(timeDiff)}. Click the button below to confirm your presence.", colour=0xFFFF00).set_footer(text="Prompt times out in 2 minutes").set_thumbnail(url="https://cdn.discordapp.com/attachments/678298437854298122/865876440851546162/c.png").set_author(name=mod.display_name,icon_url=mod.avatar)
                    view = IASConfirmView(mod)
                    IASalertmsg = await modChannel.send(
                        f'{mod.mention}',
                        embed=embed,
                        view=view
                    )
                    await view.wait()
                    if view.value: # Confirmed
                        embed = discord.Embed(title="Presence confirmed!",description="An automated comment has been added to your patrol.",colour=0x7FFF00).set_thumbnail(url="https://cdn.discordapp.com/attachments/678298437854298122/865875608987107328/a.png").set_author(name=mod.display_name,icon_url=mod.avatar)
                        await IASalertmsg.edit(content=f"{mod.mention}", embed=embed, view=None)
                        self.client.activityDB[modId] = time.time()
                        patrolchannel = self.client.get_channel(696133524167720970)
                        user_id = mod.id
                        #-----------------------------------------------------------------
                        cursor = await self.client.db.execute(f"SELECT * FROM patrol WHERE id='{user_id}'")
                        data = await cursor.fetchone()
                        raw_starttime = data[2]
                        patrolling_status = data[3]
                        original_strt_msgid = data[4]
                        raw_commentslog = eval(data[5])
                        await cursor.close()
                        #-----------------------------------------------------------------
                        if patrolling_status == True:
                            original_strt_msg = await patrolchannel.fetch_message(original_strt_msgid)
                            embed=discord.Embed(title="‎[RATA] Moderation Patrol Started", description=f"__**Moderator**__\n{mod.mention}", color=0x13d510)
                            embed.set_author(name=mod.display_name, icon_url=mod.avatar)
                            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
                            embed.add_field(name="Start Time:", value=f"<t:{round(raw_starttime)}:f>", inline=True)
                            time_elapsed_sec = time.time() - raw_starttime
                            iascheck = False
                            for i in raw_commentslog:
                                if isinstance(i,dict):
                                    iascheck = raw_commentslog.index(i)
                            if iascheck == False:
                                raw_commentslog.append({"ias":[f"{time_convert_special(time_elapsed_sec)}"]})
                            else:
                                raw_commentslog[iascheck]['ias'].append(f"{time_convert_special(time_elapsed_sec)}")
                            comments = ""
                            for i in range(1,len(raw_commentslog)):
                                if i==1:
                                    if isinstance(raw_commentslog[i], dict):
                                        time_str = ', '.join(raw_commentslog[i]['ias'])
                                        comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                                        comments = "◉"+" "+comment_sep+time_str
                                        continue
                                    comment_sep = str(raw_commentslog[i])
                                    comments = "◉"+" "+comment_sep
                                    continue
                                if i>1:
                                    if isinstance(raw_commentslog[i], dict):
                                        time_str = ', '.join(raw_commentslog[i]['ias'])
                                        comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                                        comments = comments+"\n"+"◉"+" "+comment_sep+time_str
                                        continue
                                    comment_sep = str(raw_commentslog[i])
                                    comments = comments+"\n"+"◉"+" "+comment_sep
                                    continue
                            embed.add_field(name="Patrol Comments", value=f"{comments}", inline=False)
                            await original_strt_msg.edit(embed=embed)
                            ias_randomize = random.choice([1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620]) #17 - 27

                            await self.client.db.execute(f"UPDATE patrol SET commentslog=\"{str(raw_commentslog)}\", next_ias={ias_randomize} WHERE id={user_id}")
                            await self.client.db.commit()
                        else:
                            pass
                    else: # Timed out - 1 minute
                        if dm_toggle:
                            reminderAlertMsg = await mod.send(embed=discord.Embed(title="Inactivity Alert System", description=f'{mod.mention}, you have **`60`** seconds left to respond to [this]({IASalertmsg.jump_url}) IAS check.', colour=0xFFFF00).set_footer(text="Toggleable DM Alert").set_thumbnail(url="https://cdn.discordapp.com/attachments/678298437854298122/865876440851546162/c.png"))
                        else:
                            reminderAlertMsg = await IASalertmsg.reply(f'{mod.mention}, you have **`60`** seconds left to respond.')
                        embed = discord.Embed(title="Inactivity Alert System", description=f"You have been flagged for inactivity for over {display_time(timeDiff)}. Click the button below to confirm your presence.", colour=0xFFFF00).set_footer(text="Prompt times out in 1 minute").set_thumbnail(url="https://cdn.discordapp.com/attachments/678298437854298122/865876440851546162/c.png").set_author(name=mod.display_name,icon_url=mod.avatar)
                        view = IASConfirmView(mod)
                        await IASalertmsg.edit(
                            content=f'{mod.mention}',
                            embed=embed,
                            view=view
                        )
                        await view.wait()
                        if view.value: # Confirmed
                            embed = discord.Embed(title="Presence confirmed!",description="An automated comment has been added to your patrol.",colour=0x7FFF00).set_thumbnail(url="https://cdn.discordapp.com/attachments/678298437854298122/865875608987107328/a.png").set_author(name=mod.display_name,icon_url=mod.avatar)
                            await reminderAlertMsg.delete(delay=0)
                            await IASalertmsg.edit(content=f"{mod.mention}", embed=embed, view=None)
                            self.client.activityDB[modId] = time.time()
                            patrolchannel = self.client.get_channel(696133524167720970)
                            user_id = mod.id
                            #-----------------------------------------------------------------
                            cursor = await self.client.db.execute(f"SELECT * FROM patrol WHERE id='{user_id}'")
                            data = await cursor.fetchone()
                            raw_starttime = data[2]
                            patrolling_status = data[3]
                            original_strt_msgid = data[4]
                            raw_commentslog = eval(data[5])
                            await cursor.close()
                            #-----------------------------------------------------------------
                            if patrolling_status == True:
                                original_strt_msg = await patrolchannel.fetch_message(original_strt_msgid)
                                embed=discord.Embed(title="‎[RATA] Moderation Patrol Started", description=f"__**Moderator**__\n{mod.mention}", color=0x13d510)
                                embed.set_author(name=mod.display_name, icon_url=mod.avatar)
                                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
                                embed.add_field(name="Start Time:", value=f"<t:{round(raw_starttime)}:f>", inline=True)
                                time_elapsed_sec = time.time() - raw_starttime
                                iascheck = False
                                for i in raw_commentslog:
                                    if isinstance(i,dict):
                                        iascheck = raw_commentslog.index(i)
                                if iascheck == False:
                                    raw_commentslog.append({"ias":[f"{time_convert_special(time_elapsed_sec)}"]})
                                else:
                                    raw_commentslog[iascheck]['ias'].append(f"{time_convert_special(time_elapsed_sec)}")
                                comments = ""
                                for i in range(1,len(raw_commentslog)):
                                    if i==1:
                                        if isinstance(raw_commentslog[i], dict):
                                            time_str = ', '.join(raw_commentslog[i]['ias'])
                                            comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                                            comments = "◉"+" "+comment_sep+time_str
                                            continue
                                        comment_sep = str(raw_commentslog[i])
                                        comments = "◉"+" "+comment_sep
                                        continue
                                    if i>1:
                                        if isinstance(raw_commentslog[i], dict):
                                            time_str = ', '.join(raw_commentslog[i]['ias'])
                                            comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                                            comments = comments+"\n"+"◉"+" "+comment_sep+time_str
                                            continue
                                        comment_sep = str(raw_commentslog[i])
                                        comments = comments+"\n"+"◉"+" "+comment_sep
                                        continue
                                embed.add_field(name="Patrol Comments", value=f"{comments}", inline=False)
                                await original_strt_msg.edit(embed=embed)
                                ias_randomize = random.choice([1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620]) #17 - 27

                                await self.client.db.execute(f"UPDATE patrol SET commentslog=\"{str(raw_commentslog)}\", next_ias={ias_randomize} WHERE id={user_id}")
                                await self.client.db.commit()
                            else:
                                pass
                        else: # Timed out - 2 minutes - Cancelled
                            embed = discord.Embed(title="Inactivity Alert Timed Out", description=f"{mod.mention} failed to interact with the alert within two minutes.\n\nThe patrol will now be automatically cancelled by `IAS`.", colour=0xFF0000).set_thumbnail(url="https://cdn.discordapp.com/attachments/678298437854298122/865875824409837628/b.png").set_author(name=mod.display_name,icon_url=mod.avatar)
                            await reminderAlertMsg.delete(delay=0)
                            await IASalertmsg.edit(content=f"{mod.mention}", embed = embed, view=None)
                            guild = self.client.get_guild(427007974947553280)
                            patrolchannel = self.client.get_channel(696133524167720970)
                            victim_id = mod.id
                            #-----------------------------------------------------------------
                            cursor = await self.client.db.execute(f"SELECT * FROM patrol WHERE id='{victim_id}'")
                            data = await cursor.fetchone()
                            raw_starttime = data[2]
                            patrolling_status = data[3]
                            original_strt_msgid = data[4]
                            raw_commentslog = eval(data[5])
                            t_cancelled_patrols = data[9]
                            sum_patroltime = data[10]
                            prev_patrols = eval(data[11])
                            await cursor.close()
                            #-----------------------------------------------------------------
                            if patrolling_status == True:
                                raw_endtime = time.time()
                                finalSeconds = raw_endtime - raw_starttime
                                t_cancelled_patrols += 1
                                original_strt_msg = await patrolchannel.fetch_message(original_strt_msgid)
                                embed=discord.Embed(title="‎[RATA] Moderation Patrol Cancelled", description=f"__**Moderator**__\n{mod.mention}", color=0x949494)
                                embed.set_author(name=mod.display_name, icon_url=mod.avatar)
                                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
                                embed.add_field(name="Start Time:", value=f"<t:{round(raw_starttime)}:f>", inline=True)
                                embed.add_field(name="Cancellation Time:", value=f"<t:{round(raw_endtime)}:f>", inline=True)
                                if len(raw_commentslog)>1:
                                    comments = ""
                                    for i in range(1,len(raw_commentslog)):
                                        if i==1:
                                            if isinstance(raw_commentslog[i], dict):
                                                time_str = ', '.join(raw_commentslog[i]['ias'])
                                                comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                                                comments = "◉"+" "+comment_sep+time_str
                                                continue
                                            comment_sep = str(raw_commentslog[i])
                                            comments = "◉"+" "+comment_sep
                                            continue
                                        if i>1:
                                            if isinstance(raw_commentslog[i], dict):
                                                time_str = ', '.join(raw_commentslog[i]['ias'])
                                                comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                                                comments = comments+"\n"+"◉"+" "+comment_sep+time_str
                                                continue
                                            comment_sep = str(raw_commentslog[i])
                                            comments = comments+"\n"+"◉"+" "+comment_sep
                                            continue
                                    embed.add_field(name="Patrol Comments", value=f"{comments}", inline=False)
                                elif len(raw_commentslog)==1:
                                    embed.add_field(name="Patrol Comments", value="No comments added.", inline=False)
                                embed.add_field(name="Cancelled by:", value="**`Inactivity Alert System`**", inline=True)
                                embed.add_field(name="Reason:", value=f"Unable to respond to IAS alert", inline=True)
                                embed.add_field(name="Total Patrolling Minutes", value=f"{time_convert_mod(raw_endtime - raw_starttime)}", inline=False)
                                await original_strt_msg.edit(content=mod.mention, embed=embed)
                                embed2=discord.Embed(title="Your RATA Moderator Patrol was cancelled",description=f"The **`Inactivity Alert System`** has cancelled your patrol with the reason being flagged for inactivity for {display_time(timeDiff)}.\n\nView the [Cancellation Report]({original_strt_msg.jump_url}) for more information.",color=0xff0f0f)
                                embed2.set_footer(text="Robloxian Adventures Training Academy", icon_url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
                                await mod.send(embed=embed2)
                                del self.client.activityDB[victim_id]
                                
                                await self.client.db.execute(f"UPDATE patrol SET starttime=Null, status=False, startmsg_id=Null, commentslog='{{}}', t_cancelled_patrols={t_cancelled_patrols}, next_ias=Null WHERE id={victim_id}")
                                await self.client.db.commit()
                                
                                # Removal of code for reduced time logging for cancelled patrols
                                # agc = await agcm.authorize()
                                # g_sheet = await agc.open_by_key("1Cwi5qBuI0kG1DEQZ605Nl_qBRFFyvxMoDv4U_U6DmyQ")
                                # g_worksheet = await g_sheet.worksheet("Activity Record")
                                # actualName = deEmojify(str(mod.display_name)).split()[-1].replace(" ","")
                                # try:
                                #     foundName = await g_worksheet.find(actualName)
                                # except:
                                #     s_modchannel = self.client.get_channel(597971477190410242)
                                #     return await s_modchannel.send(embed=discord.Embed(title=f'SPREADSHEET ERROR:', description=f'Could not log {mod.mention}\'s patrol. `{actualName}` not found on spreadsheet. This will require manual logging.\n\nPatrol Link: [Click Me!]({original_strt_msg.jump_url})',colour=0xFF0000))
                                # currentDay = time.strftime("%A", time.gmtime(raw_starttime))
                                # dayCell = await g_worksheet.find(str(currentDay))
                                # if int(finalSeconds // 60) < 200:
                                #     minsValue = int((await g_worksheet.cell(foundName.row,dayCell.col)).value or "0") + round(int(finalSeconds // 60)-(int(finalSeconds // 60)*0.25))
                                # else:
                                #     minsValue = int((await g_worksheet.cell(foundName.row,dayCell.col)).value or "0") + round(int(finalSeconds // 60)-(int(finalSeconds // 60)*0.15))
                                # await g_worksheet.update_cell(foundName.row, dayCell.col, str(minsValue))
                                # await original_strt_msg.add_reaction("<a:RO_check:848611390993203221>")
                                # await original_strt_msg.add_reaction("📑")
                                
                            else:
                                pass

        coros = [one_iter(modId) for modId in list(self.client.activityDB)]
        await asyncio.gather(*coros)

    @activityPinger.before_loop
    async def before_printer(self):
        await self.client.wait_until_ready()
    
    @commands.command(name='checktask_activity',aliases=['ct_activity'])
    @commands.is_owner()
    async def checktask_activity(self,ctx):
        var = self.activityPinger.is_running()
        var1 = self.activityPinger.failed()
        var2 = self.activityPinger.next_iteration
        await ctx.send(f'Running: **{var}**\nNext Iteration: `{var2.strftime("%m/%d/%Y, %H:%M:%S %Z")}`')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id not in self.client.activityDB.keys():
            return
        if message.guild == None or message.guild.id != 427007974947553280:
            return
        self.client.activityDB[message.author.id] = time.time()
        
    @commands.command(name="startpatrol")
    @commands.check(inmodcmds)
    @commands.cooldown(1,2.5,commands.BucketType.user)
    async def startpatrol(self, ctx):
        guild = self.client.get_guild(427007974947553280)
        patrolchannel = self.client.get_channel(696133524167720970)
        executor_id = ctx.author.id
        member = guild.get_member(executor_id)
        #-----------------------------------------------------------------

        async with self.client.db.execute(f"SELECT status, t_patrols FROM patrol WHERE id='{executor_id}'") as cursor:
            res = await cursor.fetchone()
            if res == None:
                patrolling_status = None
                t_patrols = 0
            else:
                patrolling_status = res[0]
                t_patrols = res[1]

        #-----------------------------------------------------------------
        if patrolling_status == False or patrolling_status == None:
            embed=discord.Embed(title="[RATA] Moderation Patrol Started‎", description=f"__**Moderator**__\n{ctx.author.mention}", color=0x13d510)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
            embed.add_field(name="Start Time:", value=f"<t:{round(time.time())}:f>", inline=True)
            embed.add_field(name="Patrol Comments:", value="No comments yet.", inline=False)
            temp_strt_msg = await patrolchannel.send(content=ctx.author.mention, embed=embed)
            await ctx.send(f"<a:RO_online:773206810635141200> You have started your patrol, **{member.display_name}**.")
            self.client.activityDB[executor_id] = time.time()
            t_patrols += 1
            ias_randomize = random.choice([1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620]) #17 - 27
            
            async with self.client.db.execute(f"SELECT status FROM patrol WHERE id='{executor_id}'") as cursor:
                row = await cursor.fetchone()
                if row == None:
                    await self.client.db.execute(f"INSERT INTO patrol VALUES ({str(executor_id)},'{ctx.author.display_name}',{str(time.time())},True,{str(temp_strt_msg.id)},\"{str(['No comments yet.'])}\",False,{t_patrols},0,0,0,\"[]\",{ias_randomize})")
                    await self.client.db.commit()
                else:
                    await self.client.db.execute(f"UPDATE patrol SET name=\"{deEmojify(member.display_name)}\", starttime={str(time.time())}, status=True, startmsg_id={str(temp_strt_msg.id)}, commentslog=\"{str(['No comments yet.'])}\", t_patrols={t_patrols}, next_ias={ias_randomize} WHERE id={executor_id}")
                    await self.client.db.commit()
        
        elif patrolling_status == True:
            return await ctx.send("<:RO_error:773206804758790184> You already have a on-going patrol. Use `r.endpatrol` to end the patrol.")
        
    @commands.command(name = "comment")
    @commands.has_any_role(Roles.senior_moderator, Roles.lead_moderator, Roles.board_of_directors, Roles.assistant_director, Roles.director, Roles.advisor, Roles.lead_moderator)
    @commands.cooldown(1,2,commands.BucketType.user)
    @commands.guild_only()
    async def comment(self, ctx, member : discord.Member, *, comment : str):
        patrolchannel = self.client.get_channel(696133524167720970)
        user_id = member.id
        #-----------------------------------------------------------------
        cursor = await self.client.db.execute(f"SELECT * FROM patrol WHERE id='{user_id}'")
        data = await cursor.fetchone()
        if data == None:
            await cursor.close()
            return await ctx.send(f"<:RO_error:773206804758790184> {member.display_name} is not in the moderator database.")
        else:
            raw_starttime = data[2]
            patrolling_status = data[3]
            original_strt_msgid = data[4]
            raw_commentslog = eval(data[5])
            await cursor.close()
        #-----------------------------------------------------------------
        if patrolling_status == True:
            original_strt_msg = await patrolchannel.fetch_message(original_strt_msgid)
            embed=discord.Embed(title="‎[RATA] Moderation Patrol Started", description=f"__**Moderator**__\n{member.mention}", color=0x13d510)
            embed.set_author(name=member.display_name, icon_url=member.avatar)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
            embed.add_field(name="Start Time:", value=f"<t:{round(raw_starttime)}:f>", inline=True)
            time_elapsed_sec = time.time() - raw_starttime
            raw_commentslog.append(f"{time_convert_special(time_elapsed_sec)} {ctx.author.mention} - {comment}")
            comments = ""
            for i in range(1,len(raw_commentslog)):
                if i==1:
                    if isinstance(raw_commentslog[i], dict):
                        time_str = ', '.join(raw_commentslog[i]['ias'])
                        comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                        comments = "◉"+" "+comment_sep+time_str
                        continue
                    comment_sep = str(raw_commentslog[i])
                    comments = "◉"+" "+comment_sep
                    continue
                if i>1:
                    if isinstance(raw_commentslog[i], dict):
                        time_str = ', '.join(raw_commentslog[i]['ias'])
                        comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                        comments = comments+"\n"+"◉"+" "+comment_sep+time_str
                        continue
                    comment_sep = str(raw_commentslog[i])
                    comments = comments+"\n"+"◉"+" "+comment_sep
                    continue
            embed.add_field(name="Patrol Comments", value=f"{comments}", inline=False)
            await ctx.send(f"<:RO_success:773206804850016276> Added comment `{comment}` to {member.display_name}\'s patrol log.")
            await original_strt_msg.edit(embed=embed)

            await self.client.db.execute(f"UPDATE patrol SET commentslog=\"{str(raw_commentslog)}\" WHERE id={user_id}")
            await self.client.db.commit()

        else:
            await ctx.send(f"<:RO_error:773206804758790184> {member.display_name} is not on patrol currently.")
        

    @comment.error
    async def comment_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send("<a:RO_alert:773211228373647360> User was not found. Please ensure you are using either complete discord username (abc#1234), their @ mention or their user ID.")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("<a:RO_alert:773211228373647360> Missing necessary argument.\n```\nr.comment <user> <comment>\n```")   



    @commands.command(name = "endpatrol")
    @commands.check(inmodcmds)
    @commands.cooldown(1,2.5,commands.BucketType.user)
    async def endpatrol(self, ctx):
        guild = self.client.get_guild(427007974947553280)
        patrolchannel = guild.get_channel(696133524167720970)
        executor_id = ctx.author.id
        member = guild.get_member(executor_id)
        #-----------------------------------------------------------------
        cursor = await self.client.db.execute(f"SELECT * FROM patrol WHERE id='{executor_id}'")
        data = await cursor.fetchone()
        if data == None:
            await cursor.close()
            return await ctx.send(f"<:RO_error:773206804758790184> Your record is not in the moderator database.")
        else:
            raw_starttime = data[2]
            patrolling_status = data[3]
            original_strt_msgid = data[4]
            raw_commentslog = eval(data[5])
            t_full_patrols = data[8]
            sum_patroltime = data[10]
            prev_patrols = eval(data[11])
            await cursor.close()
        #-----------------------------------------------------------------
        if patrolling_status == True:
            original_strt_msg = await patrolchannel.fetch_message(original_strt_msgid)
            raw_endtime = time.time()
            finalSeconds = raw_endtime - raw_starttime
            if finalSeconds < 600:
                embed=discord.Embed(title="‎[RATA] Moderation Patrol Ended", description=f"__**Moderator**__\n{ctx.author.mention}", color=0x949494)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
                embed.add_field(name="Start Time:", value=f"<t:{round(raw_starttime)}:f>", inline=True)
                embed.add_field(name="End Time:", value=f"<t:{round(raw_endtime)}:f>", inline=True)
                if len(raw_commentslog)>1:
                    comments = ""
                    for i in range(1,len(raw_commentslog)):
                        if i==1:
                            if isinstance(raw_commentslog[i], dict):
                                time_str = ', '.join(raw_commentslog[i]['ias'])
                                comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                                comments = "◉"+" "+comment_sep+time_str
                                continue
                            comment_sep = str(raw_commentslog[i])
                            comments = "◉"+" "+comment_sep
                            continue
                        if i>1:
                            if isinstance(raw_commentslog[i], dict):
                                time_str = ', '.join(raw_commentslog[i]['ias'])
                                comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                                comments = comments+"\n"+"◉"+" "+comment_sep+time_str
                                continue
                            comment_sep = str(raw_commentslog[i])
                            comments = comments+"\n"+"◉"+" "+comment_sep
                            continue
                    embed.add_field(name="Patrol Comments", value=f"{comments}", inline=False)
                elif len(raw_commentslog)==1:
                    embed.add_field(name="Patrol Comments", value="No comments added.", inline=False)
                embed.add_field(name="Total Patrolling Minutes", value=f"{time_convert_mod(finalSeconds)}", inline=False)
                await original_strt_msg.edit(content=ctx.author.mention,embed=embed)
                await ctx.send(f"<a:RO_offline:773206809091506217> You have ended your patrol, **{member.display_name}**. However, due to the patrol duration being less than 10 minutes, your patrol will not be logged.")
                del self.client.activityDB[executor_id]
                
                await self.client.db.execute(f"UPDATE patrol SET starttime=Null, status=False, startmsg_id=Null, commentslog='{{}}', next_ias=Null WHERE id={executor_id}")
                await self.client.db.commit()

            else:
                embed=discord.Embed(title="‎[RATA] Moderation Patrol Ended", description=f"__**Moderator**__\n{ctx.author.mention}", color=0xff0f0f)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
                embed.add_field(name="Start Time:", value=f"<t:{round(raw_starttime)}:f>", inline=True)
                embed.add_field(name="End Time:", value=f"<t:{round(raw_endtime)}:f>", inline=True)
                if len(raw_commentslog)>1:
                    comments = ""
                    for i in range(1,len(raw_commentslog)):
                        if i==1:
                            if isinstance(raw_commentslog[i], dict):
                                time_str = ', '.join(raw_commentslog[i]['ias'])
                                comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                                comments = "◉"+" "+comment_sep+time_str
                                continue
                            comment_sep = str(raw_commentslog[i])
                            comments = "◉"+" "+comment_sep
                            continue
                        if i>1:
                            if isinstance(raw_commentslog[i], dict):
                                time_str = ', '.join(raw_commentslog[i]['ias'])
                                comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                                comments = comments+"\n"+"◉"+" "+comment_sep+time_str
                                continue
                            comment_sep = str(raw_commentslog[i])
                            comments = comments+"\n"+"◉"+" "+comment_sep
                            continue
                    embed.add_field(name="Patrol Comments", value=f"{comments}", inline=False)
                elif len(raw_commentslog)==1:
                    embed.add_field(name="Patrol Comments", value="No comments added.", inline=False)
                sum_patroltime += finalSeconds
                embed.add_field(name="Total Patrolling Minutes", value=f"{time_convert_mod(finalSeconds)}", inline=False)
                await original_strt_msg.edit(content=ctx.author.mention,embed=embed)
                await ctx.send(f"<a:RO_offline:773206809091506217> You have ended your patrol, **{member.display_name}**.")
                del self.client.activityDB[executor_id]
                t_full_patrols += 1
                prev_patrols.append(finalSeconds)
                if len(prev_patrols) == 7:
                    del prev_patrols[0]
                
                await self.client.db.execute(f"UPDATE patrol SET starttime=Null, status=False, startmsg_id=Null, commentslog='{{}}', t_full_patrols={t_full_patrols}, sum_patroltime={sum_patroltime}, prev_patrols='{prev_patrols}', next_ias=Null WHERE id={executor_id}")
                await self.client.db.commit()

                agc = await agcm.authorize()
                g_sheet = await agc.open_by_key("1Cwi5qBuI0kG1DEQZ605Nl_qBRFFyvxMoDv4U_U6DmyQ")
                g_worksheet = await g_sheet.worksheet("Activity Record")
                actualName = deEmojify(str(ctx.author.display_name)).split()[-1].replace(" ","")
                try:
                    foundName = await g_worksheet.find(actualName)
                except:
                    return await ctx.send(f'**SPREADSHEET ERROR:** `{actualName}` not found')
                currentDay = time.strftime("%A", time.gmtime(raw_starttime))
                dayCell = await g_worksheet.find(str(currentDay))
                minsValue = int((await g_worksheet.cell(foundName.row,dayCell.col)).value or "0") + int(finalSeconds // 60)
                await g_worksheet.update_cell(foundName.row, dayCell.col, str(minsValue))
                await original_strt_msg.add_reaction("<a:RO_check:848611390993203221>")
                await original_strt_msg.add_reaction("📑")

        elif patrolling_status == False:
            await ctx.send("<:RO_error:773206804758790184> You have not started a patrol yet. Please use `r.startpatrol` to start your patrol.")
        



    @commands.command(name = "patroltime")
    @commands.check(inmodcmds)
    @commands.cooldown(1,0.5,commands.BucketType.user)
    async def patroltime(self, ctx, executor : discord.Member = None):

        if executor == None:
            executor_id = ctx.author.id
            
            cursor = await self.client.db.execute(f"SELECT * FROM patrol WHERE id='{executor_id}'")
            data = await cursor.fetchone()
            if data == None:
                await cursor.close()
                return await ctx.send(f"<:RO_error:773206804758790184> Your record is not in the moderator database.")
            else:
                raw_starttime = data[2]
                patrolling_status = data[3]
                await cursor.close()

            if patrolling_status == True:
                current_time = time.time()
                time_elapsed_yet = current_time - raw_starttime
                embed=discord.Embed(description=f"<:RO_time:773207335396573226> {ctx.author.mention}, you have patrolled for **`{time_convert_mod(time_elapsed_yet)}`**.", color=0x24bdff)
                await ctx.send(embed=embed)
            else:
                await ctx.send("<:RO_error:773206804758790184> You aren't on patrol currently.")
        
        else:
            executor_id = executor.id

            cursor = await self.client.db.execute(f"SELECT * FROM patrol WHERE id='{executor_id}'")
            data = await cursor.fetchone()
            if data == None:
                await cursor.close()
                return await ctx.send(f"<:RO_error:773206804758790184> \"{executor.display_name}\" matches no record in the moderator database.")
            else:
                raw_starttime = data[2]
                patrolling_status = data[3]
                await cursor.close()

            if patrolling_status == True:
                current_time = time.time()
                time_elapsed_yet = current_time - raw_starttime
                await ctx.send(f"<:RO_time:773207335396573226> **{executor.display_name}** has been patrolling for **`{time_convert_mod(time_elapsed_yet)}`**")
            else:
                await ctx.send(f"<:RO_error:773206804758790184> **{executor.display_name}** isn't on patrol currently.")

    @commands.command(name = "onpatrol")
    @commands.guild_only()
    
    #@commands.has_any_role(Roles.senior_moderator, Roles.lead_moderator, Roles.board_of_directors, Roles.assistant_director, Roles.director, Roles.advisor, Roles.lead_moderator)
    @commands.cooldown(1,0.5,commands.BucketType.user)
    async def onpatrol(self, ctx):
        guild = self.client.get_guild(427007974947553280)
        #-----------------------------------------------------------------
        cursor = await self.client.db.execute(f"SELECT id FROM patrol WHERE status=True")
        data = await cursor.fetchall()
        if len(data) == 0:
            await cursor.close()
            return await ctx.send("<:RO_error:773206804758790184> No moderators are currently on patrol :(")
        else:
            online_mods_tup = data
            await cursor.close()
        #-----------------------------------------------------------------
        embed=discord.Embed(title="On-Patrol Moderators‎", color=0xfcfcfc, timestamp = discord.utils.utcnow())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar)
        mod = guild.get_role(Roles.moderator)
        srmod = guild.get_role(Roles.senior_moderator)
        probmod = guild.get_role(Roles.probationary_moderator)
        leadmod = guild.get_role(Roles.lead_moderator)
        bod = guild.get_role(Roles.board_of_directors)
        ADcheck = True
        for logged_user in online_mods_tup:
            online_mod = guild.get_member(int(logged_user[0]))
            if mod in online_mod.roles : 
                modrank = "Moderator"
                ADcheck = False
            if probmod in online_mod.roles :
                modrank = "Probationary Moderator"
                ADcheck = False
            if srmod in online_mod.roles :
                modrank = "Senior Moderator"
                ADcheck = False
            if leadmod in online_mod.roles :
                modrank = "Lead Moderator"
                ADcheck = False
            if bod in online_mod.roles : 
                modrank = "Board of Directors"
                ADcheck = False
            if ADcheck == True:
                modrank = "Assistant Director+"

            mod_status = str(online_mod.status)
            if mod_status=="dnd" or mod_status=="do_not_disturb":
                mod_status_emoji = "<:status_dnd:812363317988687872>"
            elif mod_status=="offline":
                mod_status_emoji = "<:status_offline:812363250939199558> "
            elif mod_status=="idle":
                mod_status_emoji = "<:status_idle:812363298116599858> "
            elif mod_status=="online":
                mod_status_emoji = "<:status_online:812363218080104448> "
            elif mod_status=="streaming":
                mod_status_emoji = "<:status_streaming:812363393897594920>"

            embed.add_field(name=online_mod.display_name, value=f"{mod_status_emoji} | {modrank} | ID: {online_mod.id}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name = "cancelpatrol")
    @commands.guild_only()
    @commands.has_any_role(Roles.lead_moderator, Roles.board_of_directors, Roles.director, Roles.assistant_director, Roles.advisor, Roles.senior_moderator)
    @commands.cooldown(1,2.5,commands.BucketType.user)
    async def cancelpatrol(self, ctx, victim : discord.Member, *, reason=None):
        guild = self.client.get_guild(427007974947553280)
        patrolchannel = self.client.get_channel(696133524167720970)
        victim_id = victim.id
        #-----------------------------------------------------------------
        cursor = await self.client.db.execute(f"SELECT * FROM patrol WHERE id='{victim_id}'")
        data = await cursor.fetchone()
        if data == None:
            await cursor.close()
            return await ctx.send(f"<:RO_error:773206804758790184> That record is not in the moderator database.")
        else:
            raw_starttime = data[2]
            patrolling_status = data[3]
            original_strt_msgid = data[4]
            raw_commentslog = eval(data[5])
            t_cancelled_patrols = data[9]
            sum_patroltime = data[10]
            prev_patrols = eval(data[11])
            await cursor.close()
        #-----------------------------------------------------------------
        if patrolling_status == True:
            raw_endtime = time.time()
            if reason==None:
                reason="N/A"
            else:
                reason=reason
            original_strt_msg = await patrolchannel.fetch_message(original_strt_msgid)
            embed=discord.Embed(title="‎[RATA] Moderation Patrol Cancelled", description=f"__**Moderator**__\n{victim.mention}", color=0x949494)
            embed.set_author(name=victim.display_name, icon_url=victim.avatar)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
            embed.add_field(name="Start Time:", value=f"<t:{round(raw_starttime)}:f>", inline=True)
            embed.add_field(name="Cancellation Time:", value=f"<t:{round(raw_endtime)}:f>", inline=True)
            if len(raw_commentslog)>1:
                comments = ""
                for i in range(1,len(raw_commentslog)):
                    if i==1:
                        if isinstance(raw_commentslog[i], dict):
                            time_str = ', '.join(raw_commentslog[i]['ias'])
                            comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                            comments = "◉"+" "+comment_sep+time_str
                            continue
                        comment_sep = str(raw_commentslog[i])
                        comments = "◉"+" "+comment_sep
                        continue
                    if i>1:
                        if isinstance(raw_commentslog[i], dict):
                            time_str = ', '.join(raw_commentslog[i]['ias'])
                            comment_sep = '**`🚨[IAS REPORT]`** Successfully confirmed presence after period of inactivity at '
                            comments = comments+"\n"+"◉"+" "+comment_sep+time_str
                            continue
                        comment_sep = str(raw_commentslog[i])
                        comments = comments+"\n"+"◉"+" "+comment_sep
                        continue
                embed.add_field(name="Patrol Comments", value=f"{comments}", inline=False)
            elif len(raw_commentslog)==1:
                embed.add_field(name="Patrol Comments", value="No comments added.", inline=False)
            embed.add_field(name="Cancelled by:", value=ctx.author.mention, inline=True)
            embed.add_field(name="Reason:", value=reason, inline=True)
            embed.add_field(name="Total Patrolling Minutes", value=f"{time_convert_mod(raw_endtime - raw_starttime)}", inline=False)
            await original_strt_msg.edit(content=victim.mention, embed=embed)
            embed2=discord.Embed(title="Your RATA Moderator Patrol was cancelled",description=f"**{ctx.author.display_name}** has cancelled your patrol with the reason being :\n`{reason}`\n\nView the [Cancellation Report]({original_strt_msg.jump_url}) for more information.",color=0xff0f0f)
            embed2.set_footer(text="Robloxian Adventures Training Academy", icon_url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
            await victim.send(embed=embed2)
            await ctx.send(f"<:RO_success:773206804850016276> The patrol by **{victim.display_name}** has been successfully cancelled.")
            
            del self.client.activityDB[victim_id]
            t_cancelled_patrols +=1

            await self.client.db.execute(f"UPDATE patrol SET starttime=Null, status=False, startmsg_id=Null, commentslog='{{}}', t_cancelled_patrols={t_cancelled_patrols}, next_ias=Null WHERE id={victim_id}")
            await self.client.db.commit()
            
        elif patrolling_status == False:
            member = guild.get_member(victim_id)
            await ctx.send(f"<:RO_error:773206804758790184> {member.display_name} is not on-patrol currently.")

    @cancelpatrol.error
    async def cancelpatrol_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send("<a:RO_alert:773211228373647360> User was not found. Please ensure you are using either complete discord username (abc#1234), their @ mention or their user ID.")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("<a:RO_alert:773211228373647360> Missing necessary argument.\n```\nr.cancelpatrol <user> <optional_reason>\n```")    
            
    @commands.command(name = "dm_alerts")
    @commands.guild_only()
    @commands.check(inmodcmds)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def dm_alerts(self, ctx):
        #-----------------------------------------------------------------
        cursor = await self.client.db.execute(f"SELECT ias_dm_toggle FROM patrol WHERE id='{ctx.author.id}'")
        data = await cursor.fetchone()
        if data == None:
            await cursor.close()
            return await ctx.send(f"<:RO_error:773206804758790184> Your record is not in the moderator database.")
        else:
            ias_dm_toggle = data[0]
            await cursor.close()
        #-----------------------------------------------------------------
        if ias_dm_toggle:
            embed = discord.Embed(title=f'Currently you have IAS DM alerts toggle ON', description='Would you like to turn off this toggle?',colour=0xFFA500).set_footer(text="Prompt times out in 60 seconds.")
            view = OFF_DMAlertsView(ctx.author)
            askingMsg = await ctx.reply(embed=embed,view=view)
            await view.wait()
            if view.value == True:
                await self.client.db.execute(f"UPDATE patrol SET ias_dm_toggle=False WHERE id={ctx.author.id}")
                await self.client.db.commit()
                return await askingMsg.edit(embed=discord.Embed(title="IAS DM alerts toggle is now OFF", colour=0xFFA500), view=None)
            elif view.value == False:
                return await askingMsg.edit(embed=discord.Embed(title="Prompt cancelled", colour=0xFFA500), view=None)
            else:
                return await askingMsg.edit(embed=discord.Embed(title="Prompt timed out.", colour=0xFF0000), view=None)

        else:
            embed = discord.Embed(title=f'Currently you have IAS DM alerts toggle OFF', description='Would you like to turn on this toggle?\n\nThis toggle will make it so that the bot will DM you if you do not respond to a IAS trigger after 60 seconds of it being issued.',colour=0xFFA500).set_footer(text="Prompt times out in 60 seconds.")
            view = ON_DMAlertsView(ctx.author)
            askingMsg = await ctx.reply(embed=embed,view=view)
            await view.wait()
            if view.value == True:
                await self.client.db.execute(f"UPDATE patrol SET ias_dm_toggle=True WHERE id={ctx.author.id}")
                await self.client.db.commit()
                return await askingMsg.edit(embed=discord.Embed(title="IAS DM alerts toggle is now ON", colour=0xFFA500), view=None)
            elif view.value == False:
                return await askingMsg.edit(embed=discord.Embed(title="Prompt cancelled", colour=0xFFA500), view=None)
            else:
                return await askingMsg.edit(embed=discord.Embed(title="Prompt timed out.", colour=0xFF0000), view=None)
                    
    @commands.command(name = "patrolstats")
    @commands.guild_only()
    @commands.check(inmodcmds)
    @commands.cooldown(1,2,commands.BucketType.user)
    async def patrolstats(self,ctx, user : discord.Member = None):
        if user == None:
            mod = ctx.author
        else:
            mod = user
        #-----------------------------------------------------------------
        cursor = await self.client.db.execute(f"SELECT t_patrols, t_full_patrols, t_cancelled_patrols, sum_patroltime, prev_patrols FROM patrol WHERE id='{mod.id}'")
        data = await cursor.fetchone()
        if data == None:
            await cursor.close()
            if mod != ctx.author:
                return await ctx.reply("<:RO_error:773206804758790184> That user's record is not in the moderator database.")
            else:
                return await ctx.reply("<:RO_error:773206804758790184> Your record is not in the moderator database.")

        else:
            t_patrols = data[0]
            t_full_patrols = data[1]
            t_cancelled_patrols = data[2]
            sum_patroltime = data[3]
            prev_patrols = eval(data[4])
            await cursor.close()
        #-----------------------------------------------------------------
        if t_patrols == 0:
            if mod != ctx.author:
                return await ctx.reply('<:RO_error:773206804758790184> That user has no patrols that were recorded yet.')
            else:
                return await ctx.reply('<:RO_error:773206804758790184> You have no patrols that were recorded yet.')
        
        embed = discord.Embed(title="Moderator Patrol Stats").set_author(name=mod.display_name,icon_url=mod.avatar)

        post_data = {'chart': {'type': 'pie', 'data': {'labels': ['Completed', 'Cancelled'],
        "datasets": [{"data": [t_full_patrols, t_cancelled_patrols],"backgroundColor": ['rgb(75, 192, 192)','rgb(255, 99, 132)',], "label": 'Patrols'}]}}}
        async with aiohttp.ClientSession() as session:
            async with session.post("https://quickchart.io/chart/create", json=post_data) as resp:
                if resp.status == 200:
                    data = json.loads(await resp.read())
                    embed.set_thumbnail(url=data['url'])
        
        data_labels = []
        count = 0
        for i in range(0, len(prev_patrols)):
            prev_patrols[i] = prev_patrols[i] / 60
            data_labels.insert(0, f'Patrol {t_patrols - count}')
            count+=1

        post_data2 = {'chart': {"type": 'line',"data": {"labels": data_labels,
        "datasets": [{"backgroundColor": 'rgba(255, 99, 132, 0.5)',"borderColor": 'rgb(255, 99, 132)',"data": prev_patrols,"label": 'Patrolling Minutes',"fill": 'origin'}]},"options": {"title": {"text": 'Total Patrol Time Pattern',"display": True}}}}

        async with aiohttp.ClientSession() as session:
            async with session.post("https://quickchart.io/chart/create", json=post_data2) as resp:
                if resp.status == 200:
                    data = json.loads(await resp.read())
                    embed.set_image(url=data['url'])
        
        embed.add_field(name='Total Initiated Patrols',value=f'{t_patrols}', inline=True)
        embed.add_field(name='Total Completed Patrols',value=f'{t_full_patrols}', inline=True)
        embed.add_field(name='Total Cancelled Patrols',value=f'{t_cancelled_patrols}', inline=True)
        avg = display_time(sum_patroltime / t_patrols) or "-"
        embed.add_field(name='Average Patrol Time',value=f"{avg}")
        cancel_perc = round(((t_cancelled_patrols / t_patrols) * 100), 2)
        embed.add_field(name='Cancellation Rate',value=f"{cancel_perc}%")
        await ctx.reply(embed=embed)
        
    @commands.command(name="rule")
    @commands.guild_only()
    @commands.has_any_role(Roles.moderator, Roles.senior_moderator, Roles.lead_moderator, Roles.board_of_directors, Roles.director, Roles.assistant_director)
    async def rule(self, ctx, ruleinput : str):
        try:
            await ctx.reply(rules[ruleinput.upper().replace(' ','')])
        except KeyError:
            await ctx.reply(f'No rule with rule number **`{ruleinput}`** found.')
    
    @commands.command(name='checkquota')
    @commands.guild_only()
    @commands.has_any_role(Roles.moderator, Roles.senior_moderator, Roles.lead_moderator, Roles.board_of_directors, Roles.director, Roles.assistant_director)
    async def checkquota(self, ctx, user : discord.Member = None):   
        msg = await ctx.reply(embed=discord.Embed(description='*Fetching...*'))
        agc = await agcm.authorize()
        g_sheet = await agc.open_by_key("1Cwi5qBuI0kG1DEQZ605Nl_qBRFFyvxMoDv4U_U6DmyQ")
        g_worksheet = await g_sheet.worksheet("Activity Record")   
        if user == None:
            actualName = deEmojify(str(ctx.author.display_name)).split()[-1].replace(" ","")
            try:
                foundName = await g_worksheet.find(actualName)
            except:
                return await msg.edit(content=f'**SPREADSHEET ERROR:** `{actualName}` not found')
            sunday_min = int((await g_worksheet.cell(foundName.row, 4)).value or 0)
            monday_min = int((await g_worksheet.cell(foundName.row, 5)).value or 0)
            tuesday_min = int((await g_worksheet.cell(foundName.row, 6)).value or 0)
            wednesday_min = int((await g_worksheet.cell(foundName.row, 7)).value or 0)
            thursday_min = int((await g_worksheet.cell(foundName.row, 8)).value or 0)
            friday_min = int((await g_worksheet.cell(foundName.row, 9)).value or 0)
            saturday_min = int((await g_worksheet.cell(foundName.row, 10)).value or 0)
            patrol_days = 0
            for i in [sunday_min,monday_min,tuesday_min,wednesday_min,thursday_min,friday_min,saturday_min]:
                if i != 0:
                    patrol_days +=1
            total_mins = sum([sunday_min,monday_min,tuesday_min,wednesday_min,thursday_min,friday_min,saturday_min])
            try:
                avg_min = round(total_mins/patrol_days,2)       
            except ZeroDivisionError:
                avg_min = 0
            embed = discord.Embed(title="Moderator Quota", description=f"> Sunday: `{int(sunday_min)}`\n> Monday: `{int(monday_min)}`\n> Tuesday: `{int(tuesday_min)}`\n> Wednesday: `{wednesday_min}`\n> Thursday: `{thursday_min}`\n> Friday: `{friday_min}`\n> Saturday: `{saturday_min}`", colour = ctx.author.color)
            embed.add_field(name="Avg. Patrolling Time",value=str(round(avg_min))+" mins")
            embed.add_field(name="Patrolling Days",value=str(patrol_days))
            embed.add_field(name="Total Patrolling Time",value=str(total_mins)+" mins")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
            embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar)
            await msg.edit(embed=embed)
        else:
            actualName = deEmojify(str(user.display_name)).split()[-1].replace(" ","")
            try:
                foundName = await g_worksheet.find(actualName)
            except:
                return await msg.edit(content=f'**SPREADSHEET ERROR:** `{actualName}` not found')
            sunday_min = int((await g_worksheet.cell(foundName.row, 4)).value or 0)
            monday_min = int((await g_worksheet.cell(foundName.row, 5)).value or 0)
            tuesday_min = int((await g_worksheet.cell(foundName.row, 6)).value or 0)
            wednesday_min = int((await g_worksheet.cell(foundName.row, 7)).value or 0)
            thursday_min = int((await g_worksheet.cell(foundName.row, 8)).value or 0)
            friday_min = int((await g_worksheet.cell(foundName.row, 9)).value or 0)
            saturday_min = int((await g_worksheet.cell(foundName.row, 10)).value or 0)

            patrol_days = 0
            for i in [sunday_min,monday_min,tuesday_min,wednesday_min,thursday_min,friday_min,saturday_min]:
                if i != 0:
                    patrol_days +=1
            total_mins = sum([sunday_min,monday_min,tuesday_min,wednesday_min,thursday_min,friday_min,saturday_min])
            try:
                avg_min = round(total_mins/patrol_days,2)       
            except ZeroDivisionError:
                avg_min = 0
            embed = discord.Embed(title="Moderator Quota", description=f"> Sunday: `{int(sunday_min)}`\n> Monday: `{int(monday_min)}`\n> Tuesday: `{int(tuesday_min)}`\n> Wednesday: `{wednesday_min}`\n> Thursday: `{thursday_min}`\n> Friday: `{friday_min}`\n> Saturday: `{saturday_min}`", colour = user.color)
            embed.add_field(name="Avg. Patrolling Time",value=str(round(avg_min))+" mins")
            embed.add_field(name="Patrolling Days",value=str(patrol_days))
            embed.add_field(name="Total Patrolling Time",value=str(total_mins)+" mins")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
            embed.set_author(name=user.display_name,icon_url=user.avatar)
            await msg.edit(embed=embed)

async def setup(client):
    await client.add_cog(PatrolCog(client))