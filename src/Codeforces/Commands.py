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
    async def introduce(inter, handle: str):
        '''/introduce <CF Handle>: Let the bot know your Codeforces handle'''
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\handle.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data[str(inter.author.id)] = handle
            json.dump(json_data, json_file)
            json_file.truncate()
        await inter.response.send_message(f"{inter.author.mention} has been introduced as {handle}")

    @commands.slash_command()
    async def query(inter, dischand: disnake.User):
        '''/query @<Discord>: Get someone's CF handle'''
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\handle.json", "r") as json_file:
            json_data = json.load(json_file)
            if str(dischand.id) in json_data:
                await inter.response.send_message(f"{dischand.mention} is {json_data[str(dischand.id)]}", embed=Funcs.userEmbed(json_data[str(dischand.id)], dischand))
            else:
                await inter.response.send_message(f"{dischand.mention} has not been introduced yet")

    @commands.slash_command()
    async def ping(inter):
        '''/ping: Get the bot's latency'''
        await inter.response.send_message("Pong!")

    @commands.slash_command()
    async def helpme(inter):
        '''/helpme: Get help'''
        message = '''
        Here are several things I can do:
            1. /introduce <CF Handle>: Let the bot know your Codeforces handle
            2. /query @<Discord>: Get someone's CF handle
            3. /help: You just used this
        '''
def setup(bot: commands.Bot):
    bot.add_cog(CFCommand(bot))