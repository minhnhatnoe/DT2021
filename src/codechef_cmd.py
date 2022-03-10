'''Commands relating to Codechef'''

import disnake
from disnake.ext import commands
from src.utils.json_file import load_from_json, write_to_json
from src.utils import guild_funcs
from src.utils.Codechef import cc_external
from src.utils import user_funcs


class CodechefCommand(commands.Cog):
    '''A cog for all commands relating to Codechef'''

    def __init__(self, bot=commands.Bot):
        '''Assign bot for future use'''
        self.bot = bot

    @commands.slash_command(name="cc")
    async def codechef(inter, *args):
        '''Slash command group for Codechef command'''

    @codechef.sub_command()
    async def assign(inter, user: disnake.User, username: str):
        '''/cc assign <Discord user> <Codechef username>: Assign an user to an username'''
        await inter.response.defer()
        user_funcs.assign_handle(user.id, username, 2)
        user_funcs.update_change(inter.guild.id, user.id, 2)


def setup(bot: commands.Bot):
    '''Add the cog to bot'''
    bot.add_cog(CodechefCommand(bot))
