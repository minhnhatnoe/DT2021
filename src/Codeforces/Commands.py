import json
import disnake
import os
from dotenv import load_dotenv
from src.Codeforces import Funcs
from disnake.ext import commands

class CFCommand(commands.Cog):
    "A cog for all of commands regarding Codeforces"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def cf(inter, *args):
        pass

    @cf.sub_command()
    async def assign(inter, handle: str):
        '''/cf assign <CF Handle>: Let the bot know your Codeforces handle'''
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\handle.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data[str(inter.author.id)] = handle
            json.dump(json_data, json_file)
            json_file.truncate()
        await inter.response.send_message(f"{inter.author.mention} has been introduced as {handle}")

    @cf.sub_command()
    async def info(inter, user: disnake.User):
        '''/cf info @<Discord>: Get someone's CF handle'''
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\handle.json", "r") as json_file:
            json_data = json.load(json_file)
            if str(user.id) in json_data:
                await inter.response.send_message(f"{user.mention} is {json_data[str(user.id)]}", embed=Funcs.userEmbed(json_data[str(user.id)], user))
            else:
                await inter.response.send_message(f"{user.mention} has not been introduced yet")
                
def setup(bot: commands.Bot):
    bot.add_cog(CFCommand(bot))