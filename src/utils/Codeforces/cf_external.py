'''Codeforces API interaction'''
import json
from disnake import Embed
import aiohttp
import src.utils.guild_funcs
class CFApi(Exception):
    "Base class for all exception raised from communicating with CF API"


async def get_user_data(userlist):
    '''Get user data abt someone from CF'''
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://codeforces.com/api/user.info?handles={';'.join(userlist)}"
            ) as response:
                fromnet = await response.text()
    except Exception as ex_type:
        raise CFApi(Exception("Network Error")) from ex_type

    json_data = json.loads(fromnet)
    if json_data["status"] == "FAILED":
        raise CFApi(Exception("Handle Error"))
    return json_data["result"]


async def get_roles(userlist):
    '''Get role of someone based on their CF ranking'''
    data = await get_user_data(userlist)
    ranklist = []
    for user in data:
        if "rank" in user:
            ranklist.append(user["rank"])
        else:
            ranklist.append("unrated")
    return ranklist


async def get_user_embed(handle: str, dischand: str):
    '''Create an embed that represent a user'''
    data = await get_user_data([handle])
    data = data[0]
    if "rank" not in data:
        data["rank"] = "unrated"
    obj = Embed(
        title=dischand, color=src.utils.guild_funcs.RANKCOLOR[data["rank"]], description=data["rank"].title())
    obj.set_thumbnail(url=data["titlePhoto"])
    if "firstName" in data and "lastName" in data:
        if data["firstName"] != "" and data["lastName"] != "":
            obj.add_field(
                "Name", data["firstName"] + " " + data["lastName"])

    fields = [
        "handle",
        "country",
        "city",
        "organization",
        "rating"
    ]
    for field in fields:
        if field in data:
            if data[field] != "":
                obj.add_field(field.title(), data[field])
    return obj
