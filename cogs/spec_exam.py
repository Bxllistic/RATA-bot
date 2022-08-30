import discord
import datetime 
from discord.ext import commands
from bot_utils.roleId import Roles


# ----------------------------------------
# Button Classes
class ON_SpecPingView(discord.ui.View):
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

class OFF_SpecPingView(discord.ui.View):
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

# ----------------------------------------
# Cog Begin

class SpecExam(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Spec Exam cog healthy.")

    @commands.command()
    @commands.has_any_role(Roles.head_instructor, Roles.head_instructor, Roles.board_of_directors, Roles.advisor, Roles.assistant_director, Roles.director, Roles.junior_instructor_trainer)
    @commands.cooldown(1,3.0)
    async def specpass(self, ctx, *, user: discord.Member = None):
        guild = self.client.get_guild(427007974947553280)
        specrole = guild.get_role(Roles.trainedspectator_ping)

        if ctx.message.reference != None:
            user = None
            try:
                webmsg = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            except discord.HTTPException:
                return await ctx.send("<:RO_error:773206804758790184> Could not fetch the message replied to.")
            fieldcheck = False
            try:
                for i in webmsg.embeds[0].fields:
                    if i.name == "⬜ Enter your Discord username + discriminator":
                        fieldcheck = True
                        user = guild.get_member_named(i.value)
                        if not isinstance(user,discord.Member):
                            return await ctx.send(f"<:RO_error:773206804758790184> Could not find user named `{i.value}`")
                        break
                if fieldcheck == False:
                    return await ctx.send("<:RO_error:773206804758790184> The message you replied to was not a valid spectator submission embed.")
            except (IndexError, AttributeError):
                return await ctx.send("<:RO_error:773206804758790184> The message you replied to was not a valid spectator submission embed.")
            roles = user.roles
            check = False
            for role in roles:
                if role.id == Roles.tier_4:
                    check = True
                elif role.id == Roles.rata_certified:
                    check = True
            if check == True:
                await user.add_roles(specrole)
                today = datetime.date.today()
                d1=today.strftime("%B %d, %Y")
                d2=today.strftime("%Y")
                embed=discord.Embed(title="Spectator Request Form Results", description=f"We're glad to let you know that you've passed your Spectator Training! You are now allowed to specatate trainings hosted at RATA. Make sure you follow the guidelines we went over in the briefing form. For any further enquiries, contact any management member from the RATA staff team.\n\nIf you no longer want to get pinged for trainings but still want to remain as a Trained Spectator, use the command `r.specswitch` in any RATA channel.\nAlso make sure to check our dress code: [Click Me!](https://docs.google.com/document/d/1quMxc67VQd-OmZKtW4upja3UR04DUSqTmrLPsE3Nkog/edit?usp=sharing)\n\n> Examiner: {ctx.author.display_name}\n> Final Score: PASS\n> Date of Issue: {d1}",color=0x2fee92)
                embed.set_footer(text=f"RATA Administration - {d2}", icon_url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
                try:
                    await user.send(embed=embed)
                except Exception:
                    await ctx.send("<:RO_error:773206804758790184> Could not DM the user.")
                await ctx.message.add_reaction('<:RO_success:773206804850016276>')
                await webmsg.add_reaction('<:yes:614538082774941716>')
            else:
                await ctx.send(f"<:RO_error:773206804758790184> **{user.display_name}** is not a Tier 4 / Certified Guide. Disregard the submission.")
        
        else:
            if not isinstance(user, discord.Member):
                return await ctx.send("<:RO_error:773206804758790184> User parameter is missing.")
            else:              
                roles = user.roles
                check = False
                for role in roles:
                    if role.id == Roles.tier_4:
                        check = True
                    elif role.id == Roles.rata_certified:
                        check = True
                if check == True:
                    await user.add_roles(specrole)
                    today = datetime.date.today()
                    d1=today.strftime("%B %d, %Y")
                    d2=today.strftime("%Y")
                    embed=discord.Embed(title="Spectator Request Form Results", description=f"We're glad to let you know that you've passed your Spectator Training! You are now allowed to specatate trainings hosted at RATA. Make sure you follow the guidelines we went over in the briefing form. For any further enquiries, contact any management member from the RATA staff team.\n\nIf you no longer want to get pinged for trainings but still want to remain as a Trained Spectator, use the command `r.specswitch` in any RATA channel.\nAlso make sure to check our dress code: [Click Me!](https://docs.google.com/document/d/1quMxc67VQd-OmZKtW4upja3UR04DUSqTmrLPsE3Nkog/edit?usp=sharing)\n\n> Examiner: {ctx.author.display_name}\n> Final Score: PASS\n> Date of Issue: {d1}",color=0x2fee92)
                    embed.set_footer(text=f"RATA Administration - {d2}", icon_url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
                    try:
                        await user.send(embed=embed)
                    except Exception:
                        await ctx.send("<:RO_error:773206804758790184> Could not DM the user.")
                    await ctx.message.add_reaction('<:RO_success:773206804850016276>')
                else:
                    await ctx.send(f"<:RO_error:773206804758790184> **{user.display_name}** is not a Tier 4 / Certified Guide. Disregard the submission.")

    @specpass.error
    async def specpass_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send("<a:RO_alert:773211228373647360> User was not found. Please ensure you are using either complete discord username (abc#1234) or their user ID.")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("<a:RO_alert:773211228373647360> Missing necessary argument.\n```\nr.specpass <user_name>\n```")

    @commands.command()
    @commands.has_any_role(Roles.head_instructor, Roles.head_instructor, Roles.board_of_directors, Roles.advisor, Roles.assistant_director, Roles.director, Roles.junior_instructor_trainer)
    @commands.cooldown(1,3.0)
    async def specfail(self, ctx, *, user: discord.Member = None):
        guild=self.client.get_guild(427007974947553280)
        if ctx.message.reference != None:
            user = None
            try:
                webmsg = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            except discord.HTTPException:
                return await ctx.send("<:RO_error:773206804758790184> Could not fetch the message replied to.")
            try:
                for i in webmsg.embeds[0].fields:
                    if i.name == "⬜ Enter your Discord username + discriminator":
                        user = guild.get_member_named(i.value)
                        if not isinstance(user,discord.Member):
                            return await ctx.send(f"<:RO_error:773206804758790184> Could not find user named `{i.value}`")
                        break
            except (IndexError, AttributeError):
                return await ctx.send("<:RO_error:773206804758790184> The message you replied to was not a valid spectator submission embed.")
            roles = user.roles
            check = False
            for role in roles:
                if role.id == Roles.tier_4:
                    check = True
                elif role.id == Roles.rata_certified:
                    check = True
            if check == True:
                today = datetime.date.today()
                d1=today.strftime("%B %d, %Y")
                d2=today.strftime("%Y")
                embed=discord.Embed(title="Spectator Request Form Results", description=f"Unfortunately, you have failed the Spectator Training form. Don't worry, you can apply again after the coming Monday [here]()as we reset all applications every week. Make sure to read through the briefing before attempting the quiz next time.\n\n> Examiner: {ctx.author.display_name}\n> Final Score: FAIL\n> Date of Issue: {d1}",color=0xff0f0f)
                embed.set_footer(text=f"RATA Administration - {d2}", icon_url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
                try:
                    await user.send(embed=embed)
                except Exception:
                    await ctx.send("<:RO_error:773206804758790184> Could not DM the user.")
                await ctx.message.add_reaction('<:RO_success:773206804850016276>')
                await webmsg.add_reaction('<:no:614538096704487425>')
            else:
                await ctx.send(f"<:RO_error:773206804758790184> **{user.display_name}** is not a Tier 4 / Certified Guide. Disregard the submission.")

        else:
            if not isinstance(user, discord.Member):
                return await ctx.send("<:RO_error:773206804758790184> User parameter is missing.")
            else:
                roles = user.roles
                check = False
                for role in roles:
                    if role.id == Roles.tier_4:
                        check = True
                    elif role.id == Roles.rata_certified:
                        check = True
                if check == True:
                    today = datetime.date.today()
                    d1=today.strftime("%B %d, %Y")
                    d2=today.strftime("%Y")
                    embed=discord.Embed(title="Spectator Request Form Results", description=f"Unfortunately, you have failed the Spectator Training form. Don't worry, you can apply again after the coming Monday [here]()as we reset all applications every week. Make sure to read through the briefing before attempting the quiz next time.\n\n> Examiner: {ctx.author.display_name}\n> Final Score: FAIL\n> Date of Issue: {d1}",color=0xff0f0f)
                    embed.set_footer(text=f"RATA Administration - {d2}", icon_url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
                    try:
                        await user.send(embed=embed)
                    except Exception:
                        await ctx.send("<:RO_error:773206804758790184> Could not DM the user.")
                    await ctx.message.add_reaction('<:RO_success:773206804850016276>')
                else:
                    await ctx.send(f"<:RO_error:773206804758790184> **{user.display_name}** is not a Tier 4 / Certified Guide. Disregard the submission.")

    @specfail.error
    async def specfail_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send("<a:RO_alert:773211228373647360> User was not found. Please ensure you are using either complete discord username (abc#1234) or their user ID.")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("<a:RO_alert:773211228373647360> Missing necessary argument.\n```\nr.specfail <user_name>\n```")
   
    @commands.command()
    @commands.guild_only()
    async def specswitch(self, ctx):
        guild = self.client.get_guild(427007974947553280)
        ping_specrole = guild.get_role(Roles.trainedspectator_ping) 
        noping_specrole = guild.get_role(Roles.trainedspectator_noping) 
        emojifromserver = self.client.get_emoji(614538082774941716)

        if 751776350691655680 in [role.id for role in ctx.author.roles]:
            embed = discord.Embed(title=f'Spectator Role Switch', description='Currently, you have spectator shout pings **`enabled`**. Would you like to disable them?',colour=0xFFA500).set_footer(text="Prompt times out in 60 seconds.").set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar)
            view = OFF_SpecPingView(ctx.author)
            askingMsg = await ctx.reply(embed=embed,view=view)
            await view.wait()
            if view.value == True:
                await ctx.author.remove_roles(ping_specrole)
                await ctx.author.add_roles(noping_specrole)
                return await askingMsg.edit(embed=discord.Embed(title="Spectator shout pings are now **`disabled`**.", colour=0xFFA500).set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar), view=None)
            elif view.value == False:
                return await askingMsg.edit(embed=discord.Embed(title="Prompt cancelled", colour=0xFFA500).set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar), view=None)
            else:
                return await askingMsg.edit(embed=discord.Embed(title="Prompt timed out.", colour=0xFF0000).set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar), view=None)
            
        elif 916738999408795688 in [role.id for role in ctx.author.roles]:
            embed = discord.Embed(title=f'Spectator Role Switch', description='Currently, you have spectator shout pings **`disabled`**. Would you like to re-enable them?',colour=0xFFA500).set_footer(text="Prompt times out in 60 seconds.").set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar)
            view = ON_SpecPingView(ctx.author)
            askingMsg = await ctx.reply(embed=embed,view=view)
            await view.wait()
            if view.value == True:
                await ctx.author.remove_roles(noping_specrole)
                await ctx.author.add_roles(ping_specrole)
                return await askingMsg.edit(embed=discord.Embed(title="Spectator shout pings are now **`enabled`**.", colour=0xFFA500).set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar), view=None)
            elif view.value == False:
                return await askingMsg.edit(embed=discord.Embed(title="Prompt cancelled", colour=0xFFA500).set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar), view=None)
            else:
                return await askingMsg.edit(embed=discord.Embed(title="Prompt timed out.", colour=0xFF0000).set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar), view=None)
                
        else:
            return await ctx.reply(embed=discord.Embed(title='Insufficient Permissions', description='You need to be a `Trained Spectator` to use this command.', colour=0xFF0000).set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar))


async def setup(client):
    await client.add_cog(SpecExam(client)) 