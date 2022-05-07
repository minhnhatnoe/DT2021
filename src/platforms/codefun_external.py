'''Codefun API Interaction'''
import json
from typing import Dict
import disnake
from src.utils import network
from src.platforms import platform_abs

class CodeFunApi(Exception):
    '''Base class for all exceptions from Codefun'''
    class NotFound(Exception):
        '''Class if not found'''


class CodeFun(platform_abs.PlatForm):
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

    async def generate_user_embed(self, handle: str, member: disnake.Member) -> disnake.Embed:
        '''Generate user embed from server data'''
        data = await get_user_data_from_net(handle)
        rank = process_rank(data["ratio"])
        obj = disnake.Embed(
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
        }
        for field_key, field_name in fields.items():
            if field_key in data:
                if isinstance(data[field_key], float):
                    obj.add_field(field_name, f"{data[field_key]:.2f}")
                elif data[field_key] != "":
                    obj.add_field(field_name, data[field_key])

        obj.add_field("Solved in pool", f"{data['ratio']:.0%}")
        return obj

    async def generate_dict_of_rank(self, user_list) -> Dict:
        '''Generate a rank dict from a list of usernames'''
        result = {}
        for person in user_list:
            handle = person.lower()
            data = await get_user_data_from_net(handle)
            result[handle] = process_rank(data["ratio"])
        return result

RANKLIST = {
    0.9: "Grandmaster",
    0.55: "Hacker",
    0.3755: "Master",
    0.25: "Expert",
    0.1: "Coder",
    0.05: "Novice",
    0.02: "Beginner",
    0: "Newbie"
}
def process_rank(ratio: float) -> str:
    '''Get rank from solved problem ratio'''
    for point, name in RANKLIST.items():
        if ratio >= point:
            return f"Codefun-{name}"
    raise Exception("Invalid rank")

async def get_user_data_from_net(user: str) -> Dict:
    '''Get a person data from Codefun'''
    request_url = f"https://codefun.vn/api/users/{user}"
    try:
        from_net = await network.get_net(request_url, json.loads, json.JSONDecodeError)
    except Exception as ex_type:
        if str(ex_type) == "Not Found":
            raise CodeFunApi.NotFound(
                Exception("Provided handle not found")) from ex_type
        raise CodeFunApi(Exception("Error")) from ex_type

    json_data = json.loads(from_net)
    if "error" in json_data:
        raise CodeFunApi(Exception(json_data["error"]))
    return json_data["data"]
