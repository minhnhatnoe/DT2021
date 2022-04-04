import disnake
from disnake.ext import commands
from src.utils import guild_funcs, user_funcs
from src.utils.constants import UPDATECHOICES, UPDATECHOICELIST


class GuildCommand(commands.Cog):
    "A cog for all of commands regarding general Discord stuff"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def user(self, inter: disnake.CommandInteraction, *args):
        '''General commands family'''
    
    @user.sub_command()
    async def refresh(self, inter: disnake.CommandInteraction):
        '''/gen refresh: Refresh all color-based roles'''
        await inter.response.defer()
        await guild_funcs.refresh_roles_of_bot(self.bot)
        await inter.edit_original_message(content="All roles refreshed")

    @user.sub_command() # TODO
    async def clear(self, inter: disnake.CommandInteraction):  # pylint: disable=no-self-use
        '''/gen clear: Clear all roles with matching names from server'''
        await inter.response.defer()
        await guild_funcs.remove_roles_in_guild(inter.guild)
        await inter.edit_original_message(content="All roles cleared")

    @user.sub_command()
    async def dump(self, inter: disnake.CommandInteraction,
                   choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/gen dump: Make the bot DM you a list off all Codeforces handles'''
        data_dump = user_funcs.handle_database_dump(
            self.bot, UPDATECHOICES[choice])
        await inter.user.send(data_dump)
        await inter.response.send_message("Sent!")


def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(UserCommand(bot))
