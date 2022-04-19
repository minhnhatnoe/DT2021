'''Module for guild commands'''
import disnake
from disnake.ext import commands
from src import cfg
from src.utils import handle_functions, refresh_procedure
from src.utils.platform_class import UPDATECHOICES, UPDATECHOICELIST


class GuildCommand(commands.Cog):
    "A cog for all of commands regarding general Discord stuff"

    def __init__(self):
        self.bot = cfg.bot

    @commands.slash_command()
    async def guild(self, inter: disnake.CommandInteraction, *args):
        '''Guild commands family'''

    @guild.sub_command()
    async def refresh(self, inter: disnake.CommandInteraction):
        '''/guild refresh: Refresh all color-based roles'''
        await inter.response.defer()
        await refresh_procedure.refresh_roles_of_bot()
        await inter.edit_original_message(content="All roles refreshed")

    @guild.sub_command()
    async def dump(self, inter: disnake.CommandInteraction,
                   choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/guild dump: Make the bot DM you a list off all handles from a platform'''
        data_dump = handle_functions.handle_database_dump(UPDATECHOICES[choice])
        await inter.user.send(data_dump)
        await inter.response.send_message("Sent!")


def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(GuildCommand())
