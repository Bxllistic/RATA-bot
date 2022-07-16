import discord
from discord.ext import commands, tasks
import re
import datetime
from dateutil import tz
from bot_utils.utilFunctions import currentTimeDXB
from bot_utils.roleId import Roles

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

class StaffListCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.staffupdateloop.start()
   
    @tasks.loop(hours=24)
    async def staffupdateloop(self):
        server = self.client.get_guild(427007974947553280)
        channel = server.get_channel(814467021705838592)
        msg = await channel.fetch_message(814467097073156108)
        staff = {"Department Overseer":None,"Director":None,"Assistant Director":None,"Advisor":None,"Board of Directors":None,"Head Instructor":None,"Lead Moderator":None,"Junior Instructor Trainer":None,"Supervisor":None,"Instructor":None,"Junior Instructor":None,"Senior Moderator":None,"Moderator":None,"Probationary Moderator":None}
        staff["Department Overseer"] = server.get_role(Roles.department_overseer).members
        staff["Director"] = server.get_role(Roles.director).members
        staff["Assistant Director"] = server.get_role(Roles.assistant_director).members
        staff["Advisor"] = server.get_role(Roles.advisor).members
        staff["Board of Directors"] = server.get_role(Roles.board_of_directors).members
        staff["Head Instructor"] = server.get_role(Roles.head_instructor).members
        staff["Lead Moderator"] = server.get_role(Roles.lead_moderator).members
        staff["Junior Instructor Trainer"] = server.get_role(Roles.junior_instructor_trainer).members
        staff["Supervisor"] = server.get_role(Roles.supervisor).members
        staff["Instructor"] = server.get_role(Roles.instructor).members
        staff["Junior Instructor"] = server.get_role(Roles.junior_instructor).members
        staff["Senior Moderator"] = server.get_role(Roles.senior_moderator).members
        staff["Moderator"] = server.get_role(Roles.moderator).members
        staff["Probationary Moderator"] = server.get_role(Roles.probationary_moderator).members
        # Role Member Assignment
        
        try:
            for user in staff["Department Overseer"]:
                for extrarole in ["Probationary Moderator","Moderator","Senior Moderator","Junior Instructor","Instructor","Supervisor","Junior Instructor Trainer","Lead Moderator","Head Instructor","Board of Directors","Assistant Director","Advisor","Director"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass
        except:
            pass
        try:
            for user in staff["Director"]:
                for extrarole in ["Probationary Moderator","Moderator","Senior Moderator","Junior Instructor","Instructor","Supervisor","Junior Instructor Trainer","Lead Moderator","Head Instructor","Board of Directors","Assistant Director","Advisor"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass
        except:
            pass
        try:
            for user in staff["Assistant Director"]:
                for extrarole in ["Probationary Moderator","Moderator","Senior Moderator","Junior Instructor","Instructor","Supervisor","Junior Instructor Trainer","Lead Moderator","Head Instructor","Board of Directors","Advisor"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass
        except:
            pass
        try:
            for user in staff["Advisor"]:
                for extrarole in ["Probationary Moderator","Moderator","Senior Moderator","Junior Instructor","Instructor","Supervisor","Junior Instructor Trainer","Lead Moderator","Head Instructor","Board of Directors"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass
        except:
            pass
        try:
            for user in staff["Board of Directors"]:
                for extrarole in ["Probationary Moderator","Moderator","Senior Moderator","Junior Instructor","Instructor","Supervisor","Junior Instructor Trainer","Lead Moderator","Head Instructor"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass
        except:
            pass
        try:                    
            for user in staff["Head Instructor"]:
                for extrarole in ["Junior Instructor","Instructor","Supervisor","Junior Instructor Trainer","Lead Moderator"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass  
        except:
            pass  
        try:                
            for user in staff["Junior Instructor Trainer"]:
                for extrarole in ["Junior Instructor","Instructor","Supervisor"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass
        except:
            pass
        try:                  
            for user in staff["Supervisor"]:
                for extrarole in ["Junior Instructor","Instructor"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass 
        except:
            pass      
        try:             
            for user in staff["Lead Moderator"]:
                for extrarole in ["Probationary Moderator","Moderator","Senior Moderator"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass
        except:
            pass
        try:
            for user in staff["Senior Moderator"]:
                for extrarole in ["Probationary Moderator","Moderator"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass
        except:
            pass
        try:
            for user in staff["Probationary Moderator"]:
                for extrarole in ["Moderator"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass  
        except:
            pass
        
        for i in list(staff):
            if staff[i]==[]:
                del staff[i]

        e = discord.Embed(title="RATA Staff List",colour=0x43BCE9)
        e.set_footer(text="RATA | List updates every 24 hours",icon_url="https://cdn.discordapp.com/attachments/450656229744967681/770326969505153064/image-min22.png")
        for key,val in staff.items():
            strng = ""
            for member in val:
                strng+="\n> "+re.sub("\{.*?}","",(re.sub("\[.*?\]", "", deEmojify(str(member.display_name)))))
            e.add_field(name=f"{key} [{len(val)}]",value=f"{strng}",inline=False)
        await msg.edit(content=None,embed=e)
	
    @staffupdateloop.before_loop
    async def wait_until_midnight(self):
        await self.client.wait_until_ready()
        
        now = datetime.datetime.now(tz.gettz('Etc/Greenwich'))
        next_run = now.replace(hour=0, minute=0, second=0)

        if next_run < now:
            next_run += datetime.timedelta(days=1)

        await discord.utils.sleep_until(next_run)  
  
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{currentTimeDXB()} > Stafflist cog healthy.")
        
  
async def setup(client):
    await client.add_cog(StaffListCog(client))