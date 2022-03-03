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
        '''/gen update @<Discord>: Add someone to the handle update list'''
        Funcs.UserFuncs.add_to_update(inter.guild.id, user.id)
        await inter.response.send_message(f"{user.mention} has been added to the update list")

    @gen.sub_command()
    async def notupdate(self, inter, user: disnake.User):
        '''gen/ notupdate @<Discord>: Remove someone from the update list'''
        Funcs.UserFuncs.delete_from_update(inter.guild.id, user.id)
        await Funcs.UserFuncs.clear_user_role(inter.guild, user)
        await inter.response.send_message(f"{user.mention} has been removed from the update list")

    @gen.sub_command()
    async def silent(self, inter, user: disnake.User):
        '''/gen silent @<Discord>: same as update, but no mention'''
        Funcs.UserFuncs.add_to_update(inter.guild.id, user.id)
        await inter.response.send_message(f"{user.name} has been added to the update list")

    @gen.sub_command()
    async def refresh(self, inter):
        '''/gen refresh: Refresh all color-based roles'''
        await inter.response.defer()
        await Funcs.GuildFuncs.refresh_roles([inter.guild])
        await inter.edit_original_message(content="All roles refreshed")

    @gen.sub_command()
    async def clear(inter):
        '''/gen clear: Clear all roles created in the server'''
        await inter.response.defer()
        guild = inter.guild
        guildroles = Funcs.GuildFuncs.get_roles(guild.id)
        if guildroles is None:
            return
        for roleid in guildroles.values():
            role = guild.get_role(int(roleid))
            if role is not None:
                await role.delete()
        Funcs.GuildFuncs.remove_guild(guild.id)
        await inter.edit_original_message(content="All roles cleared")


def setup(bot: commands.Bot):
    bot.add_cog(GeneralCommand(bot))
