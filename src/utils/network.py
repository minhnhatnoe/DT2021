'''All network comms, with expo backoff'''
from asyncio import sleep
from typing import Callable
import aiohttp
from disnake.ext import commands
from src.utils.bot_funcs import Presence

async def get_net(bot: commands.Bot, request_url: str, trial: Callable, catch_list):
    '''Get data with expo backoff. Catch is list of exception. Trial is function to try catch'''

    catch_list.append(aiohttp.ClientPayloadError)
    backoff_period = 1
    async with Presence(bot) as bot_state:
        while True:
            try:
                from_net: str
                async with aiohttp.ClientSession() as session:
                    async with session.get(request_url) as response:
                        from_net = await response.text()
                trial(from_net)
                return from_net
            except catch_list as ex_type: # pylint: disable=catching-non-exception
                if backoff_period >= 256:  # 9 is limit due to Discord's 900sec limit
                    raise Exception("Backoff timeout") from ex_type # pylint: disable=bad-exception-context
                await bot_state.presence_change(
                    f"CF server down, waiting for {backoff_period} seconds")
                await sleep(backoff_period)
                backoff_period *= 2
