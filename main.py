from disnake.ext import commands
import os  # TODO: Minimize footprint of os
from dotenv import load_dotenv

guilds = [934020662765453312]
bot = commands.Bot(test_guilds=guilds)

@bot.event
async def on_ready():
    print("Logged in")

@bot.slash_command()
async def ping(inter):
    await inter.response.send_message("Pong!")

@bot.slash_command()
async def helpme(inter):
    message = '''
    Here are several things I can do:
        1. /introduce <CF Handle>: Let the bot know your Codeforces handle
        2. /query @<Discord>: Get someone's CF handle
        3. /help: You just used this
    '''

bot.load_extension("src.Codeforces.Commands")

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get("TOKEN"))