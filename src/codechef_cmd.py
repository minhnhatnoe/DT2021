'''Commands relating to Codechef'''

import disnake
from disnake.ext import commands
from src.utils import user_funcs


class CodechefCommand(commands.Cog):
    '''A cog for all commands relating to Codechef'''

    def __init__(self, bot=commands.Bot):
        '''Assign bot for future use'''
        self.bot = bot

    @commands.slash_command(name="cc")
    async def codechef(inter: disnake.CommandInteraction, *args):
        '''Slash command group for Codechef command'''

    @codechef.sub_command()
    async def assign(inter: disnake.CommandInteraction, user: disnake.User, username: str):
        '''/cc assign <Discord user> <Codechef username>: Assign an user to an username'''
        await inter.response.defer()
        user_funcs.assign_handle(user, username, 2)
        user_funcs.update_change(user, 2)
        await inter.edit_original_message(content=f"{user.mention} is linked with Codechef account {username}")

def setup(bot: commands.Bot):
    '''Add the cog to bot'''
    bot.add_cog(CodechefCommand(bot))
