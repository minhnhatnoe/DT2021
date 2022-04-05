'''All network comms, with expo backoff'''
from asyncio import sleep
from typing import Callable
import aiohttp
from disnake.ext import commands
from src.utils.bot_funcs import Presence

# To bypass codechef's anti-crawler
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36"}  # pylint: disable=line-too-long


async def get_net(bot: commands.Bot, request_url: str, trial: Callable,
                  exception_to_catch=aiohttp.ClientPayloadError):
    '''Get data with expo backoff. Catch is list of exception. Trial is function to try catch'''

    backoff_period = 1
    async with Presence(bot) as bot_state:
        while True:
            try:
                from_net: str
                async with aiohttp.ClientSession(headers=HEADERS) as session:
                    async with session.get(request_url) as response:
                        from_net = await response.text()
                trial(from_net)
                return from_net
            except (exception_to_catch, aiohttp.ClientPayloadError) as ex_type:
                if backoff_period >= 256:  # 9 is limit due to Discord's 900sec limit
                    raise Exception("Backoff timeout") from ex_type
                await bot_state.presence_change(
                    f"CF server down, waiting for {backoff_period} seconds")
                await sleep(backoff_period)
                backoff_period *= 2
