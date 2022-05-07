'''Codeforces API interaction'''
import asyncio
import json
import hashlib
import secrets
from typing import Dict, List
import disnake
from src.utils import network
from src.platforms import platform_abs

class CodeForces(platform_abs.PlatForm):
    '''CodeForces-related tasks'''

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

    PLATFORM_NAME = "Codeforces"
    HANDLE_FILE_NAME = "/cfhandle"

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
            new_name = await get_user_data_from_net([handle])
            try:
                new_name = new_name[0]["firstName"]
            except KeyError:
                continue
            if new_name == hash_val:
                return True
        return False

    async def generate_user_embed(self, handle: str, member: disnake.Member) -> disnake.Embed:
        '''Create an embed that represent a Codeforces user'''
        data = await get_user_data_from_net([handle])
        data = data[0]
        obj = disnake.Embed(
            title=member.name,
            color=self.RANKCOLOR[data["rank"]],
            description=f"{data['rank'].title()}")
        obj.set_thumbnail(url=data["titlePhoto"])

        if "firstName" in data and "lastName" in data:
            name = f'{data["firstName"]} {data["lastName"]}'
            if name != " ":
                obj.add_field("Name", name)

        fields = {
            "handle": "Handle",
            "country": "Country",
            "city": "City",
            "organization": "Organization",
            "rating": "Current Rating",
            "maxRank": "Max Rank",
            "maxRating": "Max Rating",
            "contribution": "Contribution",
            "friendOfCount": "Friends",
        }
        for field_key, field_name in fields.items():
            if field_key in data:
                if isinstance(data[field_key], float):
                    obj.add_field(field_name, f"{data[field_key]:.2f}")
                elif isinstance(data[field_key], str):
                    if data[field_key]!= "":
                        obj.add_field(field_name, data[field_key].title())
                else:
                    obj.add_field(field_name, data[field_key])

        if "registrationTimeSeconds" in data:
            obj.add_field("Registered", f"<t:{data['registrationTimeSeconds']}:R>")
        if "lastOnlineTimeSeconds" in data:
            obj.add_field("Last visit", f"<t:{data['lastOnlineTimeSeconds']}:R>")

        obj.add_field("Link", f"https://codeforces.com/profile/{handle}")
        return obj

    async def generate_dict_of_rank(self, user_list: List):
        '''Generate dict of rank from provided user list'''
        result = {}
        data = await get_user_data_from_net(user_list)
        for person in data:
            handle = person["handle"].lower()
            result[handle] = person["rank"]
        return result


class CodeForcesApi(Exception):
    "Base class for all exception raised from communicating with CF API"


async def get_user_data_from_net(user_list: List) -> Dict:
    '''Get user data of person(s) from CF'''
    if len(user_list) == 0:
        return {}
    request_url = f"https://codeforces.com/api/user.info?handles={';'.join(user_list)}"
    try:
        from_net = await network.get_net(request_url, json.loads, json.JSONDecodeError)
    except Exception as ex_type:
        raise CodeForcesApi(Exception("Network Error")) from ex_type

    json_data = json.loads(from_net)
    if json_data["status"] == "FAILED":
        raise CodeForcesApi(Exception(f"Handle Error: {user_list}"))

    data = json_data["result"]
    for person in data:
        if "rank" not in person:
            person["rank"] = "unrated"
    return data
