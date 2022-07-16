import discord
from discord.ext import commands
import asyncio
from bot_utils.roleId import Roles

class FeedbackConfirmationView(discord.ui.View):
    def __init__(self, author : discord.Member, *, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None
    
    @discord.ui.button(label = 'Confirm', style=discord.ButtonStyle.green, emoji='<:yes:614538082774941716>')
    async def announce(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(label = 'Cancel Prompt',style=discord.ButtonStyle.red, emoji='<:no:614538096704487425>')
    async def abort(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

class FeedbackCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Feedback cog healthy.")

    @commands.command(name="feedback")
    @commands.cooldown(1,500,commands.BucketType.user)
    @commands.has_role(Roles.verified)
    @commands.guild_only()
    async def feedback(self,ctx):
        user = ctx.author
        embed = discord.Embed(title="RATA Instructor Feedback Form",description="This form's sole purpose is to obtain feedback regarding the instructors at RATA from the public in order to improve RATA's training department. If you have concerns, comments, or any other kind of feedback for any Instructor; then you can fill this form out. Please make sure you have valid reasoning and detailed answers. Being disrespectful to the Instructor will only cause consequences for yourself.\n\nEach question prompt times out in 5 minutes.\nCancel at any timing by entering `cancel`.\n\n> :warning: *Privacy Warning*\n> All messages after this point will be logged within the bot as soon as they are sent. Please avoid entering any personal / sensitive content within any of the answers.", colour=0xfc9003)
        embed.set_footer(text=f"Requested by {user}",icon_url=f"{user.avatar}")
        try:
            firstDM = await user.send(embed=embed)
        except:
            return await ctx.reply('<:RO_error:773206804758790184> I can\'t DM you! Please keep your DMs open to everyone to allow me to continue with the feedback questions.')
        await ctx.reply(embed=discord.Embed(description=f"**I've [DM'd]({firstDM.jump_url}) you!**"))
        #------------------------------------------------------------------------------------------
        embed1 = discord.Embed(description="Enter the roblox username of the instructor: ",colour=0xffdd00)
        embed1.set_footer(text="Question 1/4")
        await user.send(embed=embed1)
        def check(message):
            return message.author == user and message.guild == None
        try:
            message1 = await self.client.wait_for('message', timeout=300.0, check=check)
        except asyncio.TimeoutError:
            return await user.send(embed=discord.Embed(title="Prompt timed out.",description="You have exceeded our 5 minute time out. Please try the command again."))
        else:
            if message1.content == 'cancel':
                return await user.send(embed=discord.Embed(title="Feedback cancelled.",description="You have cancelled the feedback. Feel free to try again."))
            await message1.add_reaction("<:yes:614538082774941716>")
        #------------------------------------------------------------------------------------------
        embed2 = discord.Embed(description="What tier did you attend?",colour=0xffdd00)
        embed2.set_footer(text="Question 2/4")
        tempmsg = await user.send(embed=embed2)
        for i in ["1️⃣","2️⃣","3️⃣","4️⃣"]:
            await tempmsg.add_reaction(i)

        def tiercheck(reaction,user1):
            return user1 == user and reaction.message.id == tempmsg.id and (str(reaction.emoji) == "1️⃣" or str(reaction.emoji) == "2️⃣" or str(reaction.emoji) == "3️⃣" or str(reaction.emoji) == "4️⃣")
        try:
            reaction,user1 = await self.client.wait_for('reaction_add', timeout=300.0, check=tiercheck)
        except asyncio.TimeoutError:
            return await user.send(embed=discord.Embed(title="Prompt timed out.",description="You have exceeded our 5 minute time out. Please try the command again."))
        else:
            if str(reaction.emoji) == "1️⃣":
                tier = "Tier 1"
            elif str(reaction.emoji) == "2️⃣":
                tier = "Tier 2"
            elif str(reaction.emoji) == "3️⃣":
                tier = "Tier 3"
            elif str(reaction.emoji) == "4️⃣":
                tier = "Tier 4"
        #------------------------------------------------------------------------------------------
        embed3 = discord.Embed(description="Do you think that the training was good? Briefly explain your opinion/concern.",colour=0xffdd00)
        embed3.set_footer(text="Question 3/4")
        await user.send(embed=embed3)
        try:
            message3 = await self.client.wait_for('message', timeout=300.0, check=check)
        except asyncio.TimeoutError:
            return await user.send(embed=discord.Embed(title="Prompt timed out.",description="You have exceeded our 5 minute time out. Please try the command again."))
        else:
            if message3.content == 'cancel':
                return await user.send(embed=discord.Embed(title="Feedback cancelled.",description="You have cancelled the feedback. Feel free to try again."))
            await message3.add_reaction("<:yes:614538082774941716>")
            msg3_attachmentStr = ""
            if len(message3.attachments) >= 1:
                for att in message3.attachments:
                    msg3_attachmentStr += f"> [Attachment]({att.url})\n"
        #------------------------------------------------------------------------------------------
        embed4 = discord.Embed(description="What could've been done to make it better? If this feedback is a report, can you provide any proof or supporting details to support your claim?\n\n*You may add attachments as proof if required.*",colour=0xffdd00)
        embed4.set_footer(text="Question 4/4")
        await user.send(embed=embed4)
        try:
            message4 = await self.client.wait_for('message', timeout=300.0, check=check)
        except asyncio.TimeoutError:
            return await user.send(embed=discord.Embed(title="Prompt timed out.",description="You have exceeded our 5 minute time out. Please try the command again."))
        else:
            if message4.content == 'cancel':
                return await user.send(embed=discord.Embed(title="Feedback cancelled.",description="You have cancelled the feedback. Feel free to try again."))
            await message4.add_reaction("<:yes:614538082774941716>")
            msg4_attachmentStr = ""
            if len(message4.attachments) >= 1:
                for att in message4.attachments:
                    msg4_attachmentStr += f"> [Attachment]({att.url})\n"
            #------------------------------------------------------------------------------------------
            finalembed = discord.Embed(title="Feedback Confirmation",description="Please confirm if the following details are correct before we send this feedback to higher authorities.\n\n\u2800", colour=0xfc9003)
            finalembed.add_field(name="Enter the roblox username of the instructor:",value=message1.content, inline=False)
            finalembed.add_field(name="What tier did you attend?",value=tier, inline=False)
            finalembed.add_field(name="Do you think that the training was good? Briefly explain your opinion/concern.",value=message3.content+f"\n{msg3_attachmentStr}", inline=False)
            finalembed.add_field(name="What could've been done to make it better? If this feedback is a report, can you provide any proof or supporting details to support your claim?",value=message4.content+f"\n{msg4_attachmentStr}", inline=False)
            finalembed.set_footer(text="React accordingly | Times out in 1 minute")
            confirmView = FeedbackConfirmationView(user)
            confirm_msg = await user.send(embed=finalembed, view=confirmView)
            await confirmView.wait()
            if confirmView.value == True:
                embed5 = discord.Embed(title="Thank you.", description="We sincerely appreciate you spending your time filling our feedback form. If your feedback was a complaint, we will take actions depending on the case. ", colour = 0x24f228)
                embed5.set_footer(text="RATA Department of Group Operations")
                await confirm_msg.edit(embed=embed5,view=None)

                guild = self.client.get_guild(427007974947553280)
                dogo_role = guild.get_role(Roles.director_of_group_operations)
                hi_role = guild.get_role(Roles.head_instructor)
                member = guild.get_member(user.id)

                sendembed = discord.Embed(title="A new training feedback has been sent!",description=f"> 👤 {user} | {member.top_role.name} [{user.id}]\n\n\u2800", colour = 0x24f228)
                sendembed.add_field(name="Enter the roblox username of the instructor:",value=message1.content, inline=False)
                sendembed.add_field(name="What tier did you attend?",value=tier, inline=False)
                sendembed.add_field(name="Do you think that the training was good? Briefly explain your opinion/concern.",value=message3.content+f"\n{msg3_attachmentStr}", inline=False)
                sendembed.add_field(name="What could've been done to make it better? If this feedback is a report, can you provide any proof or supporting details to support your claim?",value=message4.content+f"\n{msg4_attachmentStr}", inline=False)
                sendembed.set_footer(text="You have recieved this message because you have the DoGO / Head Ins role.")
                for person in dogo_role.members:
                    await person.send(embed=sendembed)
                for person in hi_role.members:
                    if person not in dogo_role.members:
                        await person.send(embed=sendembed)
            elif confirmView.value == False:
                embed_no=discord.Embed(title="Feedback prompt cancelled", description="If you would like to send a feedback again, simply do `r.feedback` in <#481485159632470016>.", color=0xeb6b34).set_author(name=str(ctx.author), icon_url=ctx.author.avatar)
                await confirm_msg.edit(embed=embed_no,view=None)
            else:
                await confirm_msg.edit(embed = discord.Embed(description="**Prompt timed out.**",color=0xFF0000).set_author(name=str(ctx.author), icon_url=ctx.author.avatar), view=None)
        

async def setup(client):
    await client.add_cog(FeedbackCog(client))