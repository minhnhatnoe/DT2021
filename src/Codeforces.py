from src.imports import *
from src import Funcs


class CFCommand(commands.Cog):
    "A cog for all of commands regarding Codeforces"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def cf(inter, *args):
        pass

    @cf.sub_command()
    async def assign(self, inter, user: disnake.User, handle: str):
        '''/cf assign <CF Handle>: Let the bot know your Codeforces handle'''
        try:
            embedobj = await Funcs.CFExternal.get_user_embed(handle, user.id)
            await inter.response.send_message(f"{user.mention} has been introduced as {handle}", embed=embedobj)
            Funcs.CFInternal.assign_handle(user.id, handle)
        except Exception as inst:
            if str(inst) == "Handle Error":
                await inter.response.send_message(f"Error occurred. Please carefully check provided handle")
            else:
                await inter.response.send_message(f"How did u trigger that?")

    @cf.sub_command()
    async def info(self, inter, user: disnake.User):
        '''/cf info @<Discord>: Get someone's CF handle'''
        await inter.response.defer()
        handle = Funcs.CFInternal.get_handle(user.id)
        if handle is None:
            await inter.edit_original_message(content = f"{user.mention} has not been introduced yet")
        else:
            await inter.edit_original_message(embed=await Funcs.CFExternal.get_user_embed(handle, user.name))


def setup(bot: commands.Bot):
    bot.add_cog(CFCommand(bot))
