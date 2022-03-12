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
    async def codechef(self, inter: disnake.CommandInteraction, *args):
        '''Slash command group for Codechef command'''

    @codechef.sub_command()
    async def assign(self, inter: disnake.CommandInteraction, # pylint: disable=no-self-use
                     user: disnake.User, username: str = ""):
        '''/cc assign <Discord user> <Codechef username>: Link user to username, delete if blank'''
        await inter.response.defer()
        user_funcs.assign_handle(user, username, 2)
        if username == "":
            message_content = f"{user.mention} is unlinked"
        else:
            message_content = f"{user.mention} is linked with Codechef account {username}"

        await inter.edit_original_message(content=message_content)


def setup(bot: commands.Bot):
    '''Add the cog to bot'''
    bot.add_cog(CodechefCommand(bot))
