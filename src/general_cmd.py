'''General commands regarding the bot'''
from secrets import choice
from disnake.ext import commands
import disnake
from src.utils import user_funcs
from src.utils import guild_funcs
from src.utils.constants import UPDATECHOICES, UPDATECHOICELIST


class GeneralCommand(commands.Cog):
    "A cog for all of commands regarding general Discord stuff"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def gen(self, inter: disnake.CommandInteraction, *args):
        '''General commands family'''

    @gen.sub_command()
    async def ping(self, inter: disnake.CommandInteraction): # pylint: disable=no-self-use
        '''/gen ping: Get the bot's latency'''
        await inter.response.send_message(f"Pong! ({inter.bot.latency * 1000:.0f}ms)")

    @gen.sub_command()
    async def update(self, inter: disnake.CommandInteraction, user: disnake.User, # pylint: disable=no-self-use
                     choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/gen update @<Discord>: Add someone to the handle update list'''
        message_content = str()
        choice = choice.title()
        if choice in UPDATECHOICES:
            user_funcs.update_change(user, UPDATECHOICES[choice])
            message_content = f"{user.mention} will be updated by {choice}"
        else:
            message_content = f"{choice} is not a valid option"
        await inter.response.send_message(message_content)

    @gen.sub_command()
    async def silent(self, inter: disnake.CommandInteraction, user: disnake.User, # pylint: disable=no-self-use
                     choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/gen update @<Discord>: Add someone to the handle update list without mention'''
        message_content = str()
        choice = choice.title()
        if choice in UPDATECHOICES:
            user_funcs.update_change(user, UPDATECHOICES[choice])
            message_content = f"{user.display_name} has been added to the update with {choice}"
        else:
            message_content = f"{choice} is not a valid option"
        await inter.response.send_message(message_content)

    @gen.sub_command()
    async def refresh(self, inter: disnake.CommandInteraction):
        '''/gen refresh: Refresh all color-based roles'''
        await inter.response.defer()
        await guild_funcs.refresh_roles(self.bot)
        await inter.edit_original_message(content="All roles refreshed")

    @gen.sub_command()
    async def clear(self, inter: disnake.CommandInteraction): # pylint: disable=no-self-use
        '''/gen clear: Clear all roles with matching names from server'''
        await inter.response.defer()
        await guild_funcs.delete_roles(inter.guild)
        await inter.edit_original_message(content="All roles cleared")

    @gen.sub_command()
    async def dump(self, inter: disnake.CommandInteraction,
                   choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/gen dump: Make the bot DM you a list off all Codeforces handles'''
        choice = choice.title()
        if choice in UPDATECHOICES:
            data_dump = user_funcs.dump_all_handle(self.bot, UPDATECHOICES[choice])
            await inter.user.send(data_dump)
            message_content = "Sent!"
        else:
            message_content = f"{choice} is not a valid option"
        await inter.response.send_message(message_content)

def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(GeneralCommand(bot))
