'''Codefun API Interaction'''
import json
from typing import Dict
from src.utils import network
import disnake
from disnake import Embed
from disnake.ext import commands


class CodeFunApi(Exception):
    '''Base class for all exceptions from Codefun'''
    class NotFound(Exception):
        '''Class if not found'''


class CodeFun:
    '''Codefun-related tasks'''

    RANKCOLOR = {
        "Codefun-Newbie": 0x000000,
        "Codefun-Beginner": 0x000000,
        "Codefun-Novice": 0x000000,
        "Codefun-Coder": 0x000000,
        "Codefun-Expert": 0x000000,
        "Codefun-Master": 0x000000,
        "Codefun-Hacker": 0x000000,
        "Codefun-Grandmaster": 0x000000
    }

    PLATFORM_CODE = {
        "Codefun": 4
    }

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def verify(self, member: disnake.Member, handle: str) -> bool:  # pylint: disable=unused-argument, no-self-use
        # TODO
        return True

    async def generate_user_embed(self, handle: str, member: disnake.Member) -> Embed:
        '''Generate user embed from server data'''


async def get_user_data_from_net(bot: commands.Bot, user: str) -> Dict:
    '''Get a person data from Codefun'''
    request_url = f"https://codefun.vn/api/users/{user}"
    try:
        from_net = await network.get_net(bot, request_url, json.loads, json.JSONDecodeError)
    except Exception as ex_type:
        if str(ex_type) == "Not Found":
            raise CodeFunApi.NotFound(
                Exception("Provided handle not found")) from ex_type
        raise CodeFunApi(Exception("Error")) from ex_type

    json_data = json.loads(from_net)
    if "error" in json_data:
        raise CodeFunApi(Exception(json_data["error"]))
    return json_data["data"]
