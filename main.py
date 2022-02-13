from disnake.ext import commands
import os  # TODO: Minimize footprint of os
from dotenv import load_dotenv

guilds = [934020662765453312]
bot = commands.Bot(test_guilds=guilds)

@bot.event
async def on_ready():
    print("Logged in")

bot.load_extension("src.Codeforces.Commands")

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get("TOKEN"))