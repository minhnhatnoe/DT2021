import json
import disnake
import os
from dotenv import load_dotenv
from src.Codeforces import Funcs
from disnake.ext import commands
from src.jsontask import jsontask

class CFCommand(commands.Cog):
    "A cog for all of commands regarding Codeforces"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def cf(inter, *args):
        pass

    @cf.sub_command()
    async def assign(self, inter, handle: str):
        '''/cf assign <CF Handle>: Let the bot know your Codeforces handle'''
        try:
            embedobj = await Funcs.getUserEmbed(handle, inter.user.id)
            await inter.response.send_message(f"{inter.author.mention} has been introduced as {handle}", embed = embedobj)
            jsontask.assign_handle(inter.author.id, handle)
        except:
            await inter.response.send_message(f"Error occurred. Please carefully check provided handle")

    @cf.sub_command()
    async def info(self, inter, user: disnake.User):
        '''/cf info @<Discord>: Get someone's CF handle'''
        handle = jsontask.get_handle(user.id)
        if handle is None:
            await inter.response.send_message(f"{user.mention} has not been introduced yet")
        else:
            await inter.response.send_message(f"{user.mention}'s handle is {handle}", embed = await Funcs.getUserEmbed(handle, user.name))
                
def setup(bot: commands.Bot):
    bot.add_cog(CFCommand(bot))