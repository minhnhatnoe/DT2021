'''Commands regarding Codeforces'''
import disnake
from disnake.ext import commands
from src import funcs


class CFCommand(commands.Cog):
    "A cog for all of commands regarding Codeforces"

    def __init__(self, bot: commands.Bot):
        '''Assign bot for future use'''
        self.bot = bot

    @commands.slash_command(name = 'cf')
    async def codeforces(inter, *args):
        '''cf family'''

    @codeforces.sub_command()
    async def assign(self, inter, user: disnake.User, handle: str):
        '''/cf assign <CF Handle>: Let the bot know your Codeforces handle'''
        try:
            embedobj = await funcs.CFExternal.get_user_embed(handle, user.id)
            await inter.response.send_message(
                f"{user.mention} has been introduced as {handle}",
                embed=embedobj
            )
            funcs.CFInternal.assign_handle(user.id, handle)
            funcs.UserFuncs.add_to_update(inter.guild.id, user.id)
        except Exception as inst:
            if str(inst) == "Handle Error":
                await inter.response.send_message(
                    "Error occurred. Please carefully check provided handle"
                )
            else:
                await inter.response.send_message("How did u trigger that?")

    @codeforces.sub_command()
    async def info(self, inter, user: disnake.User):
        '''/cf info @<Discord>: Get someone's CF handle'''
        await inter.response.defer()
        handle = funcs.CFInternal.get_handle(user.id)
        if handle is None:
            await inter.edit_original_message(
                content = f"{user.mention} has not been introduced yet"
            )
        else:
            await inter.edit_original_message(
                embed=await funcs.CFExternal.get_user_embed(handle, user.name)
            )


def setup(bot: commands.Bot):
    '''Add the "cf" cog'''
    bot.add_cog(CFCommand(bot))
