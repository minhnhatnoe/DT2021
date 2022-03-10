'''Commands regarding Codeforces'''
from email import message
import disnake
from disnake.ext import commands
from src.utils import user_funcs
from src.utils.Codeforces import cf_external


class CodeforcesCommand(commands.Cog):
    "A cog for all of commands regarding Codeforces"

    def __init__(self, bot: commands.Bot):
        '''Assign bot for future use'''
        self.bot = bot

    @commands.slash_command(name='cf')
    async def codeforces(inter, *args):
        '''cf family'''

    @codeforces.sub_command()
    async def assign(inter, user: disnake.User, handle: str):
        '''/cf assign <CF Handle>: Let the bot know your Codeforces handle'''
        try:
            embed_obj = await cf_external.generate_user_embed(handle, user.id)
            user_funcs.assign_handle(user.id, handle, 1)
            # Policy: add user to update list after assignment
            user_funcs.update_change(inter.guild.id, user.id, 1)
            await inter.response.send_message(f"{user.mention} introduced as {handle}", embed=embed_obj)
        except cf_external.CFApi as inst:
            message_content = str()
            if str(inst) == "Handle Error":
                message_content = "Error occurred. Check provided handle"
            else:
                message_content = f"How did u trigger that? (Error code: {str(inst)})"
            await inter.response.send_message(message_content)

    @codeforces.sub_command()
    async def info(inter, user: disnake.User):
        '''/cf info @<Discord>: Get someone's CF handle'''
        await inter.response.defer()
        handle = user_funcs.get_handle(user.id, 1)
        if handle is None:
            message_content = f"{user.mention} not introduced yet"
            await inter.edit_original_message(content=message_content)
        else:
            embed_obj = await cf_external.generate_user_embed(handle, user.name)
            await inter.edit_original_message(embed=embed_obj)


def setup(bot: commands.Bot):
    '''Add the "cf" cog'''
    bot.add_cog(CodeforcesCommand(bot))
