from os import environ
import asyncio
import aiohttp
from dotenv import load_dotenv
import disnake
from disnake.ext import commands
from src import keep_alive

load_dotenv()
guilds = [int(v) for v in environ.get("TEST_GUILDS").split(",")]
bot = commands.Bot(test_guilds=guilds, intents=disnake.Intents.all())

EXTENSIONLIST = ["general_cmd", "codeforces_cmd",
                 "codechef_cmd", "bot_extension"]
for extension in EXTENSIONLIST:
    bot.load_extension(f"src.{extension}")

async def check_instance(request_url: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(environ.get("DEPLOY_ADDRESS")) as response:
            return response.status != 200

def deploy():
    keep_alive.keep_alive()
    bot.run(environ.get("TOKEN"))

def local():
    deploy_server = environ.get("DEPLOY_ADDRESS", "None")
    if deploy_server != "None":
        print(f"Checking live deployment at {deploy_server}. Disable this by removing var in .env")
        check = asyncio.get_event_loop().run_until_complete(check_instance(deploy_server))
    if check:
        bot.run(environ.get("TOKEN"))
    else:
        print(f"Deployment instance active at {deploy_server}. Terminating")
