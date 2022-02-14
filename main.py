from disnake.ext import commands
import os  # TODO: Minimize footprint of os
from dotenv import load_dotenv

guilds = [934020662765453312]
bot = commands.Bot(test_guilds=guilds)

@bot.slash_command()
async def ping(inter):
    '''/ping: Get the bot's latency'''
    await inter.response.send_message(f"Pong! ({inter.bot.latency * 1000:.0f}ms)")

@bot.slash_command()
async def helpme(inter):
    '''/helpme: Get help'''
    message = '''
    Here are several things I can do:
        1. /introduce <CF Handle>: Let the bot know your Codeforces handle
        2. /query @<Discord>: Get someone's CF handle
        3. /help: You just used this
    '''

@bot.event
async def on_ready():
    print("Logged in")

bot.load_extension("src.Codeforces.Commands")

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get("TOKEN"))