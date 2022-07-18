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

rankDescriptions = {
    'RA Executive Management': 'These individuals act as management over all RA sub-departments. They assist the Chairman with admin issues, and will also make decisions for the wider RA community. Unless you have a problem with the Department Overseer, they should not be contacted with issues related to RATA.',
    'Department Overseer': 'Overseer of RATA and SnR. They will supervise the HR team, and make executive decisions in relation to any changes within RATA. They should not be contacted unless you have a problem with the Director, or Assistant Director.',
    'Director': 'The individual assigned to direct RATA. This individual is in charge of all RATA departments and makes sure each department within RATA is being run correctly. They will also discuss issues with the RA overseers and get their opinions. You may contact this person if your reason does not apply to any of the ranks below. The rank is assigned to an individual chosen by RA management.',
    'Assistant Director': 'The assistant to the Director of RATA. This individual will help with admin, and ensure all RATA departments are run properly. They will also give advice and suggestions on potential changes to RATA. This individual should be contacted if you have concerns or suggestions about RATA, and to report issues with the HR team. You should also choose to DM them before going to the Director.',
    'Advisor': 'This role is given to retired HRs who have been helpful and dedicated to RATA. They will advise the current Director on issues, and give suggestions for future ideas. While this role does not have any specific responsibilities, some Advisors will also run small sections of RATA, such as managing Adverts. These individuals should be contacted if you have a question about their section. They should not be contacted if you have a complaint about a staff member.',
    'Board of Directors': 'This rank consists of 2 members: The Director of Group Operations & The Director of Moderation. They each run a department within RATA. You may contact them if you have questions, concerns, or suggestions about their respective department. They should also be contacted if you need a rank restored in RATA. These individuals should be your source to go if needed assistance about anything that no lower ranks can resolve.',
    'Head Instructor': 'The assistant of the Director of Group Operations. They are given tasks and are responsible for important subjects such as keeping track of the weekly activity of instructors and ensuring cooperation within their department. If you have questions or concerns with the Training Department, you may bring them up with them. You may also ask the Head Instructor to restore ranks.',
    'Lead Moderator': 'The assistant of the Director of Moderation. They are given tasks and are responsible for important subjects such as keeping track of the weekly activity of moderators and ensuring cooperation within their department. If you have questions or concerns with the Moderation Department, you may bring them up with them.',
    'Junior Instructor Trainer': 'Responsible for junior instructors, and also helping out the Head Instructor when necessary. Although, this position mainly hosts and supervises the junior instructors. Supervisors who have shown proficiency and dedication will be promoted to this rank. These individuals should be contacted with questions about the RATA training program, as well as any concerns about Junior Instructors.',
    'Supervisor': 'Supervisors are the next rank up from Instructor. This role is only awarded to those who show their determination for the job. Their main responsibility is to supervise Junior Instructors, and host trainings. If you have a question about the Training Department, you may contact these individuals, however concerns about Junior Instructors should be directed to Junior Instructor Trainers.',
    'Instructor': 'Instructors are responsible for hosting trainings and helping the students reach their goals of becoming a Certified Guide. This role can be achieved by passing a trial phase as a Junior Instructor. You should contact these individuals with queries regarding the Instruction department',
    'Junior Instructor': 'Newly recruited staff members. They will be going through their trial phase if they have this role. It is recommended to contact a more experienced staff member if you have any questions or concerns, unless they are related to the specific individual. You can achieve this role through Junior Instructor Applications.',
    'Senior Moderator': 'Senior individuals within the moderation department. These individuals assist the probationary moderators during their introductory phase. They will also assist the Lead Moderator with any issues. They should be contacted with questions about the Moderation Department, however, they should not be contacted to complain about actions taken against you.',
    'Moderator': 'They moderate the chats and answer any questions that are asked. This role can be achieved by passing the Moderation Training Program. They can be contacted with questions about RATAs discord, as well as questions about moderation actions. You can also contact them if you have any questions about warnings or previous moderation actions.',
    'Probationary Moderator': 'Newly recruited staff members. They will be going through their training phase if they have this role. It is recommended to contact a more experienced staff member if you have any questions or concerns, unless they are related to the specific individual. You can achieve this role through Moderator Applications.',
}

class StaffListCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.staffupdateloop.start()
   
    @tasks.loop(hours=24)
    async def staffupdateloop(self):
        server = self.client.get_guild(427007974947553280)
        channel = server.get_channel(814467021705838592)
        msg = await channel.fetch_message(814467097073156108)
        staff = {"RA Executive Management":None,"Department Overseer":None,"Director":None,"Assistant Director":None,"Advisor":None,"Board of Directors":None,"Head Instructor":None,"Lead Moderator":None,"Junior Instructor Trainer":None,"Supervisor":None,"Instructor":None,"Junior Instructor":None,"Senior Moderator":None,"Moderator":None,"Probationary Moderator":None}
        staff["RA Executive Management"] = server.get_role(Roles.ra_executive_management).members
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
            for user in staff["RA Executive Management"]:
                for extrarole in ["Probationary Moderator","Moderator","Senior Moderator","Junior Instructor","Instructor","Supervisor","Junior Instructor Trainer","Lead Moderator","Head Instructor","Board of Directors","Assistant Director","Advisor","Director","Department Overseer"]:
                    try:
                        if user in staff[extrarole]:
                            staff[extrarole].remove(user)
                    except:
                        pass
        except:
            pass

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
        
        hr_str = ''
        ins_str = ''
        mod_str = ''
        for key,val in staff.items():
            if key == 'RA Executive Management':
                hr_str += f"\n\n<@&{Roles.ra_executive_management}>\n{rankDescriptions['RA Executive Management']}"
                if val == []:
                    hr_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        hr_str += f"\n> {member.mention}"
            elif key == 'Department Overseer':
                hr_str += f"\n\n<@&{Roles.department_overseer}>\n{rankDescriptions['Department Overseer']}"
                if val == []:
                    hr_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        hr_str += f"\n> {member.mention}"
            elif key == 'Director':
                hr_str += f"\n\n<@&{Roles.director}>\n{rankDescriptions['Director']}"
                if val == []:
                    hr_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        hr_str += f"\n> {member.mention}"
            elif key == 'Assistant Director':
                hr_str += f"\n\n<@&{Roles.assistant_director}>\n{rankDescriptions['Assistant Director']}"
                if val == []:
                    hr_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        hr_str += f"\n> {member.mention}"
            elif key == 'Advisor':
                hr_str += f"\n\n<@&{Roles.advisor}>\n{rankDescriptions['Advisor']}"
                if val == []:
                    hr_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        hr_str += f"\n> {member.mention}"
            elif key == 'Board of Directors':
                hr_str += f"\n\n<@&{Roles.board_of_directors}>\n{rankDescriptions['Board of Directors']}"
                if val == []:
                    hr_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        hr_str += f"\n> {member.mention}"
            elif key == 'Head Instructor':
                hr_str += f"\n\n<@&{Roles.head_instructor}>\n{rankDescriptions['Head Instructor']}"
                if val == []:
                    hr_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        hr_str += f"\n> {member.mention}"
            elif key == 'Lead Moderator':
                hr_str += f"\n\n<@&{Roles.lead_moderator}>\n{rankDescriptions['Lead Moderator']}"
                if val == []:
                    hr_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        hr_str += f"\n> {member.mention}"
            elif key == 'Junior Instructor Trainer':
                ins_str += f"\n\n<@&{Roles.junior_instructor_trainer}>\n{rankDescriptions['Junior Instructor Trainer']}"
                if val == []:
                    ins_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        ins_str += f"\n> {member.mention}"
            elif key == 'Supervisor':
                ins_str += f"\n\n<@&{Roles.supervisor}>\n{rankDescriptions['Supervisor']}"
                if val == []:
                    ins_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        ins_str += f"\n> {member.mention}"
            elif key == 'Instructor':
                ins_str += f"\n\n<@&{Roles.instructor}>\n{rankDescriptions['Instructor']}"
                if val == []:
                    ins_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        ins_str += f"\n> {member.mention}"
            elif key == 'Junior Instructor':
                ins_str += f"\n\n<@&{Roles.junior_instructor}>\n{rankDescriptions['Junior Instructor']}"
                if val == []:
                    ins_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        ins_str += f"\n> {member.mention}"
            elif key == 'Senior Moderator':
                mod_str += f"\n\n<@&{Roles.senior_moderator}>\n{rankDescriptions['Senior Moderator']}"
                if val == []:
                    mod_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        mod_str += f"\n> {member.mention}"
            elif key == 'Moderator':
                mod_str += f"\n\n<@&{Roles.moderator}>\n{rankDescriptions['Moderator']}"
                if val == []:
                    mod_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        mod_str += f"\n> {member.mention}"
            elif key == 'Probationary Moderator':
                mod_str += f"\n\n<@&{Roles.probationary_moderator}>\n{rankDescriptions['Probationary Moderator']}"
                if val == []:
                    mod_str += '\n> *No members belong to this rank as of latest refresh*'
                else:
                    for member in val:
                        mod_str += f"\n> {member.mention}"
        
        img_emb = discord.Embed(colour=0xFFFFFF).set_image(url='https://media.discordapp.net/attachments/678298437854298122/998218167568584824/imag122e.png')
        hr_emb = discord.Embed(title='High Ranks', description=hr_str, color=discord.Color.blue())
        ins_emb = discord.Embed(title='Training Staff', description=ins_str, color=discord.Color.blue())
        mod_emb = discord.Embed(title='Moderation Staff', description=mod_str, color=discord.Color.blue())
        closing_emb = discord.Embed(description='Welcome to <:RATAcleanlogo:739164550862995502> **RATA**! Above is a list of ranks that you\'ll find within RATA, their purpose/duties, along with the members who hold that rank. If you have any questions we highly recommend going to one of the ranks under "Staff" before reaching out to a higher rank. All HR ranks are assigned by Management.', color=0xFFFFFF).set_footer(text='RATA Administration | List auto-updates every 24 hours')
        
        await msg.edit(content=None,embeds=[img_emb,hr_emb,ins_emb,mod_emb,closing_emb])
	
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