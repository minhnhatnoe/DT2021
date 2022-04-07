'''Codeforces API interaction'''
import asyncio
import json
import hashlib
import secrets
from typing import Dict, List
import disnake
from disnake import Embed
from disnake.ext import commands
from src.utils.constants import RANKCOLOR
from src.utils import network


class CFApi(Exception):
    "Base class for all exception raised from communicating with CF API"


async def get_user_data_from_net(bot: commands.Bot, user_list: List) -> Dict:
    '''Get user data of person(s) from CF'''
    request_url = f"https://codeforces.com/api/user.info?handles={';'.join(user_list)}"
    try:
        from_net = await network.get_net(bot, request_url, json.loads, json.JSONDecodeError)
    except Exception as ex_type:
        raise CFApi(Exception("Network Error")) from ex_type

    json_data = json.loads(from_net)
    if json_data["status"] == "FAILED":
        raise CFApi(Exception("Handle Error"))

    data = json_data["result"]
    for person in data:
        if "rank" not in person:
            person["rank"] = "unrated"
    return data


async def generate_user_embed(bot: commands.Bot, handle: str, member: disnake.Member) -> Embed:
    '''Create an embed that represent a Codeforces user'''
    data = await get_user_data_from_net(bot, [handle])
    data = data[0]
    obj = Embed(
        title=member.display_name,
        color=RANKCOLOR[data["rank"]],
        description=data["rank"].title())

    obj.set_thumbnail(url=data["titlePhoto"])

    if "firstName" in data and "lastName" in data:
        name = f'{data["firstName"]} {data["lastName"]}'
        if name != " ":
            obj.add_field("Name", name)

    fields = ["handle", "country", "city", "organization", "rating"]
    for field in fields:
        if field in data:
            if data[field] != "":
                obj.add_field(field.title(), data[field])
    return obj


class CodeForces:
    '''CodeForces-related tasks'''
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def verify(self, member: disnake.Member, handle: str) -> bool:
        '''Perform verification process, assuming handle exist'''
        salt = secrets.token_bytes(16)
        hash_str = f"{salt}{member.id}-dt2021-verify".encode("utf-8")
        hash_val = hashlib.md5(hash_str).hexdigest()
        await member.send(
            f"Temporarily change your First name (English) to \
    {hash_val} in https://codeforces.com/settings/social within the next minute")
        for _ in range(7):
            await asyncio.sleep(10)
            new_name = await get_user_data_from_net(self.bot, [handle])
            try:
                new_name = new_name[0]["firstName"]
            except KeyError:
                continue
            if new_name == hash_val:
                return True
        return False
