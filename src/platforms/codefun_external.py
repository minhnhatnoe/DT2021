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

    PLATFORM_NAME = "Codefun"
    HANDLE_FILE_NAME = "/cfunhandle"
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def get_rank(self, handle: str):
        data = await get_user_data_from_net(self.bot, handle)
        rank = process_rank(data["ratio"])
        return rank

    async def verify(self, member: disnake.Member, handle: str) -> bool:  # pylint: disable=unused-argument, no-self-use
        '''Initialize verification procedure'''
        # TODO
        return True

    async def generate_user_embed(self, handle: str, member: disnake.Member) -> Embed:
        '''Generate user embed from server data'''
        data = await get_user_data_from_net(self.bot, handle)
        rank = process_rank(data["ratio"])
        obj = Embed(
            title=member.display_name,
            color=self.RANKCOLOR[rank],
            description=rank
        )
        if "avatar" in data:
            obj.set_thumbnail(url=data["avatar"])

        if "group" in data:
            if "name" in data["group"]:
                obj.add_field("Group", data["group"]["name"])

        fields = {
            "username": "Handle",
            "name": "Name",
            "score": "Total score",
            "solved": "Solved problems count",
            "rank": "Global rank",
            "ratio": "Solved problem ratio"
        }
        for field_key, field_name in fields.items():
            if field_key in data:
                if data[field_key] is float:
                    obj.add_field(field_name, f"{data[field_key]:.2f}")
                elif data[field_key] != "":
                    obj.add_field(field_name, data[field_key])

        return obj


def process_rank(ratio: float) -> str: # TODO
    '''Get rank from solved problem ratio'''
    return "Codefun-Newbie"


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
