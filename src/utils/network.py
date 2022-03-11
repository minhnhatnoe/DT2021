from asyncio import sleep
import json
import aiohttp
from disnake.ext import commands
from src.utils.bot_funcs import presence


async def get_net_cf(bot: commands.Bot, request_url: str):
    '''Get data with expo backoff'''
    backoff_period = 1
    async with presence(bot) as bot_state:
        while True:
            try:
                from_net: str
                async with aiohttp.ClientSession() as session:
                    async with session.get(request_url) as response:
                        from_net = await response.text()
                json.loads(from_net)
                return from_net
            except (aiohttp.ClientPayloadError, json.JSONDecodeError) as ex_type:
                if backoff_period >= 256:  # 9 is limit due to Discord's 900sec limit
                    raise Exception("Backoff timeout") from ex_type
                await bot_state.presence_change(f"CF server down, waiting for {backoff_period} seconds")
                await sleep(backoff_period)
                backoff_period *= 2


async def get_net_cc(bot: commands.Bot, request_url: str):
    '''Get data with expo backoff'''
    backoff_period = 1
    async with presence(bot) as bot_state:
        while True:
            try:
                from_net: str
                async with aiohttp.ClientSession() as session:
                    async with session.get(request_url) as response:
                        from_net = await response.text()
                return from_net
            except aiohttp.ClientPayloadError as ex_type:
                if backoff_period >= 256:  # 9 is limit due to Discord's 900sec limit
                    raise Exception("Backoff timeout") from ex_type
                await bot_state.presence_change(f"CF server down, waiting for {backoff_period} seconds")
                await sleep(backoff_period)
                backoff_period *= 2
