import disnake
from disnake.ext import commands
import os  # TODO: Minimize footprint of os
from dotenv import load_dotenv
import json
from src import Funcs
guilds = [934020662765453312]
bot = commands.Bot(test_guilds=guilds)

@bot.event
async def on_ready():
    print("Logged in")

@bot.slash_command()
async def ping(inter):
    await inter.response.send_message("Pong!")

@bot.slash_command()
async def introduce(inter, handle: str):
    # Scheme: /introduce <handle>
    load_dotenv()
    path = os.environ.get("DATAPATH")
    with open(f"{path}\handle.json", "r+") as json_file:
        json_data = json.load(json_file)
        json_file.seek(0)
        json_data[str(inter.author.id)] = handle
        json.dump(json_data, json_file)
        json_file.truncate()
    await inter.response.send_message(f"{inter.author.mention} has been introduced as {handle}")

@bot.slash_command()
async def query(inter, dischand: disnake.User):
    # Scheme: /query <handle>
    load_dotenv()
    path = os.environ.get("DATAPATH")
    with open(f"{path}\handle.json", "r") as json_file:
        json_data = json.load(json_file)
        if str(dischand.id) in json_data:
            await inter.response.send_message(f"{dischand.mention} is {json_data[str(dischand.id)]}", embed=Funcs.userEmbed(json_data[str(dischand.id)], dischand))
        else:
            await inter.response.send_message(f"{dischand.mention} has not been introduced yet")

@bot.slash_command()
async def helpme(inter):
    message = '''
    Here are several things I can do:
        1. /introduce <CF Handle>: Let the bot know your Codeforces handle
        2. /query @<Discord>: Get someone's CF handle
        3. /help: You just used this
    '''

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get("TOKEN"))