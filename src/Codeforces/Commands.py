import json
import disnake
import os
from dotenv import load_dotenv
from src.Codeforces import Funcs
from disnake.ext import commands

class jsontask:
    def gethandle(userid: str):
        userid = str(userid)
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\\handle.json", "r") as json_file:
            json_data = json.load(json_file)
            if userid in json_data:
                return json_data[userid]
            else:
                return None
    def assignhandle(userid: str, handle: str):
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\\handle.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data[userid] = handle
            json.dump(json_data, json_file)
            json_file.truncate()

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
        jsontask.assignhandle(inter.author.id, handle)
        await inter.response.send_message(f"{inter.author.mention} has been introduced as {handle}")

    @cf.sub_command()
    async def info(inter, user: disnake.User):
        '''/cf info @<Discord>: Get someone's CF handle'''
        handle = jsontask.gethandle(user.id)
        if handle is None:
            await inter.response.send_message(f"{user.mention} has not been introduced yet")
        else:
            await inter.response.send_message(f"{user.mention}'s handle is {handle}")
                
def setup(bot: commands.Bot):
    bot.add_cog(CFCommand(bot))