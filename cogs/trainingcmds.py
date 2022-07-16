import discord
from discord.ext import commands, tasks
import gspread_asyncio
import asyncio
import time, datetime
from dateutil import tz
import re

from google.oauth2.service_account import Credentials

def get_creds():
    creds = Credentials.from_service_account_file("/home/container/cogs/JSON credentials/credentials_training.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

def intrainingcmds(ctx):
    return ctx.channel.id == 773979094940385330

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

def onDay(date, day):
    if date.weekday() == 0: # If date given is the same as required date
        return 0
    days = (day - date.weekday() + 7) % 7
    return (date + datetime.timedelta(days=days)).replace(hour=0,minute=0,second=0,microsecond=0)
# ------------------------------------
# Button Classes

class askPollTiersView(discord.ui.View):
    def __init__(self, author : discord.Member, *, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = []
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return True
        else:
            return False 

    @discord.ui.button(label='Tier 1', style=discord.ButtonStyle.gray)
    async def t1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]
        if embed.description:
            embed.description += "\n ```ml\nTier 1\n```"
        else:
            embed.description = "\n ```ml\nTier 1\n```"
        button.disabled=True
        await interaction.response.edit_message(content="", embed=embed, view=self)
        self.value.append(1)
    @discord.ui.button(label='Tier 2', style=discord.ButtonStyle.gray)
    async def t2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]
        if embed.description:
            embed.description += "\n ```ml\nTier 2\n```"
        else:
            embed.description = "\n ```ml\nTier 2\n```"
        button.disabled=True
        await interaction.response.edit_message(content="", embed=embed, view=self)
        self.value.append(2)
    @discord.ui.button(label='Tier 3', style=discord.ButtonStyle.gray)
    async def t3(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]
        if embed.description:
            embed.description += "\n ```ml\nTier 3\n```"
        else:
            embed.description = "\n ```ml\nTier 3\n```"
        button.disabled=True
        await interaction.response.edit_message(content="", embed=embed, view=self)
        self.value.append(3)
    @discord.ui.button(label='Tier 4', style=discord.ButtonStyle.gray)
    async def t4(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]
        if embed.description:
            embed.description += "\n ```ml\nTier 4\n```"
        else:
            embed.description = "\n ```ml\nTier 4\n```"
        button.disabled=True
        await interaction.response.edit_message(content="", embed=embed, view=self)
        self.value.append(4)
    @discord.ui.button(label='Continue', style=discord.ButtonStyle.green, emoji="⏩")
    async def cont(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]
        embed.colour = discord.Colour.green()
        embed.set_footer(text=None)
        await interaction.response.edit_message(content="", embed=embed, view=None)
        self.stop()

