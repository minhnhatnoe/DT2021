'''Master Bot code'''
from os import environ
from dotenv import load_dotenv
import disnake
from disnake.ext import commands
from src import keep_alive

load_dotenv()
guilds = [int(v) for v in environ.get("TEST_GUILDS").split(",")]
bot = commands.Bot(test_guilds=guilds, intents=disnake.Intents.all())

EXTENSIONLIST = ["general_cmd", "codeforces_cmd", "codechef_cmd", "bot_extension"]
for extension in EXTENSIONLIST:
    bot.load_extension(f"src.{extension}")

if __name__ == "__main__":
    load_dotenv()
    keep_alive.keep_alive()
    bot.run(environ.get("TOKEN"))
