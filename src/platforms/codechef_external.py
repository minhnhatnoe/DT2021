'''Module for fetching data from Codechef'''

from typing import Dict, List
from bs4 import BeautifulSoup
import disnake
from src.utils import network
from src.platforms import platform_abs

class CodeChefApi(Exception):
    "Base class for all exception raised from getting information from Codechef"


class CodeChef(platform_abs.PlatForm):
    '''CodeChef-related tasks'''

    RANKCOLOR = {
        "Codechef 0*": 0x000000,
        "Codechef 1*": 0x000000,
        "Codechef 2*": 0x1E7D22,
        "Codechef 3*": 0x3366CC,
        "Codechef 4*": 0x684273,
        "Codechef 5*": 0xFFBF00,
        "Codechef 6*": 0xFF7F00,
        "Codechef 7*": 0xD0011B
    }

    PLATFORM_NAME = "Codechef"
    HANDLE_FILE_NAME = "/cchandle"

    async def generate_user_embed(self, handle: str, member: disnake.Member) -> disnake.Embed:
        '''Generate user disnake.Embed from Codechef data'''
        rank_text = await get_user_role_name(handle)
        obj = disnake.Embed(
            title=member.display_name,
            color=self.RANKCOLOR[rank_text],
            description=rank_text.title())

        obj.add_field("Handle", handle)
        return obj

    async def generate_dict_of_rank(self, user_list: List) -> Dict:
        '''Generate rank dict of user list'''
        result = {}
        for person in user_list:
            handle = person.lower()
            result[handle] = await get_user_role_name(handle)
        return result


def bs_soup_callable(from_net: str):
    '''BeautifulSoup Callable to use in get_net'''
    return BeautifulSoup(from_net, features="html.parser")


async def get_user_data_from_net(username: str) -> BeautifulSoup:
    '''Returns a soup'''
    request_url = f"https://codechef.com/users/{username}"
    try:
        from_net = await network.get_net(
            request_url, bs_soup_callable)
    except Exception as ex_type:
        raise CodeChefApi(Exception("Network Error")) from ex_type

    soup = bs_soup_callable(from_net)
    return soup


async def get_user_role_name(username: str) -> str:
    '''Return role name'''
    soup = await get_user_data_from_net(username)
    star = soup.select('span[class="rating"]')
    star_text = str()
    if len(star) == 0:
        star_text = "0*"
    else:
        star_text = star[0].getText()

    star_text = star_text.replace('★', '*')
    return f"Codechef {star_text}"
