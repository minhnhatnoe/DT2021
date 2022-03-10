'''Codeforces API interaction'''
import json
import disnake
from disnake import Embed
import aiohttp
from src.utils.constants import *

class CFApi(Exception):
    "Base class for all exception raised from communicating with CF API"


async def get_user_data(user_list):
    '''Get user data of person(s) from CF'''
    request_url = f"https://codeforces.com/api/user.info?handles={';'.join(user_list)}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as response:
                from_net = await response.text()
    except Exception as ex_type:
        raise CFApi(Exception("Network Error")) from ex_type

    json_data = json.loads(from_net)

    if json_data["status"] == "FAILED":
        raise CFApi(Exception("Handle Error"))
    return json_data["result"]


async def generate_dict_of_rank(user_list):
    '''Generate a dict of handle-rank from CF, accepting dict of str only'''
    data = await get_user_data(user_list)
    result = dict()
    for person in data:
        if "rank" not in person:
            person["rank"] = "unrated"
        result[person["handle"].lower()] = person["rank"]
    return result


async def generate_user_embed(handle: str, member: disnake.Member):
    '''Create an embed that represent a user'''
    data = await get_user_data([handle])
    data = data[0]
    if "rank" not in data:
        data["rank"] = "unrated"
    obj = Embed(
        title=member.display_name, color=RANKCOLOR[data["rank"]], description=data["rank"].title())
    obj.set_thumbnail(url=data["titlePhoto"])
    if "firstName" in data and "lastName" in data:
        if data["firstName"] != "" and data["lastName"] != "":
            obj.add_field(
                "Name", data["firstName"] + " " + data["lastName"])

    fields = ["handle", "country", "city", "organization", "rating"]
    for field in fields:
        if field in data:
            if data[field] != "":
                obj.add_field(field.title(), data[field])
    return obj