class PollShoutConfirmationView(discord.ui.View):
    def __init__(self, author : discord.Member, *, timeout=600):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return True
        else:
            return False 
    
    @discord.ui.button(label='Announce Poll', style=discord.ButtonStyle.gray, emoji='<:yes:614538082774941716>')
    async def announce(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='<:no:614538096704487425>')
    async def abort(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

class TrainingShoutConfirmationView(discord.ui.View):
    def __init__(self, author : discord.Member, *, timeout=600):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return True
        else:
            return False 
    
    @discord.ui.button(label='Announce Training', style=discord.ButtonStyle.gray, emoji='<:yes:614538082774941716>')
    async def announce(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(label='Abort Training', style=discord.ButtonStyle.gray, emoji='<:no:614538096704487425>')
    async def abort(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()



class TierButton(discord.ui.Button):
    def __init__(self, label, *, dictionary={}):
        super().__init__(style=discord.ButtonStyle.secondary, label=label)
        self.label = label
        self.dictionary = dictionary
        self.votes = 0

    async def callback(self, interaction: discord.Interaction):
        rolesID = []
        for role in interaction.user.roles:
            rolesID.append(role.id)
        
        if interaction.user.id not in self.dictionary:
            if self.label=='Tier 1':
                if 516976454731563020 in rolesID:
                    embed = interaction.message.embeds[0]
                    fieldIndex = 0
                    voterNames = ""
                    for field in embed.fields:
                        if field.name.startswith('Tier 1'):
                            voterNames = field.value
                            if voterNames.startswith('*'):
                                voterNames = ''
                            try:
                                voterNames += (interaction.user.display_name).split(" | ")[1] + "\n"
                            except IndexError:
                                return await interaction.response.send_message("<:RO_error:773206804758790184> Please use /getroles to update your nickname into the correct format.")
                            break
                        fieldIndex += 1 
                    self.votes += 1
                    embed.set_field_at(fieldIndex, name=self.label + f" ({self.votes} votes)", value=voterNames)
                    self.dictionary[interaction.user.id] = self.label
                    await interaction.response.edit_message(embed = embed, view = self.view)
                    await interaction.followup.send("<:RO_success:773206804850016276> Your vote has been recorded as " + self.label, ephemeral = True)
                else:
                    return await interaction.response.send_message("<:RO_error:773206804758790184> You do not have the required role to vote for this tier.", ephemeral = True)
            
            elif self.label=='Tier 2':
                if 516976276201013261 in rolesID:
                    embed = interaction.message.embeds[0]
                    fieldIndex = 0
                    voterNames = ""
                    for field in embed.fields:
                        if field.name.startswith('Tier 2'):
                            voterNames = field.value
                            if voterNames.startswith('*'):
                                voterNames = ''
                            try:
                                voterNames += (interaction.user.display_name).split(" | ")[1] + "\n"
                            except IndexError:
                                return await interaction.response.send_message("<:RO_error:773206804758790184> Please use /getroles to update your nickname into the correct format.", ephemeral = True)
                            break
                        fieldIndex += 1 
                    self.votes += 1
                    embed.set_field_at(fieldIndex, name=self.label + f" ({self.votes} votes)", value=voterNames)
                    self.dictionary[interaction.user.id] = self.label
                    await interaction.response.edit_message(embed = embed, view = self.view)
                    await interaction.followup.send("<:RO_success:773206804850016276> Your vote has been recorded as " + self.label, ephemeral = True)
                else:
                    return await interaction.response.send_message("<:RO_error:773206804758790184> You do not have the required role to vote for this tier.", ephemeral = True)
            
            elif self.label=='Tier 3':
                if 516976069027430401 in rolesID:
                    embed = interaction.message.embeds[0]
                    fieldIndex = 0
                    voterNames = ""
                    for field in embed.fields:
                        if field.name.startswith('Tier 3'):
                            voterNames = field.value
                            if voterNames.startswith('*'):
                                voterNames = ''
                            try:
                                voterNames += (interaction.user.display_name).split(" | ")[1] + "\n"
                            except IndexError:
                                return await interaction.response.send_message("<:RO_error:773206804758790184> Please use /getroles to update your nickname into the correct format.")
                            break
                        fieldIndex += 1 
                    self.votes += 1
                    embed.set_field_at(fieldIndex, name=self.label + f" ({self.votes} votes)", value=voterNames)
                    self.dictionary[interaction.user.id] = self.label
                    await interaction.response.edit_message(embed = embed, view = self.view)
                    await interaction.followup.send("<:RO_success:773206804850016276> Your vote has been recorded as " + self.label, ephemeral = True)
                else:
                    return await interaction.response.send_message("<:RO_error:773206804758790184> You do not have the required role to vote for this tier.", ephemeral = True)
            
            elif self.label=='Tier 4':
                if 516975850764238858 in rolesID:
                    embed = interaction.message.embeds[0]
                    fieldIndex = 0
                    for field in embed.fields:
                        if field.name.startswith('Tier 4'):
                            voterNames = field.value
                            if voterNames.startswith('*'):
                                voterNames = ''
                            try:
                                voterNames += (interaction.user.display_name).split(" | ")[1] + "\n"
                            except IndexError:
                                return await interaction.response.send_message("<:RO_error:773206804758790184> Please use /getroles to update your nickname into the correct format.")
                            break
                        fieldIndex += 1 
                    self.votes += 1
                    embed.set_field_at(fieldIndex, name=self.label + f" ({self.votes} votes)", value=voterNames)
                    self.dictionary[interaction.user.id] = self.label
                    await interaction.response.edit_message(embed = embed, view = self.view)
                    await interaction.followup.send("<:RO_success:773206804850016276> Your vote has been recorded as " + self.label, ephemeral = True)
                else:
                    return await interaction.response.send_message("<:RO_error:773206804758790184> You do not have the required role to vote for this tier.", ephemeral = True)


class TierPoll(discord.ui.View):    
    def __init__(self, thread, buttonList):
        super().__init__(timeout = 60) #TODO: change to 600 on deployment pls
        self.thread = thread
        self.winningTier = None
        for button in buttonList:
            self.add_item(button)
    
    async def on_timeout(self):
        pollResultsMsg = (await self.message.channel.fetch_message(self.message.id)).embeds[0]
        winningTierDict = {'name': None, 'amount':0}
        for field in pollResultsMsg.fields:
            try:
                if int(field.name[8]) > winningTierDict['amount']:
                    winningTierDict['name'] = field.name[:6]
                    winningTierDict['amount'] = int((field.name[8:]).strip(' votes)'))
                    continue
            except IndexError:
                continue

            #DUPE CHECKR ----------------------------
            """
            if list(total.values()).count(win['a']) >= 2:
    win['n'] = [i for i in total.keys() if total[i] == win['a']]
    print(win)
    print('ayo dupe')"""
        
        self.winningTier = winningTierDict
        pollResultsMsg.colour = discord.Colour.red()
        pollResultsMsg.description = 'Voting has ended!\n\n*Awaiting instructor\'s further action...*\n\n🔒 **VOTING CHART**'
        await self.message.edit(embed=pollResultsMsg, view=None)
        self.stop()

# ------------------------------------

class TrainingCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.newWeekAlertTask.start()

    @commands.Cog.listener()
    async def on_ready(self):
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Training Commands cog healthy.")
    
    @tasks.loop(hours=168) 
    async def newWeekAlertTask(self):
        hostlogsChannel = self.client.get_channel(486233755439333377)
        weekStart = datetime.datetime.now(tz.gettz('Etc/Greenwich'))
        weekStart_f = weekStart.strftime("%d/%m/%y")
        weekEnd = weekStart + datetime.timedelta(days=7)
        weekEnd_f = weekEnd.strftime("%d/%m/%y")
        embed = discord.Embed(description=f"<:RATAcleanlogo:739164550862995502> **New week `{weekStart_f}` - `{weekEnd_f}`**", colour=discord.Color.blue())
        await hostlogsChannel.send(embed=embed)

    @newWeekAlertTask.before_loop
    async def wait_until_monday(self):
        await self.client.wait_until_ready()

        now = datetime.datetime.now(tz.gettz('Etc/Greenwich'))
        next_run = onDay(now, 0)

        if next_run == None:
            now += datetime.timedelta(days=1)
            next_run = onDay(now, 0)

        await discord.utils.sleep_until(next_run)

    @commands.command(name="host")
    @commands.check(intrainingcmds)
    @commands.is_owner() #TODO: remove
    @commands.cooldown(1,2.5,commands.BucketType.user)
    async def host(self, ctx):
        guild = self.client.get_guild(427007974947553280)
        host = guild.get_member(ctx.author.id)
        beginMsg = await ctx.reply('<:RO_success:773206804850016276> Join the thread to view the training UI!')
        thread = await ctx.channel.create_thread(name="⚪"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(host.display_name)))))+"'s training", auto_archive_duration=1440, type=discord.ChannelType.private_thread, message=beginMsg)
        await thread.add_user(host)
        pollview = askPollTiersView(host)
        embed = discord.Embed(title="What tiers would you like to do a poll over?", description="", colour = discord.Color.green()).set_footer(text="Times out in 60 seconds")
        askTierPollsMsg = await thread.send(embed=embed,view=pollview)
        await pollview.wait()
        tiersVotingOver = pollview.value
        if tiersVotingOver == []:
            await askTierPollsMsg.reply('Prompt timed out, thread will be deleted in 5 minutes.')
            await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(host.display_name)))))+"'s training")
            await asyncio.sleep(300)
            return await thread.delete()
        embed = (await thread.fetch_message(askTierPollsMsg.id)).embeds[0]
        embed.title = "Click to announce the poll whenever you're ready"
        embed.description += "\nPress <:no:614538096704487425> to abort it."
        view = PollShoutConfirmationView(ctx.author)
        await askTierPollsMsg.edit(embed=embed, view=view)
        await view.wait()
        if view.value == False:
            await thread.send("Training Aborted, thread will be deleted in 5 minutes.")
            await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(host.display_name)))))+"'s training")
            await asyncio.sleep(300)
            return await thread.delete()
        elif view.value == None:
            await askTierPollsMsg.reply('Prompt timed out, thread will be deleted in 5 minutes.')
            await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(host.display_name)))))+"'s training")
            await asyncio.sleep(300)
            return await thread.delete()
        
        if len(tiersVotingOver) > 1:
            embed=discord.Embed(description="<a:loading:973263527458533396> **Poll announced, awaiting trainee votes...**")
            pollLoadingMsg = await askTierPollsMsg.edit(embed=embed, view=None)
            shoutsChannel = guild.get_channel(773979094940385330)
            embed = discord.Embed(title="TIER TRAINING VOTE", description=f"> Please vote on what training you want.\n> Please only vote for your tier if you are able to attend.\n> To vote simply click on the buttons below!\n\nIf you vote, yet do not attend, you will recieve a warning. \n\nVoting ends <t:{str(round(time.time()) + 600)}:R>!\n\n**VOTING CHART**")
            buttonList = []
            if 1 in tiersVotingOver:
                embed.add_field(name="Tier 1", value="*No votes yet*", inline=True)
                buttonList.append(TierButton('Tier 1'))
            if 2 in tiersVotingOver:
                embed.add_field(name="Tier 2", value="*No votes yet*", inline=True)
                buttonList.append(TierButton('Tier 2'))
            if 3 in tiersVotingOver:
                embed.add_field(name="Tier 3", value="*No votes yet*", inline=True)
                buttonList.append(TierButton('Tier 3'))
            if 4 in tiersVotingOver:
                embed.add_field(name="Tier 4", value="*No votes yet*", inline=True)
                buttonList.append(TierButton('Tier 4'))
            
            view = TierPoll(thread, buttonList)
            view.message = await shoutsChannel.send(embed=embed, view=view)
            tierPollMsg = view.message
            await view.wait()
            await asyncio.sleep(5)
            chosenTier = view.winningTier
            if chosenTier['name'] == None:
                pass #TODO: handle no votes situation
            embed = discord.Embed(title='Tier Voting Results', description=f'**{chosenTier["name"]}** has won the voting with {chosenTier["amount"]} votes!\n\nPlease choose your next action')
            view = TrainingShoutConfirmationView(ctx.author)
            await pollLoadingMsg.delete()
            await thread.send(content=host.mention, embed=embed, view=view)
            await view.wait()
            if view.value == False:
                await thread.send("Training Aborted, thread will be deleted in 5 minutes.")
                await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(host.display_name)))))+"'s training")
                await tierPollMsg.edit
                await asyncio.sleep(300)
                return await thread.delete()
            elif view.value == None:
                await askTierPollsMsg.reply('Prompt timed out, thread will be deleted in 5 minutes.')
                await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(host.display_name)))))+"'s training")
                await asyncio.sleep(300)
                return await thread.delete()
            
            



async def setup(client):
    await client.add_cog(TrainingCog(client))