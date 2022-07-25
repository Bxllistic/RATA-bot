import discord
from discord.ext import commands
import time
import random
import asyncio
import googletrans
from bot_utils.roleId import Roles
import re

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

class YesorNoView(discord.ui.View):
    def __init__(self, author : discord.Member, *, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return True
        else:
            return False 
    
    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='<:yes:614538082774941716>')
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='<:no:614538096704487425>')
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

class ConfirmationView(discord.ui.View):
    def __init__(self, author : discord.Member, *, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return True
        else:
            return False 
    
    @discord.ui.button(label='Issue strike', style=discord.ButtonStyle.gray, emoji='<:yes:614538082774941716>')
    async def announce(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji='<:no:614538096704487425>')
    async def abort(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

class DepartmentSelectionView(discord.ui.View):
    def __init__(self, author : discord.Member, *, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return True
        else:
            return False 
    
    @discord.ui.button(label='Training', style=discord.ButtonStyle.gray, emoji='<:training_icon:997466440930181200>')
    async def training(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'training'
        self.stop()

    @discord.ui.button(label='Moderation', style=discord.ButtonStyle.gray, emoji='<:moderation_icon:997466994569916466>')
    async def moderation(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'moderation'
        self.stop()

    @discord.ui.button(label='General', style=discord.ButtonStyle.gray, emoji='<:incident_investigating:812365502365564969>')
    async def general(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'general'
        self.stop()


class ModerationCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.translator = googletrans.Translator()
   
    @commands.Cog.listener()
    async def on_ready(self):
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Moderation cog healthy.")
        
    @commands.command(name='translate')
    @commands.has_permissions(manage_messages=True)
    async def translate(self, ctx, *, source : str = None):
        if ctx.message.reference != None:
            try:
                msg = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            except:
                return await ctx.reply('Could not fetch message.')
            if msg.content == "":
                return await ctx.reply('The message referenced had no content.')
            output = self.translator.translate(msg.content)
            detect_output = self.translator.detect(msg.content)
            embed = discord.Embed(title='Translation Output', description='‎‎‎‎', colour = 0x21bfeb)
            embed.add_field(name=f'Source - {googletrans.LANGUAGES[output.src.lower()].title()} [{output.src.upper()}]', value=f"```\n{output.origin}\n```", inline=False)
            embed.add_field(name=f'Result - {googletrans.LANGUAGES[output.dest.lower()].title()} [{output.dest.upper()}]', value=f"```\n{output.text}\n```", inline=False)
            if isinstance(detect_output.confidence, list):
                if (len(detect_output.confidence) - 1) == 1: 
                    embed.set_footer(text=f'Translation Confidence >> {round(float(detect_output.confidence[0]) * 100, 2)}% (1 other language detected)')
                else:
                     embed.set_footer(text=f'Translation Confidence >> {round(float(detect_output.confidence[0]) * 100, 2)}% ({len(detect_output.confidence) -1} other languages detected)')     
            else:
                embed.set_footer(text=f'Translation Confidence >> {round(float(detect_output.confidence) * 100, 2)}%')
            await msg.reply(embed=embed, mention_author=False)
        else:
            if source == None:
                return await ctx.reply('You need to give me something to translate :rolling_eyes:')
            else:
                source = source
            output = self.translator.translate(source)
            detect_output = self.translator.detect(source)
            embed = discord.Embed(title='Translation Output', description='‎‎‎‎', colour = 0x21bfeb)
            embed.add_field(name=f'Source - {googletrans.LANGUAGES[output.src.lower()].title()} [{output.src.upper()}]', value=f"```\n{output.origin}\n```", inline=False)
            embed.add_field(name=f'Result - {googletrans.LANGUAGES[output.dest.lower()].title()} [{output.dest.upper()}]', value=f"```\n{output.text}\n```", inline=False)
            if isinstance(detect_output.confidence, list):
                if (len(detect_output.confidence) - 1) == 1: 
                    embed.set_footer(text=f'Translation Confidence >> {round(float(detect_output.confidence[0]) * 100, 2)}% (1 other language detected)')
                else:
                     embed.set_footer(text=f'Translation Confidence >> {round(float(detect_output.confidence[0]) * 100, 2)}% ({len(detect_output.confidence) -1} other languages detected)')                   
            else:
                embed.set_footer(text=f'Translation Confidence >> {round(float(detect_output.confidence) * 100, 2)}%')
            await ctx.reply(embed=embed)
        
        
            
    @commands.command(name='warn')
    @commands.is_owner()
    async def warn(self, ctx, violator : discord.Member, rule : str, *, reason : str):
        guild = self.client.get_guild(427007974947553280)
        rules = {   
            "A1": "Be respectful and do not harass members of the group or discord. This includes inside AND outside the server, etc Discord DMs and ROBLOX PMs.",
            "A2": "Chat or use commands in the proper channels. If you’re going to have a public, general conversation you are to talk in the #general-channel. Misusing a channel will result in first a verbal (typed) warning to go to the proper channel; failure to do so will result in a warning.",
            "A3": "Spamming is prohibited in ALL channels of the Robloxian Adventures Discord. Doing this can result in being warned, kicked, or banned based on the severity of the situation.",
            "A4": "Swearing is now allowed but limited and moderated. You’re not allowed to use any racial/offensive slurs or anything to insult someone.",
            "A5": "Do not argue in public chatrooms. This can include provoking and/or targeting. If you want to argue, take it to your DMs.",
            "A6": "Raiding the RA, or any RA affiliated discord servers will result in an immediate ban. You will not be warned. (Ex: RATA, EIC, PO, and S&R).",
            "A7": "Links that break our rules or contain malicious content are not allowed and will be taken down. IP Grabbers are against Discord guidelines.",
            "A8": "You are prohibited from pinging (@ Username) or ( @ role) without a valid reason. Pinging any Board of Directors+ member without a valid reason will result in a warn. If you have a question, we recommend trying to contact the moderators online first.",
            "A9": "Advertising is not allowed. (YOU MAY NOT ADVERTISE THE FOLLOWING: Groups, games, clothing, Discord servers, or giveaways.) DM advertising is also strictly prohibited.",
            "A10": "We do not allow any ‘selfbots.’ Adding bots will result in those accounts being kicked/banned and your main Discord account being kicked/banned.",
            "A11": "Impersonation is a bannable offense here. If you believe someone is impersonating you please contact a Moderator + to resolve the issue.",
            "A12": "Arguing with staff about previous moderation action taken against you, OR A FRIEND, will result in further moderated punishment. You are entitled to ask why moderation was taken against you, but that does not allow you to argue about it.",
            "A13": "Slightly religious, political, or controversial topics are allowed for discussion as long as they do not get out of hand. A moderator will take action if it does.",
            "A14": "Trolling is prohibited at this server. Trolling includes anything that could disrupt any ongoing group operations.",
            "A15": "You may not post/upload cracked programs or programs that are not free for the general public.",
            "A16": "NSFW content is strictly prohibited with 0 tolerance. (links, profile pictures, pictures, videos, etc.)",
            "A17": "You may not expose anyone’s personal information without their consent. This includes, but is not limited to: social media, phone numbers, addresses, face reveals, private family matters, pictures, or videos.",
            "B1": "Playing annoying entertainment, sounds, or music is considered ‘mic spamming.’ If you want to play music, go to the music channel.",
            "B2": "We have music bots for a reason, so do not play music through your microphone.",
            "B3": "Swearing is allowed in voice chats. However, racial slurs, severe insults, and disrespect towards a member (refer to A1) will not be tolerated and is strictly enforced. The same applies to any audio played through music bots.",
            "B4": "Do not spam move into different channels. Discord gives a sound notification when someone joins a voice channel, you are not allowed to spam that notification.",
            "B5": "You are not allowed to use voice changers.",
            "B6": "Recording/streaming other users without their permission is a federal offense. Doing so will result in removal from Robloxian Adventures and the Discord.",
            "B7": "Yelling/screaming into your microphone is not allowed.",
            "C1": "Do not ask for trainings.",
            "C2": "Do not be disruptive during trainings.",
            "C3": "The max amount of spectators in a training is 4. Head Instructor+ do not count as a spectator.",
            "C4": "The use of exploits/hacks at the training facility is strictly prohibited and will result in a blacklist.",
            "C5": "Disrespecting an individual during a training will result in a kick from the training and a discord warning.",
            "C6": "Voting for a training and not attending will result in a warn."
        }
        #-----------------------------------------------------------------
        with open("moderation.txt", "r") as d:
            d.seek(0)
            combined_dicts = list(d.readlines())
            mod_db = eval(str(combined_dicts[0][:-1]))
            strike_db = eval(str(combined_dicts[1]))
        #-----------------------------------------------------------------
        if violator.id not in mod_db.keys():
            if rule.upper() not in rules.keys():
                await ctx.send(f"<:RO_error:773206804758790184> Rule \'**{rule}**\' not found.")
            else:
                embed=discord.Embed(title="Warning Confirmation", description=f"You are about to warn **{violator.display_name}** for the violation of **rule**:\n```css\n{rule.upper()} - {rules[rule.upper()]}\n```with additional **reason**: ```fix\n{reason}\n```\n\nReact with <:RO_success:773206804850016276> or <:RO_error:773206804758790184> appropriately.", color=0xeb6b34)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_footer(text='Expires in 30 seconds - RATA Administration Interface')
                confirm_msg = await ctx.send(embed=embed)
                await confirm_msg.add_reaction("<:RO_success:773206804850016276>")
                await confirm_msg.add_reaction("<:RO_error:773206804758790184>")

                def check(reaction,user):
                    return user == ctx.author and str(reaction.emoji) in ["<:RO_success:773206804850016276>","<:RO_error:773206804758790184>"] 
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await confirm_msg.edit(embed = discord.Embed(description="**Prompt timed out.**",color=0xFF0000).set_author(name=str(ctx.author), icon_url=ctx.author.avatar))
                    await confirm_msg.clear_reaction("<:RO_success:773206804850016276>")
                    await confirm_msg.clear_reaction("<:RO_error:773206804758790184>")
                else:
                    if str(reaction.emoji) == "<:RO_success:773206804850016276>":
                        await confirm_msg.delete(delay=0.0)
                        mod_db[violator.id] = [[rule,reason,None,time.time(),ctx.author.id]]
                        embed_success=discord.Embed(title="Warning Successful", description=f"You have warned **{violator.display_name}** for the violation of rule {rule.upper()}.\n\nRefer to Warning ID : `{time.time()}`", color=0xeb6b34)
                        embed_success.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                        embed_success.set_footer(text=f'Violator ID: {violator.id} - RATA Administration')

                        embed_fail=discord.Embed(title="Warning Successfully logged (DM Failure)", description=f"You have warned **{violator.display_name}** for the violation of rule {rule.upper()} however was not made aware of to the violator due to DM failure.\n\nRefer to Warning ID : `{time.time()}`", color=0xeb6b34)
                        embed_fail.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                        embed_fail.set_footer(text=f'Violator ID: {violator.id} - RATA Administration')

                        embed_dm=discord.Embed(title="You have been warned in [RA] Training Academy Discord", color=0xeb6b34)
                        embed_dm.add_field(name="Rule Violated:",value=f'**[{rule.upper()}]**\n{rules[rule.upper()]}')
                        embed_dm.add_field(name="Reason:",value=f"{reason}")
                        embed_dm.set_footer(text=f'Violator ID: {violator.id} - RATA Administration')
                        try:
                            await violator.send(embed=embed_dm)
                        except:
                            await ctx.send(embed=embed_fail)
                        else:
                            await ctx.send(embed=embed_success)
                        #-------------------------------------------
                        with open("moderation.txt", "r+") as d:
                            d.truncate(0)
                            d.seek(0)
                            dictlist = d.readlines()
                            dictlist.append(f"{str(mod_db)}\n")
                            dictlist.append(f"{str(strike_db)}")
                            d.seek(0)
                            d.writelines(dictlist)
                        #-------------------------------------------
                    elif str(reaction.emoji) == "<:RO_error:773206804758790184>":
                        await confirm_msg.delete(delay=0.0)
                        embed_no=discord.Embed(title="Warning Prompt Cancelled", color=0xeb6b34)
                        embed_no.set_footer(text=f'RATA Administration')
                        await ctx.send(embed=embed_no)
        elif violator.id in mod_db.keys():
            if rule.upper() not in rules.keys():
                await ctx.send(f"<:RO_error:773206804758790184> Rule \'**{rule}**\' not found.")
            else:
                embed=discord.Embed(title="Warning Confirmation", description=f"You are about to warn **{violator.display_name}** for the violation of **rule**:\n```css\n{rule.upper()} - {rules[rule.upper()]}\n```with additional **reason**: ```fix\n{reason}\n```\n\nReact with <:RO_success:773206804850016276> or <:RO_error:773206804758790184> appropriately.", color=0xeb6b34)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_footer(text='Expires in 30 seconds - RATA Administration Interface')
                confirm_msg = await ctx.send(embed=embed)
                await confirm_msg.add_reaction("<:RO_success:773206804850016276>")
                await confirm_msg.add_reaction("<:RO_error:773206804758790184>")

                def check(reaction,user):
                    return user == ctx.author and str(reaction.emoji) in ["<:RO_success:773206804850016276>","<:RO_error:773206804758790184>"] 
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await confirm_msg.edit(embed = discord.Embed(description="**Prompt timed out.**",color=0xFF0000).set_author(name=str(ctx.author), icon_url=ctx.author.avatar))
                    await confirm_msg.clear_reaction("<:RO_success:773206804850016276>")
                    await confirm_msg.clear_reaction("<:RO_error:773206804758790184>")
                else:
                    if str(reaction.emoji) == "<:RO_success:773206804850016276>":
                        await confirm_msg.delete(delay=0.0)
                        mod_db[violator.id].append([rule,reason,None,time.time(),ctx.author.id])
                        embed_success=discord.Embed(title="Warning Successful", description=f"You have warned **{violator.display_name}** for the violation of rule {rule.upper()}.\n\nRefer to Warning ID : `{time.time()}`", color=0xeb6b34)
                        embed_success.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                        embed_success.set_footer(text=f'Violator ID: {violator.id} - RATA Administration')

                        embed_fail=discord.Embed(title="Warning Successfully logged (DM Failure)", description=f"You have warned **{violator.display_name}** for the violation of rule {rule.upper()} however was not made aware of to the violator due to DM failure.\n\nRefer to Warning ID : `{time.time()}`", color=0xeb6b34)
                        embed_fail.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                        embed_fail.set_footer(text=f'Violator ID: {violator.id} - RATA Administration')

                        embed_dm=discord.Embed(title="You have been warned in [RA] Training Academy Discord", color=0xeb6b34)
                        embed_dm.add_field(name="Rule Violated:",value=f'**[{rule.upper()}]**\n{rules[rule.upper()]}')
                        embed_dm.add_field(name="Reason:",value=f"{reason}")
                        embed_dm.set_footer(text=f'Violator ID: {violator.id} - RATA Administration')
                        try:
                            await violator.send(embed=embed_dm)
                        except:
                            await ctx.send(embed=embed_fail)
                        else:
                            await ctx.send(embed=embed_success)
                        #-------------------------------------------
                        with open("moderation.txt", "r+") as d:
                            d.truncate(0)
                            d.seek(0)
                            dictlist = d.readlines()
                            dictlist.append(f"{str(mod_db)}\n")
                            dictlist.append(f"{str(strike_db)}")
                            d.seek(0)
                            d.writelines(dictlist)
                        #-------------------------------------------
                    elif str(reaction.emoji) == "<:RO_error:773206804758790184>":
                        await confirm_msg.delete(delay=0.0)
                        embed_no=discord.Embed(title="Warning Prompt Cancelled", color=0xeb6b34)
                        embed_no.set_footer(text=f'RATA Administration')
                        await ctx.send(embed=embed_no)
    
    
    
    @commands.command(name='strike')
    @commands.has_any_role(Roles.head_instructor, Roles.lead_moderator, Roles.board_of_directors, Roles.advisor, Roles.assistant_director, Roles.director)
    async def strike(self, ctx, staff : discord.Member):
        guild = self.client.get_guild(427007974947553280)
        strikechannel = guild.get_channel(707533786207748161)
        direc = guild.get_role(Roles.director)
        ad = guild.get_role(Roles.assistant_director)
        dogo = guild.get_role(Roles.director_of_group_operations)
        dom = guild.get_role(Roles.director_of_moderation)
        lm = guild.get_role(Roles.lead_moderator)
        head_ins = guild.get_role(Roles.head_instructor)
        beginMsg = await ctx.reply('<:RO_success:773206804850016276> Join the thread to start drafting the strike.')
        thread = await ctx.channel.create_thread(name="⚪"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(staff.display_name)))))+"'s strike", auto_archive_duration=60, type=discord.ChannelType.private_thread, message=beginMsg)
        await thread.add_user(ctx.author)
        embed = discord.Embed(description=f'**What department would you like to strike {staff.mention} in?**')
        embed.set_author(icon_url=staff.display_avatar, name=staff.display_name)
        embed.set_footer(text='RATA Administration - Times out in 60 seconds')
        view = DepartmentSelectionView(ctx.author)
        askDeptMesg = await thread.send(embed=embed, view=view)
        await view.wait()
        dept = view.value
        if view.value == None:
            await askDeptMesg.reply('Prompt timed out, thread will be deleted in 30 seconds.')
            await beginMsg.edit(content='<:no:614538096704487425> **Prompt timed out**')
            await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(staff.display_name)))))+"'s strike")
            await asyncio.sleep(30)
            return await thread.delete()
        embed = discord.Embed(description="**Explain the reason for the strike**\n\nYou may attach screenshots, links and weekly report tables as evidence.")
        embed.set_author(icon_url=staff.display_avatar, name=staff.display_name)
        embed.set_footer(text='RATA Administration - Times out in 5 minutes')
        await askDeptMesg.edit(embed=embed, view=None)
        def check(message):
            return message.author == ctx.author and message.channel.id == thread.id
        try:
            reasonMsg = await self.client.wait_for('message', timeout=300.0, check=check)
        except asyncio.TimeoutError:
            await askDeptMesg.reply('Prompt timed out, thread will be deleted in 30 seconds.')
            await beginMsg.edit(content='<:no:614538096704487425> **Prompt timed out**')
            await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(staff.display_name)))))+"'s strike")
            await asyncio.sleep(30)
            return await thread.delete()
        else:
            reasonMsg_attachmentStr = ""
            if len(reasonMsg.attachments) >= 1:
                for att in reasonMsg.attachments:
                    reasonMsg_attachmentStr += f"> [Attachment]({att.url})\n"
                reasonMsg_attachmentStr = "\n" + reasonMsg_attachmentStr
                reasonMsg_attachmentStr = reasonMsg_attachmentStr[:-1]
            reasonMsg.content = reasonMsg.content.replace('"','\"')
            reasonMsg.content = reasonMsg.content.replace("'","\'")
            reasonMsgFormatted = reasonMsg.content
            newlineIndexes = [pos for pos, char in enumerate(reasonMsgFormatted) if char == '\n']
            if newlineIndexes != []:
                count = 0
                for pos in newlineIndexes:
                    reasonMsgFormatted = list(reasonMsgFormatted)
                    reasonMsgFormatted.insert(pos+1+count, "> ")
                    count += 2
                    reasonMsgFormatted = ''.join(reasonMsgFormatted)

        embed = discord.Embed(description="**Is this strike appealable?**")
        embed.set_author(icon_url=staff.display_avatar, name=staff.display_name)
        embed.set_footer(text='RATA Administration - Times out in 1 minute')
        view = YesorNoView(ctx.author)
        appealMsg = await thread.send(embed=embed, view=view)
        await view.wait()
        appealable = False
        if view.value == None:
            await appealMsg.reply('Prompt timed out, thread will be deleted in 30 seconds.')
            await beginMsg.edit(content='<:no:614538096704487425> **Prompt timed out**')
            await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(staff.display_name)))))+"'s strike")
            await asyncio.sleep(30)
            return await thread.delete()
        elif view.value == True:
            appealable = True

        #-----------------------------------------------------------------
        cursor = await self.client.db.execute(f"SELECT reason FROM strikes WHERE staff_id = {staff.id} AND dept = '{dept}'")
        data = await cursor.fetchall()
        await cursor.close()
        #-----------------------------------------------------------------

        strikenum = str(len(data) + 1)
        if direc in ctx.author.roles:
            role = ", Director of RATA"
        elif ad in ctx.author.roles:
            role = ", Assistant Director of RATA"
        elif dogo in ctx.author.roles:
            role = ", Director of Group Operations"
        elif dom in ctx.author.roles:
            role = ", Director of Moderation"
        elif head_ins in ctx.author.roles:
            role = ", Head Instructor"
        elif lm in ctx.author.roles:
            role = ", Lead Moderator"
        else:
            role = ""
        
        if reasonMsg_attachmentStr == "":
            embed=discord.Embed(title="Strike Confirmation", description=f"You are about to strike **{staff.display_name}** for the **reason**: ```fix\n{reasonMsg.content}\n```\n"+f"This will be strike **`{strikenum}`** within the {dept.title()} department for the staff member.", color=discord.Color.orange())
        else:
            embed=discord.Embed(title="Strike Confirmation", description=f"You are about to strike **{staff.display_name}** for the **reason**: ```fix\n{reasonMsg.content}\n```"+f"{reasonMsg_attachmentStr}"+f"\n\nThis will be strike **`{strikenum}`** within the {dept.title()} department for the staff member.", color=discord.Color.orange())
        embed.set_author(icon_url=staff.display_avatar, name=staff.display_name)
        embed.set_footer(text='RATA Administration - Times out in 1 minute')
        view = ConfirmationView(ctx.author)
        await appealMsg.delete()
        confirm_msg = await thread.send(embed=embed, view=view)
        await view.wait()
        if view.value == None:
            await confirm_msg.reply('Prompt timed out, thread will be deleted in 30 seconds.')
            await beginMsg.edit(content='<:no:614538096704487425> **Prompt timed out**')
            await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(staff.display_name)))))+"'s strike")
            await asyncio.sleep(30)
            return await thread.delete()
        elif view.value == False:
            await confirm_msg.reply('Prompt cancelled, thread will be deleted in 30 seconds.')
            await beginMsg.edit(content='<:no:614538096704487425> **Prompt timed out**')
            await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(staff.display_name)))))+"'s strike")
            await asyncio.sleep(30)
            return await thread.delete()
        else:
            strike_id = '%030x' % random.randrange(16**30)
            await confirm_msg.delete()
            embed_success=discord.Embed(title="Strike Successful", description=f"You have striked **{staff.display_name}** for the **reason**: ```fix\n{reasonMsg.content}\n```"+f"{reasonMsg_attachmentStr}", color=discord.Color.green())
            embed_success.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            embed_success.set_footer(text=f'RATA Administration - Thread deletes in 1 minute')

            embed_fail=discord.Embed(title="Strike Successfully logged (DM Failure)", description=f"You have striked **{staff.display_name}** for the **reason**: ```fix\n{reasonMsg.content}\n```"+f"{reasonMsg_attachmentStr}"+"\nHowever, the staff member was not made aware of the strike due to a DM error.", color=0xeb6b34)
            embed_fail.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            embed_fail.set_footer(text=f'RATA Administration - Thread deletes in 1 minute')


            embed_dm=discord.Embed(title="You have been striked by the RATA Administration", color=0xeb6b34)
            embed_dm.add_field(name="Strike Department",value="> "+dept.title(),inline=False)
            embed_dm.add_field(name="Strike Number",value=f"> **`{strikenum}`**",inline=False)
            embed_dm.add_field(name="Strike Issuer",value=f"> **{ctx.author.display_name}**{role}",inline=False)
            embed_dm.add_field(name="Strike Date",value=f"> <t:{round(time.time())}:F>",inline=False)
            embed_dm.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")

            if appealable:
                embed_dm.add_field(name="Strike Reason",value=f"> {reasonMsgFormatted}"+f"{reasonMsg_attachmentStr}\n\nYou may appeal this strike after one month by visiting the [strike appeal form](https://forms.gle/GKLgZLbJPZjkVd7x7).",inline=False)
            else:
                embed_dm.add_field(name="Strike Reason",value=f"> {reasonMsgFormatted}"+f"{reasonMsg_attachmentStr}\n\n**`[NOT APPEALABLE]`**",inline=False)
            embed_dm.set_footer(text=f'Staff ID: {staff.id} - RATA Administration')

            embed_send = discord.Embed(color=0xeb6b34)
            embed_send.set_author(name=f"{staff.display_name} ({staff.id}) has recieved a strike.", icon_url=staff.avatar)
            embed_send.add_field(name="Strike Department",value="> "+dept.title(),inline=False)
            embed_send.add_field(name="Strike Number",value=f"> **`{strikenum}`**",inline=False)
            embed_send.add_field(name="Strike Issuer",value=f"> **{ctx.author.display_name}**{role}",inline=False)
            embed_send.add_field(name="Strike Date",value=f"> <t:{round(time.time())}:F>",inline=False)
            embed_send.add_field(name="Strike Reason",value=f"> {reasonMsgFormatted}"+f"{reasonMsg_attachmentStr}",inline=False)
            embed_send.set_thumbnail(url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
            embed_send.set_footer(text=f'Strike ID: {strike_id} | RATA Administration')
            try:
                await staff.send(embed=embed_dm)
            except:
                await thread.send(embed=embed_fail)
                await strikechannel.send(embed=embed_send)
            else:
                await thread.send(embed=embed_success)
                await strikechannel.send(embed=embed_send)
            await thread.edit(name="⛔"+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(staff.display_name)))))+"'s strike")
            #-------------------------------------------
            await self.client.db.execute(f'INSERT INTO strikes VALUES ("{strike_id}", {staff.id}, "{dept}", "{reasonMsg.content + reasonMsg_attachmentStr}", {round(time.time())}, {ctx.author.id})')
            await self.client.db.commit()
            #-------------------------------------------
            await asyncio.sleep(60)
            await thread.delete()
    
    @strike.error
    async def on_command_error(self,ctx, error):
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send("<a:RO_alert:773211228373647360> User was not found. Please ensure you are using either complete discord username (abc#1234) or their user ID.")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("<a:RO_alert:773211228373647360> Missing necessary argument.\n```\nr.strike @<user>\n```")


    @commands.command(name='strikes',aliases=['showstrikes'])
    @commands.has_role(Roles.staff)
    async def strikes(self,ctx,staff : discord.Member = None):
        selfCheck = False
        if staff == None:
            staff = ctx.author
            selfCheck = True
        else:
            HRcheck = False
            for role in ctx.author.roles:
                if role.id in [Roles.head_instructor, Roles.lead_moderator, Roles.board_of_directors, Roles.advisor, Roles.assistant_director, Roles.director]:
                    HRcheck = True
                    break
            if HRcheck == False:
                return await ctx.reply("<a:RO_alert:773211228373647360> You cannot check the strikes for another staff member other than yourself.")
        #-----------------------------------------------------------------
        cursor = await self.client.db.execute(f"SELECT strike_id, reason, time_of_issue, issuer_id FROM strikes WHERE staff_id = {staff.id} and dept = 'general'")
        general_data = await cursor.fetchall()
        cursor = await self.client.db.execute(f"SELECT strike_id, reason, time_of_issue, issuer_id FROM strikes WHERE staff_id = {staff.id} and dept = 'training'")
        training_data = await cursor.fetchall()
        cursor = await self.client.db.execute(f"SELECT strike_id, reason, time_of_issue, issuer_id FROM strikes WHERE staff_id = {staff.id} and dept = 'moderation'")
        moderation_data = await cursor.fetchall()
        await cursor.close()
        #-----------------------------------------------------------------
        if len(general_data+training_data+moderation_data) != 0:
            embedList = []
            if len(general_data) != 0:
                genEmbed = discord.Embed(title='General Department Strikes'+f' ({len(general_data)})', colour=discord.Color.blue())
                count = 1
                for strike in general_data:
                    strike = list(strike)
                    if str(strike[2]) == '0':
                        strike[2] = 'Not Available'
                        strike[3] = 'Not Available'
                        genEmbed.add_field(name=f"Strike {count} - ID {strike[0]}", value=f"> {strike[1]}"+f"\n*Issue date and issuer not available*", inline=False)
                    else:
                        newlineIndexes = [pos for pos, char in enumerate(strike[1]) if char == '\n']
                        if newlineIndexes != []:
                            count = 0
                            for pos in newlineIndexes:
                                strike[1] = list(strike[1])
                                strike[1].insert(pos+1+count, "> ")
                                count += 2
                                strike[1] = ''.join(strike[1])
                        genEmbed.add_field(name=f"Strike {count} - ID: {strike[0]}", value=f"> {strike[1]}"+f"\n*Issued by <@!{strike[3]}> on <t:{strike[2]}:D>*", inline=False)
                    count+=1
                embedList.append(genEmbed)
            if len(training_data) != 0:
                trainingEmbed = discord.Embed(title='Training Department Strikes'+f' ({len(training_data)})', colour=discord.Color.blue())
                count = 1
                for strike in training_data:
                    strike = list(strike)
                    if str(strike[2]) == '0':
                        strike[2] = 'Not Available'
                        strike[3] = 'Not Available'
                        trainingEmbed.add_field(name=f"Strike {count} - ID {strike[0]}", value=f"> {strike[1]}"+f"\n*Issue date and issuer not available*", inline=False)
                    else:
                        newlineIndexes = [pos for pos, char in enumerate(strike[1]) if char == '\n']
                        if newlineIndexes != []:
                            count = 0
                            for pos in newlineIndexes:
                                strike[1] = list(strike[1])
                                strike[1].insert(pos+1+count, "> ")
                                count += 2
                                strike[1] = ''.join(strike[1])
                        trainingEmbed.add_field(name=f"Strike {count} - ID: {strike[0]}", value=f"> {strike[1]}"+f"\n*Issued by <@!{strike[3]}> on <t:{strike[2]}:D>*", inline=False)
                    count+=1
                embedList.append(trainingEmbed)
            if len(moderation_data) != 0:
                modEmbed = discord.Embed(title='Moderation Department Strikes'+f' ({len(moderation_data)})', colour=discord.Color.blue())
                count = 1
                for strike in moderation_data:
                    strike = list(strike)
                    if str(strike[2]) == '0':
                        strike[2] = 'Not Available'
                        strike[3] = 'Not Available'
                        modEmbed.add_field(name=f"Strike {count} - ID {strike[0]}", value=f"> {strike[1]}"+f"\n*Issue date and issuer not available*", inline=False)
                    else:
                        newlineIndexes = [pos for pos, char in enumerate(strike[1]) if char == '\n']
                        if newlineIndexes != []:
                            count = 0
                            for pos in newlineIndexes:
                                strike[1] = list(strike[1])
                                strike[1].insert(pos+1+count, "> ")
                                count += 2
                                strike[1] = ''.join(strike[1])
                        modEmbed.add_field(name=f"Strike {count} - ID: {strike[0]}", value=f"> {strike[1]}"+f"\n*Issued by <@!{strike[3]}> on <t:{strike[2]}:D>*", inline=False)
                    count+=1
                embedList.append(modEmbed)
            if selfCheck == True:
                await ctx.author.send(content='You have the following strikes:',embeds=embedList)
                await ctx.reply("Please check your DMs for your strike list.")
            else:
                await ctx.send(content=f'**{staff.display_name}** has the following strikes:',embeds=embedList)
        else:
            if selfCheck == True:
                await ctx.author.send("You have no strikes. Keep it up!")
                await ctx.reply("Please check your DMs for your strike list.")
            else:
                await ctx.send(f"**{staff.display_name}** has no strikes in any of the departments.")

    @strikes.error
    async def on_command_error(self,ctx, error):
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send("<a:RO_alert:773211228373647360> User was not found. Please ensure you are using either complete discord username (abc#1234) or their user ID.")

    @commands.command(name='delstrike',aliases=['removestrike','deletestrike'])
    @commands.has_any_role(Roles.board_of_directors, Roles.advisor, Roles.assistant_director, Roles.director, Roles.head_instructor, Roles.lead_moderator)
    async def delstrike(self,ctx, strike_id : str):
        #-----------------------------------------------------------------
        cursor = await self.client.db.execute(f"SELECT staff_id, reason, dept FROM strikes WHERE strike_id = '{strike_id}'")
        data = await cursor.fetchone()
        await cursor.close()
        if len(data) == 0:
            return await ctx.send(f"<:RO_error:773206804758790184> Strike with the ID `{strike_id}` was not found.")
        #-----------------------------------------------------------------
        
        await ctx.send(f"<:RO_success:773206804850016276> {data[2].title()} department strike for <@!{data[0]}> with reason: ```fix\n{data[1]}\n```\n was __deleted__.")
        
        #-------------------------------------------
        await self.client.db.execute(f"DELETE FROM strikes WHERE strike_id = '{strike_id}'")
        await self.client.db.commit()
        #-------------------------------------------        

    @delstrike.error
    async def on_command_error(self,ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("<a:RO_alert:773211228373647360> Missing necessary argument.\n```\nr.delstrike <strike ID>\n```")

async def setup(client):
    await client.add_cog(ModerationCog(client))