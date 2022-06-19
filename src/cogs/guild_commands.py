'''Module for guild commands'''
import disnake
from disnake.ext import commands
from src import cfg
from src.utils import refresh_procedure


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

def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(GuildCommand())
