'''Entry point for application'''
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
token = environ.get("TOKEN")

EXTENSIONLIST = ["general_cmd", "codeforces_cmd",
                 "codechef_cmd", "bot_extension"]
for extension in EXTENSIONLIST:
    bot.load_extension(f"src.{extension}")


async def check_instance(request_url: str) -> bool:
    '''Check if live deploy version is running'''
    async with aiohttp.ClientSession() as session:
        async with session.get(request_url) as response:
            return response.status != 200


def deploy():
    '''Run in deploy mode'''
    keep_alive.keep_alive()
    bot.run(token)


def local():
    '''Run in local mode'''
    deploy_server = environ.get("DEPLOY_ADDRESS", "None")
    check = False
    if deploy_server != "None":
        print(
            f"Checking live deployment at {deploy_server}. Disable this by removing the variable named DEPLOY_ADDRESS in .env!")  # pylint: disable=line-too-long
        async_process = check_instance(deploy_server)
        event_loop = asyncio.get_event_loop()
        check = event_loop.run_until_complete(async_process)

    if check:
        bot.run(token)
    else:
        print(f"Deployment instance active at {deploy_server}. Terminating...")
