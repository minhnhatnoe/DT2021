'''Entry point for application'''
import asyncio
from os import environ

import aiohttp
from dotenv import load_dotenv
import disnake
from disnake.ext import commands

from src import cfg, keep_alive


async def check_instance(request_url: str) -> bool:
    '''Check if live deploy version is running'''
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as response:
                return response.status != 200
    except Exception as inst:  # pylint: disable=broad-except
        print(f"Cannot reach deploy, error code: {inst}")
        return True


def check_deploy_running():
    '''Check if the deployment version is currently running'''
    load_dotenv()
    deploy_server = environ.get("DEPLOY_ADDRESS", "None")
    check: bool
    if deploy_server != "None":
        print(f"Checking live deployment at {deploy_server}...")
        print("Disable this by removing the variable named DEPLOY_ADDRESS in .env!")
        async_process = check_instance(deploy_server)
        event_loop = asyncio.get_event_loop()
        check = event_loop.run_until_complete(async_process)
    else:
        check = True

    if check:
        return True
    else:
        print(f"Deployment instance active at {deploy_server}. Terminating...")
        return False


def load_bot():
    '''Load the bot up'''
    load_dotenv()
    guilds = [int(v) for v in environ.get("TEST_GUILDS").split(",")]
    cfg.bot = commands.Bot(test_guilds=guilds, intents=disnake.Intents.all())

    EXTENSIONLIST = ["guild_commands", "user_commands",
                     "admin_commands", "bot_extension"]
    for extension in EXTENSIONLIST:
        cfg.bot.load_extension(f"src.cogs.{extension}")


def deploy():
    '''Run in deploy mode'''
    keep_alive.keep_alive()
    load_bot()
    load_dotenv()
    cfg.bot.run(environ.get("TOKEN"))


def local():
    if check_deploy_running():
        load_bot()
        load_dotenv()
        cfg.bot.run(environ.get("TOKEN"))
