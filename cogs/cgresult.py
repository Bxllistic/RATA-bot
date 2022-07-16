import discord
import time, random, os
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from bot_utils.roleId import Roles

def sync_createCertificate(name_text, name_text3,marks):
    embed = discord.Embed(title="RATA Certification Exam Results", description=f"Greetings from the RATA Examination Team,\nWe are delighted to congratulate you, **{name_text}**, on passing the Certification Exam with **{marks}** out of 40! Thank you for attempting the exam, and good luck with your future expeditions and squad collaborations.\n\nAs a token of appreciation, we are providing you with a unique certificate attached below." , colour=0x2fee92)
    time123=time.strftime("%a, %d %b ● %H:%M:%S GMT", time.gmtime())
    embed.set_footer(text=f"sponsored by RATA.botservices | {time123}")
    raw_cert = Image.open("RAWCertificate.png")
    name_font = ImageFont.truetype('FrankRuhlLibre-Bold.ttf', 110)
    name_font1 = ImageFont.truetype('FrankRuhlLibre-Bold.ttf', 60)
    name_font2 = ImageFont.truetype('Passport Regular.ttf', 40)
    name_text2 = str(time.strftime("%d/%m/%Y", time.gmtime()))
    cert_editable = ImageDraw.Draw(raw_cert)
    cert_editable.text((960,685), name_text, (52, 52, 52), font=name_font, anchor="ms")
    cert_editable.text((443,1137), name_text2, (52, 52, 52), font=name_font1, anchor="ms")
    cert_editable.text((960,1335), name_text3, (180, 180, 180), font=name_font2, anchor="ms")
    raw_cert.save(f"MyCertificate-{name_text3}.png")
    BASE_DIR = str(os.path.dirname(os.path.abspath("main.py")))
    file = discord.File(f"{BASE_DIR}/MyCertificate-{name_text3}.png", filename=f"MyCertificate-{name_text3}.png")
    embed.set_image(url=f"attachment://MyCertificate-{name_text3}.png")
    return embed,file

def sync_deleteFile(name_text3):
    BASE_DIR = str(os.path.dirname(os.path.abspath("main.py")))
    os.remove(f"{BASE_DIR}/MyCertificate-{name_text3}.png")

class CGResultCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        from bot_utils.utilFunctions import currentTimeDXB
        print(f"{currentTimeDXB()} > CG Certificate cog healthy.")

    @commands.command()
    @commands.has_any_role(Roles.head_instructor, Roles.board_of_directors, Roles.advisor, Roles.assistant_director, Roles.director)
    async def cgresult(self, ctx, member : discord.Member, marks : int):
        guild=self.client.get_guild(427007974947553280)
        if 40>=marks>=30:
            try:
                name_text = member.display_name.split(" | ")[1]
            except IndexError:
                name_text = member.display_name
            name_text3 = "CGC-"+"".join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(7))
            returned_embed, returned_file = await self.client.loop.run_in_executor(None, sync_createCertificate, name_text, name_text3,marks)
            
            try:
                await member.send(file=returned_file, embed=returned_embed)
                await ctx.message.add_reaction('<:RO_success:773206804850016276>')
            except:
                await ctx.reply("<a:RO_alert:773211228373647360> DM Failure - Could not DM user, user possibly has DMs blocked.")
            await self.client.loop.run_in_executor(None, sync_deleteFile, name_text3)

        elif marks<30:
            try:
                name_text = member.display_name.split(" | ")[1]
            except IndexError:
                name_text = member.display_name
            time123=time.strftime("%a, %d %b | %H:%M:%S GMT", time.gmtime())
            embed = discord.Embed(title="RATA Certification Exam Results", description=f"Unfortunately **{name_text}**, you have failed the exam and have acquired **{marks}** marks out of 40. However, don't be discouraged. You still have infinite number of tries left.\n\nExams will reopen on the 1st of the next month." , colour=0xff0f0f)
            embed.set_footer(text=f"sponsored by RATA.botservices ● {time123}")
            try:
                await member.send(embed=embed)
                await ctx.message.add_reaction('<:RO_success:773206804850016276>')
            except:
                await ctx.reply("<a:RO_alert:773211228373647360> DM Failure - Could not DM user, user possibly has DMs blocked.")
        else:
            await ctx.reply("[Error 102] - Something went wrong - are you sure the marks you entered are correct?")

    @cgresult.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.reply("<a:RO_alert:773211228373647360> User was not found. Please ensure you are using either complete discord username (abc#1234) or their user ID.")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.reply("<a:RO_alert:773211228373647360> Missing necessary argument.\n```r.cgresult [member ID/username] [marks]```")


async def setup(client):
    await client.add_cog(CGResultCog(client)) 