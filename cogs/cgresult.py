import discord
import time, random, os
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import re
from bot_utils.roleId import Roles
from io import BytesIO

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

def sync_changeSignature(atch_bytes, disp_name):
    # Open the existing image
    existing_image = Image.open("RAWCertificate_NoSign.png")
    user_image = Image.open(BytesIO(atch_bytes)).convert("RGBA")
    new_image = Image.new("RGBA", (existing_image.width, existing_image.height), (0, 0, 0, 0))

    # Composite the existing image and user-provided image
    new_image.paste(existing_image, (0, 0))
    new_image.paste(user_image, (1175, 950), mask=user_image)

    # Adding director label
    match = re.search(r"\[.*?\]\s*(.*)", disp_name)
    if match:
        astr = match.group(1) + ", Director of RATA"
    else:
        astr = disp_name + ", Director of RATA"
    draw = ImageDraw.Draw(new_image)
    font = ImageFont.truetype('georgia.ttf', 35)
    bbox = draw.textbbox((0, 0), astr, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    center_x = 1428 - text_width // 2
    center_y = 1175 - text_height // 2
    draw.text((center_x, center_y), astr, font=font, fill=(0, 0, 0))

    # Save the resulting image
    new_image.save("RAWCertificate.png")


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

    @commands.command(aliases=['change_signature'])
    @commands.has_role(Roles.director)
    @commands.cooldown(1,60,commands.BucketType.user)
    async def certificateSignatureChange(self, ctx):
        try:
            attachment = ctx.message.attachments[0]  # Assuming the file is attached to the command message
            if attachment.content_type != 'image/png':
                return await ctx.reply("<a:RO_alert:773211228373647360> Invalid **file type**. Please attach a file that follows the below requirements:\n```diff\n+ Must be a PNG file\n+ Must be 500x200 by dimensions (width x height)\n+ Must be a black signature on a transparent background\n```")

            if attachment.width != 500 or attachment.height != 200:
                return await ctx.reply("<a:RO_alert:773211228373647360> Invalid **dimensions**. Please attach a file that follows the below requirements:\n```diff\n+ Must be a PNG file\n+ Must be 500x200 by dimensions (width x height)\n+ Must be a black signature on a transparent background\n```")

            msg = await ctx.reply("Working on it...")

            p_attachBytes = await attachment.read()

            await self.client.loop.run_in_executor(None, sync_changeSignature, p_attachBytes, ctx.author.display_name)

            returned_embed, returned_file = await self.client.loop.run_in_executor(None, sync_createCertificate, "SAMPLE", "CGC-0000000",40)

            await msg.edit(content="Certificate signature and name modified successfully! Below is a sample:")
            await ctx.send(file=returned_file)

            await self.client.loop.run_in_executor(None, sync_deleteFile, "CGC-0000000")
        except IndexError:
            await ctx.reply("<a:RO_alert:773211228373647360> Please attach a PNG image that follows the below requirements:\n```diff\n+ Must be a PNG file\n+ Must be 500x200 by dimensions (width x height)\n+ Must be a black signature on a transparent background\n```")
        except Exception as e:
            await ctx.reply(f"error occurred: {str(e)}\nngl avia is defo not gonna fix this shi so u might wanna forget bout it or wait a couple months until i open this god forsaken app again")


async def setup(client):
    await client.add_cog(CGResultCog(client)) 
