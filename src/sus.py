from disnake.ext import commands
from JsonHandler import jsontask
import disnake
import src.Codeforces.Commands
import src.Codeforces.Funcs

rankcolor = {
    "newbie": 0xCCCCCC,
    "pupil": 0x77FF77,
    "specialist": 0x77DDBB,
    "expert": 0xAAAAFF,
    "candidate master": 0xFF88FF,
    "master": 0xFFCC88,
    "international master": 0xFFBB55,
    "grandmaster": 0xFF7777,
    "international grandmaster": 0xFF3333,
    "legendary grandmaster": 0xAA0000
}
async def makeroles(guild):
    rolelist = {}
    for rank, color in rankcolor.items():
        role = await guild.create_role(name=rank, color=color, hoist = True)
        rolelist[rank] = role.id
    jsontask.add_roles(guild.id, rolelist)

class GeneralCommand(commands.Cog):
    "A cog for all of commands regarding general Discord stuff"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def sus(inter, *args):
        pass

    @sus.sub_command()
    async def ping(self, inter):
        '''/sus ping: Get the bot's latency'''
        await inter.response.send_message(f"Pong! ({inter.bot.latency * 1000:.0f}ms)")

    @sus.sub_command()
    async def updateme(self, inter, user: disnake.User):
        '''/sus updateme @<Discord>: Add someone to the handle update list'''
        jsontask.add_to_update(inter.guild.id, user.id)
        await inter.response.send_message(f"{user.mention} has been added to the update list")

    @sus.sub_command()
    async def refresh(self, inter):
        '''/sus refresh: Refresh all color-based roles'''
        await inter.response.defer()
        cfquery = {}
        guildid = str(inter.guild.id)
        tasklist = jsontask.get_update_list(guildid)
        rolelist = jsontask.get_roles(guildid)
        guild = self.bot.get_guild(int(guildid))

        if guild is None:
            print(f"{guildid} cannot be updated")
            return 
        if rolelist is None:
            print(f"No rolelist found in {guildid}")
            await makeroles(inter.guild)
            
        for userid in tasklist:
            user = guild.get_member(int(userid))
            if user is None:
                print(f"{userid} in {guildid} not found")
                continue
            for role in user.roles:
                if role.id in rolelist:
                    await user.remove_role(role)
            handle = src.Codeforces.Commands.jsontask.get_handle(userid)
            if handle is not None:
                cfquery[handle] = user
        
        ranks = await src.Codeforces.Funcs.getRoles([key for key in cfquery])
        for (handle, user), rankname in zip(cfquery.items(), ranks):
            rolefromrank = guild.get_role(rolelist[rankname])
            await user.add_roles(rolefromrank)
        await inter.edit_original_message(content = "All roles refreshed")

def setup(bot: commands.Bot):
    bot.add_cog(GeneralCommand(bot))