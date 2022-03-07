'''General commands regarding the bot'''
from ast import Param
from enum import auto
from turtle import update
from disnake.ext import commands
import disnake
from src import user_funcs
from src.utils.Codeforces import guild_funcs

update_choice = {
    "None": 0,
    "Codeforces": 1,
    "Codechef": 2
}


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

    async def autocomplete_update(interaction: disnake.ApplicationCommandInteraction, string: str):
        '''Autocomplete function for update platform choice'''
        return list(
            filter(
                lambda platform: string in platform,
                update_choice.keys()
            )
        )

    @gen.sub_command()
    async def update(inter, user: disnake.User, choice: str = Param(
        description="Update choice", autocomplete=autocomplete_update
    )):
        '''/gen update @<Discord>: Add someone to the handle update list'''
        if choice in update_choice:
            user_funcs.update_change(
                inter.guild.id, user.id, update_choice[choice])
            await inter.response.send_message(
                f"{user.mention} has been added to the update with {choice}"
            )
        else:
            await inter.response.send_message(f"{choice} is not a valid option")

    @gen.sub_command()
    async def silent(inter, user: disnake.User):
        '''/gen silent @<Discord>: same as update, but no mention'''
        user_funcs.update_change(inter.guild.id, user.id, True)
        await inter.response.send_message(f"{user.name} has been added to the update list")

    @gen.sub_command()
    async def refresh(inter):
        '''/gen refresh: Refresh all color-based roles'''
        await inter.response.defer()
        await guild_funcs.refresh_roles([inter.guild])
        await inter.edit_original_message(content="All roles refreshed")

    @gen.sub_command()
    async def clear(inter):
        '''/gen clear: Clear all roles created in the server'''
        await inter.response.defer()
        guild = inter.guild
        guildroles = guild_funcs.get_roles(guild.id)
        if guildroles is None:
            return
        for roleid in guildroles.values():
            role = guild.get_role(int(roleid))
            if role is not None:
                await role.delete()
        guild_funcs.remove_guild(guild.id)
        await inter.edit_original_message(content="All roles cleared")


def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(GeneralCommand(bot))
