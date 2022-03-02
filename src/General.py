from src.imports import *
from src import Funcs


class GeneralCommand(commands.Cog):
    "A cog for all of commands regarding general Discord stuff"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def gen(inter, *args):
        pass

    @gen.sub_command()
    async def ping(self, inter):
        '''/gen ping: Get the bot's latency'''
        await inter.response.send_message(f"Pong! ({inter.bot.latency * 1000:.0f}ms)")

    @gen.sub_command()
    async def update(self, inter, user: disnake.User):
        '''/gen updateme @<Discord>: Add someone to the handle update list'''
        Funcs.UserFuncs.add_to_update(inter.guild.id, user.id)
        await inter.response.send_message(f"{user.mention} has been added to the update list")

    @gen.sub_command()
    async def refresh(self, inter):
        '''/gen refresh: Refresh all color-based roles'''
        await inter.response.defer()
        cfquery = {}
        guildid = str(inter.guild.id)
        tasklist = Funcs.GuildFuncs.get_update_list(guildid)
        rolelist = Funcs.GuildFuncs.get_roles(guildid)
        guild = self.bot.get_guild(int(guildid))

        if guild is None:
            print(f"{guildid} cannot be updated")
            return
        if rolelist is None:
            print(f"No rolelist found in {guildid}")
            await Funcs.GuildFuncs.make_roles(inter.guild)

        for userid in tasklist:
            user = guild.get_member(int(userid))
            if user is None:
                print(f"{userid} in {guildid} not found")
                continue
            for role in user.roles:
                if role.id in rolelist.values():
                    await user.remove_roles(role)
            handle = Funcs.CFInternal.get_handle(userid)
            if handle is not None:
                cfquery[handle] = user

        ranks = await Funcs.CFExternal.get_roles([key for key in cfquery])
        for (handle, user), rankname in zip(cfquery.items(), ranks):
            rolefromrank = guild.get_role(rolelist[rankname])
            await user.add_roles(rolefromrank)
        await inter.edit_original_message(content="All roles refreshed")


def setup(bot: commands.Bot):
    bot.add_cog(GeneralCommand(bot))
