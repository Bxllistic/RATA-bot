import discord
from discord.ext import commands
import gspread_asyncio
import pickle
import time
import asyncio
import string
import random
from bot_utils.roleId import Roles
from urllib.parse import quote

from google.oauth2.service_account import Credentials

fail_cooldown_list = []

def get_creds():
    creds = Credentials.from_service_account_file("/home/container/cogs/JSON credentials/credentials_nitro.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

class NitroExamCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > Nitro Exam cog healthy.")

    @commands.command(name="nitroExam")
    @commands.has_role(Roles.tier_4)
    @commands.cooldown(1,60,commands.BucketType.user)
    async def nitroExam(self,ctx):
        global fail_cooldown_list
        agc = await agcm.authorize()
        sheet = await agc.open_by_key("1DwDi-ouq8gUTVPJ2kcIWTJcAuAD_lKWlZmeTFdqubUE")  #open sheet
        worksheet = await sheet.worksheet("Data")
    
        Nsheet = await agc.open_by_key("1Dd9ZKtfwBUiN1jSY-WfIlyAx2RMJmYJX-9lr8YPEQ6A")
        Nworksheet = await Nsheet.worksheet("Booster Exams")

        dono_access = False
        for role in ctx.author.roles:
            if role.id == Roles.donator:
                dono_access = True
        
        if ctx.author.premium_since == None or dono_access == False:
            return await ctx.reply(embed = discord.Embed(description="This command is only for Nitro Boosters and Donators of this server.",colour=0xFF0000))
        else:
            if ctx.author.id not in fail_cooldown_list:
                if (await worksheet.acell('B4')).value == "NO":
                    try:
                        user_id_cell = await Nworksheet.find(str(ctx.author.id))
                        return await ctx.author.send(embed=discord.Embed(description=":warning: You have already sent a booster exam. Use `r.checkScore` to check your score."))
                    except:
                        confirm_msg = await ctx.author.send(embed=discord.Embed(title="⚠️ Confirmation",description="For security reasons, you will be limited to 3 hours of time to complete the quiz. Don't worry however, the quiz should only take about 20-40 minutes.\n> *Only continue if you have enough time to give the exam.*",colour=0xeb6b34).set_footer(text="React accordingly"))
                        await confirm_msg.add_reaction("<:RO_success:773206804850016276>")
                        await confirm_msg.add_reaction("<:RO_error:773206804758790184>")

                        def check(reaction,user):
                            return user == ctx.author and str(reaction.emoji) in ["<:RO_success:773206804850016276>","<:RO_error:773206804758790184>"] 
                        try:
                            reaction, user = await self.client.wait_for('reaction_add', timeout=200.0, check=check)
                        except asyncio.TimeoutError:
                            await confirm_msg.edit(embed = discord.Embed(description="**Prompt timed out.**",color=0xFF0000).set_author(name=str(ctx.author), icon_url=ctx.author.avatar))
                            await confirm_msg.remove_reaction("<:RO_success:773206804850016276>",ctx.me)
                            await confirm_msg.remove_reaction("<:RO_error:773206804758790184>",ctx.me)
                        else:
                            if str(reaction.emoji) == "<:RO_success:773206804850016276>":
                                newCode = 'CGN-'+''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(10))
                                try:
                                    dname = ctx.author.display_name.split(" | ")[1]
                                except IndexError:
                                    dname = ctx.author.display_name
                                nuser = quote(ctx.author.name) + "%23" + ctx.author.discriminator
                                curCode = (await worksheet.acell('A4')).value
                                link = f"https://docs.google.com/forms/d/e/1FAIpQLSdN7KFwEsZNPNZ11A9ldmBZQm4gJ0ggOekr8ZgMWNszFbwkIg/viewform?usp=pp_url&entry.1555421643={curCode}&entry.435634905={dname}&entry.1117172933={nuser}&entry.1877223641={ctx.author.id}"
                                msg = await ctx.author.send(embed=discord.Embed(title = "Certification Examination Form",description = f"You will have 3 hours to complete the exam, the link to which is given below. Simply click the link to enter the examination.\n\n➤ Verification Code: **`{curCode}`**\n➤ Form Link: [Click Me!]({link})").set_footer(text="Use r.checkScore to check your final score after taking the exam.")) 
                                await worksheet.update_acell('B4', "YES")
                                await worksheet.update_acell('D4', f"{dname} | {str(ctx.author.id)}")
                                await worksheet.update_acell('A4', f'{newCode}')
                                await asyncio.sleep(10800)
                                if (await worksheet.acell('B4')).value == "YES" and (await worksheet.acell('D4')).value == dname:
                                    await worksheet.update_acell('C4',"YES")
                                    await msg.edit(embed = discord.Embed(description="⚠️**3 Hour timeout reached**\n\nThe verification code for the exam has now __updated__.",colour=0xFF0000))
                            elif str(reaction.emoji) == "<:RO_error:773206804758790184>":
                                await confirm_msg.delete()
                                embed_no=discord.Embed(title="Exam prompt cancelled.", colour=0xFF0000)
                                await user.send(embed=embed_no)
                else:
                    await ctx.author.send(embed = discord.Embed(title="Examination currently occupied",description="Unfortunately, another person is currently giving the exam. Two or more people cannot simultaneously give the exam.\n\nPlease wait for a while and try this command again (max wait times for each person : 3 hours)."))
            else:
                await ctx.author.send(embed = discord.Embed(title="⚠️ You are on cooldown",description="Please make sure you have waited the complete **24 hours** before requesting another attempt at the nitro booster exam.", colour=0xFF0000))

    @nitroExam.error
    async def nitroexam_error(self, ctx, error): 
        if isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.reply("<:RO_error:773206804758790184> You need to be at `Tier 4` to access this command.")

    @commands.command(name="checkScore")
    @commands.dm_only()
    @commands.cooldown(1,30,commands.BucketType.user)
    async def checkScore(self,ctx):
        global fail_cooldown_list
        msg = await ctx.send(embed=discord.Embed(description="> *Processing request, this may take some time...*"))
        agc = await agcm.authorize()
        Nsheet = await agc.open_by_key("1Dd9ZKtfwBUiN1jSY-WfIlyAx2RMJmYJX-9lr8YPEQ6A")
        Nworksheet = await Nsheet.worksheet("Booster Exams")

        guild = self.client.get_guild(427007974947553280)
        member = guild.get_member(ctx.author.id)
        cgrole = guild.get_role(Roles.rata_certified)
        
        check = False
        dono_access = False
        for role in member.roles:
            if role.id == Roles.tier_4:
                check = True
            elif role.id == Roles.donator:
                dono_access = True

        with open('/home/container/cogs/JSON credentials/scoreChecked.dat','rb') as file:
            try:
                checkedList = pickle.load(file)
            except EOFError:
                checkedList = []
        for ele in checkedList:
            if ele == ctx.author.id:
                return await msg.edit(content="",embed=discord.Embed(description=":warning: You have already viewed your score before. Contact the Director of Group Operations in case you require assistance regarding your result.",colour=0xFF0000)) 
        
        if check == True and (member.premium_since != None or dono_access != False):
            try:
                user_id_cell = await Nworksheet.find(str(ctx.author.id))
            except:
                return await msg.edit(content="",embed=discord.Embed(title="Exam record was not found",description="Your name was not in our `Server Booster` exam records.\n\nIf you think this was a mistake, kindly contact the current Director of Group Operations.",colour = 0xFF0000))
            score = await Nworksheet.acell(f'C{str(user_id_cell.row)}')
            try:
                dname = member.display_name.split(" | ")[1]
            except IndexError:
                dname = member.display_name
            if int(score.value.split(' / ')[0]) >= 30:
                chnl = self.client.get_channel(836662029128957992)
                await ctx.invoke(self.client.get_command("cgresult"), member, int(score.value.split(' / ')[0]))
                await msg.edit(embed=discord.Embed(title="Thank you for supporting RATA!",description="You should be ranked in both, RA and RATA roblox groups. If you still aren't ranked, kindly contact the Director of Group Operations.",colour=discord.Colour.orange()))
                await chnl.send(f'r!setrank {dname} RATA Certified')
                await chnl.send(f'r!setrankRA {dname} Certified Guide')
                try:
                    t4role = guild.get_role(Roles.tier_4)
                    await member.add_roles(cgrole)
                    await member.remove_roles(t4role)
                    await member.edit(nick=f"CG | {dname}")
                except:
                    pass
                with open('/home/container/cogs/JSON credentials/scoreChecked.dat','wb') as file:
                    checkedList.append(ctx.author.id)
                    pickle.dump(checkedList,file)
            else:
                time_u=time.strftime("%a, %d %b | %H:%M:%S GMT", time.gmtime())
                await msg.edit(embed=discord.Embed(title="RATA Certification Exam Results", description=f"Unfortunately **{dname}**, you have failed the exam and have acquired **{int(score.value.split(' / ')[0])}** marks out of 40. However, don't be discouraged. You can attempt the quiz again after 24 hours using the same command, `r.nitroExam`." , colour=0xff0f0f).set_footer(text=f"sponsored by RATA.botservices ● {time_u}"))
                await Nworksheet.update_acell(f'F{user_id_cell.row}', f'{user_id_cell.value} !-! PREV ATTEMPT')
                fail_cooldown_list.append(ctx.author.id)
                await asyncio.sleep(86400)
                fail_cooldown_list.remove(ctx.author.id)
        else:
            return await msg.edit(content="",embed=discord.Embed(description="<:RO_error:773206804758790184> You need the Nitro Booster / Donator role to run this command.",colour=0xFF0000)) 

async def setup(client):
    await client.add_cog(NitroExamCog(client)) 