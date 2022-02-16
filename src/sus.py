from disnake.ext import commands
from src import jsontask
import disnake
import src.Codeforces.Commands
import src.Codeforces.Funcs

class GeneralCommand(commands.Cog):
    "A cog for all of commands regarding Codeforces"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command
    def sus(inter, *args):
        pass

    @sus.sub_command()
    async def ping(inter):
        '''/ping: Get the bot's latency'''
        await inter.response.send_message(f"Pong! ({inter.bot.latency * 1000:.0f}ms)")

    @sus.sub_command()
    async def helpme(inter):
        '''/helpme: Show this help message'''
        msg = 'Here are several things I can do:'

        command_set = self.bot.get_guild_slash_commands(inter.guild.id)
        help_msg = []
        for cmd in command_set:
            if cmd.options:
                for opt in cmd.options:
                    help_msg.append(opt.description)
            else:
                help_msg.append(cmd.description)
        
        await inter.response.send_message(msg + "```" + "\n".join(help_msg) + "```")

    @sus.sub_command()
    async def updateme(inter, user: disnake.User):
        '''/updateme @<Discord>: Add someone to the handle update list'''
        jsontask.add_to_update(inter.guild.id, user.id)
        await inter.response.send_message(f"{user.mention} has been added to the update list")

    @sus.sub_command()
    async def refresh(inter):
        '''/refresh: Refresh all color-based roles'''
        tasklist = jsontask.get_update_list()
        for guildid in tasklist:
            rolelist = jsontask.get_roles(guildid)
            guild = self.bot.get_guild(int(guildid))
            print(int(guildid))
            print(tasklist)
            if guild is None:
                print(f"{guildid} cannot be updated")
                continue
            if rolelist is None:
                print("No rolelist found")
                # TODO: Add relevant roles 
                pass
            for userid in tasklist[guildid]:
                user = guild.get_member(int(userid))
                if user is None:
                    print(f"{userid} not found")
                    continue
                for role in user.roles:
                    if role.id in rolelist:
                        await user.remove_role(role)
                handle = src.Codeforces.Commands.jsontask.gethandle(userid)
                rankname = src.Codeforces.Funcs.getRoles([handle])[0]
                rolefromrank = guild.get_role(rolelist[rankname])
                await user.add_roles(rolefromrank)
        await inter.response.send_message("All roles refreshed")