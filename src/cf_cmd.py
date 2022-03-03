'''Commands regarding Codeforces'''
import disnake
from disnake.ext import commands
from src.funcs import cf_external, cf_internal, user_funcs


class CFCommand(commands.Cog):
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
            embedobj = await cf_external.get_user_embed(handle, user.id)
            await inter.response.send_message(
                f"{user.mention} has been introduced as {handle}",
                embed=embedobj
            )
            cf_internal.assign_handle(user.id, handle)
            user_funcs.update_change(inter.guild.id, user.id, True)
        except cf_external.CFApi as inst:
            if str(inst) == "Handle Error":
                await inter.response.send_message(
                    "Error occurred. Please carefully check provided handle"
                )
            else:
                await inter.response.send_message(
                    f"How did u trigger that? (Error code: {str(inst)})"
                )

    @codeforces.sub_command()
    async def info(inter, user: disnake.User):
        '''/cf info @<Discord>: Get someone's CF handle'''
        await inter.response.defer()
        handle = cf_internal.get_handle(user.id)
        if handle is None:
            await inter.edit_original_message(
                content=f"{user.mention} has not been introduced yet"
            )
        else:
            await inter.edit_original_message(
                embed=await cf_external.get_user_embed(handle, user.name)
            )


def setup(bot: commands.Bot):
    '''Add the "cf" cog'''
    bot.add_cog(CFCommand(bot))
