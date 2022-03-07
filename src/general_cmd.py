'''General commands regarding the bot'''
from ast import Param
from email import message
from enum import auto
from turtle import update
from disnake.ext import commands
import disnake
from src.utils import user_funcs
from src.utils import guild_funcs

UPDATECHOICES = {
    "None": 0,
    "Codeforces": 1,
    "Codechef": 2
}


async def autocomplete_update(inter: disnake.ApplicationCommandInteraction, string: str):
    '''Autocomplete function for update platform choice'''
    string = string.lower()
    return [choice for choice in UPDATECHOICES.keys() if string in choice.lower()]


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
    async def update(inter, user: disnake.User, choice: str = commands.Param(
            autocomplete=autocomplete_update)):
        '''/gen update @<Discord>: Add someone to the handle update list'''
        message_content = str()

        if choice in UPDATECHOICES:
            user_funcs.update_change(
                inter.guild.id, user.id, UPDATECHOICES[choice])
            message_content = f"{user.mention} will be updated by {choice}"
        else:
            message_content = f"{choice} is not a valid option"
        await inter.response.send_message(message_content)

    @gen.sub_command()
    async def silent(inter, user: disnake.User, choice: str = commands.Param(
            autocomplete=autocomplete_update)):
        '''/gen update @<Discord>: Add someone to the handle update list'''
        message_content = str()

        if choice in UPDATECHOICES:
            guild_id = inter.guild.id
            user_id = user.id
            user_funcs.update_change(guild_id, user_id, UPDATECHOICES[choice])
            message_content = f"{user.name} has been added to the update with {choice}"
        else:
            message_content = f"{choice} is not a valid option"
        await inter.response.send_message(message_content)

    @gen.sub_command()
    async def refresh(self, inter):
        '''/gen refresh: Refresh all color-based roles'''
        await inter.response.defer()
        await guild_funcs.refresh_roles(self.bot)
        await inter.edit_original_message(content="All roles refreshed")

    @gen.sub_command()
    async def clear(inter: disnake.CommandInteraction):
        '''/gen clear: Clear all roles with matching names from server'''
        await inter.response.defer()
        guild = inter.guild
        for role in guild.roles:
            if role.name in guild_funcs.RANKCOLOR:
                await role.delete()
        guild_funcs.remove_guild(guild.id)
        await inter.edit_original_message(content="All roles cleared")


def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(GeneralCommand(bot))
