'''Commands relating to Codechef'''

import disnake
from disnake.ext import commands
from src.funcs.json_file import load_from_json, write_to_json

class CodechefCommand(commands.Cog):
    '''A cog for all commands relating to Codechef'''

    def __init__(self, bot = commands.Bot):
        '''Assign bot for future use'''
        self.bot = bot

    @commands.slash_command(name = "cc")
    async def codechef(inter, *args):
        '''Slash command group for Codechef command'''

    @codechef.sub_command()
    async def assign(inter, user: disnake.User, username: str):
        '''/cc assign <Discord user> <Codechef username>: Assign an user to an username'''
        await inter.response.defer()

        data = load_from_json("/Codechef/username")
        current_guild_id = inter.guild.id
        userid = user.id

        if str(current_guild_id) not in data:
            data[str(current_guild_id)] = dict()

        data[str(current_guild_id)][str(userid)] = username

        write_to_json("/Codechef/username", data)

        await inter.edit_original_message(
            content = f"{user.mention} has been assigned to {username}"
        )

def setup(bot: commands.Bot):
    '''Add the cog to bot'''
    bot.add_cog(CodechefCommand(bot))