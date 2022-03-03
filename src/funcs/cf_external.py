'''Codeforces API interaction'''
import json
from disnake import Embed
import aiohttp

RANKCOLOR = {
    "unrated": 0x000000,
    "newbie": 0xCCCCCC,
    "pupil": 0x77FF77,
    "specialist": 0x77DDBB,
    "expert": 0xAAAAFF,
    "candidate master": 0xFF88FF,
    "master": 0xFFCC88,
    "international master": 0xFFBB55,
    "grandmaster": 0xFF7777,
    "international grandmaster": 0xFF3333,
    "legendary grandmaster": 0xAA0000
}

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
        title=dischand, color=RANKCOLOR[data["rank"]], description=data["rank"].title())
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
