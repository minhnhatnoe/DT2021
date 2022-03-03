'''General commands regarding the bot'''
from disnake.ext import commands
import disnake

from src import funcs


class GeneralCommand(commands.Cog):
    "A cog for all of commands regarding general Discord stuff"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def gen(inter, *args):
        '''General commands family'''

    @gen.sub_command()
    async def ping(inter):
        '''/gen ping: Get the bot's latency'''
        await inter.response.send_message(f"Pong! ({inter.bot.latency * 1000:.0f}ms)")

    @gen.sub_command()
    async def update(inter, user: disnake.User):
        '''/gen update @<Discord>: Add someone to the handle update list'''
        funcs.UserFuncs.add_to_update(inter.guild.id, user.id)
        await inter.response.send_message(f"{user.mention} has been added to the update list")

    @gen.sub_command()
    async def notupdate(inter, user: disnake.User):
        '''gen/ notupdate @<Discord>: Remove someone from the update list'''
        funcs.UserFuncs.delete_from_update(inter.guild.id, user.id)
        await funcs.UserFuncs.clear_user_role(inter.guild, user)
        await inter.response.send_message(f"{user.mention} has been removed from the update list")

    @gen.sub_command()
    async def silent(inter, user: disnake.User):
        '''/gen silent @<Discord>: same as update, but no mention'''
        funcs.UserFuncs.add_to_update(inter.guild.id, user.id)
        await inter.response.send_message(f"{user.name} has been added to the update list")

    @gen.sub_command()
    async def refresh(inter):
        '''/gen refresh: Refresh all color-based roles'''
        await inter.response.defer()
        await funcs.GuildFuncs.refresh_roles([inter.guild])
        await inter.edit_original_message(content="All roles refreshed")

    @gen.sub_command()
    async def clear(inter):
        '''/gen clear: Clear all roles created in the server'''
        await inter.response.defer()
        guild = inter.guild
        guildroles = funcs.GuildFuncs.get_roles(guild.id)
        if guildroles is None:
            return
        for roleid in guildroles.values():
            role = guild.get_role(int(roleid))
            if role is not None:
                await role.delete()
        funcs.GuildFuncs.remove_guild(guild.id)
        await inter.edit_original_message(content="All roles cleared")


def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(GeneralCommand(bot))
