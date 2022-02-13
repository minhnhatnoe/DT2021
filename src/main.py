import disnake
from disnake.ext import commands
import os  # TODO: Minimize footprint of os
from dotenv import load_dotenv
import json

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
        json_data[inter.author.id] = handle
        json.dump(json_data, json_file)
        json_file.truncate()
    await inter.response.send_message(f"{inter.author.mention} has been introduced as {handle}")

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get("TOKEN"))