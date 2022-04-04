'''Module for guild commands'''
import disnake
from disnake.ext import commands
from src.utils import guild_funcs, user_funcs
from src.utils.constants import UPDATECHOICES, UPDATECHOICELIST


class GuildCommand(commands.Cog):
    "A cog for all of commands regarding general Discord stuff"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def guild(self, inter: disnake.CommandInteraction, *args):
        '''Guild commands family'''

    @guild.sub_command()
    async def refresh(self, inter: disnake.CommandInteraction):
        '''/guild refresh: Refresh all color-based roles'''
        await inter.response.defer()
        await guild_funcs.refresh_roles_of_bot(self.bot)
        await inter.edit_original_message(content="All roles refreshed")

    @guild.sub_command()
    async def dump(self, inter: disnake.CommandInteraction,
                   choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/guild dump: Make the bot DM you a list off all handles from a platform'''
        data_dump = user_funcs.handle_database_dump(
            self.bot, UPDATECHOICES[choice])
        await inter.user.send(data_dump)
        await inter.response.send_message("Sent!")


def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(GuildCommand(bot))
