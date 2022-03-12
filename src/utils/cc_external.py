'''Module for fetching data from Codechef'''

from bs4 import BeautifulSoup
from disnake.ext import commands
from src.utils import network


class CCApi(Exception):
    "Base class for all exception raised from getting information from Codechef"


def bs_soup_callable(from_net: str):
    '''BeautifulSoup Callable to use in get_net'''
    return BeautifulSoup(from_net, features="html.parser")


async def get_user_data(bot: commands.Bot, username: str) -> BeautifulSoup:
    '''Returns a soup'''
    request_url = f"https://codechef.com/users/{username}"
    try:
        from_net = await network.get_net(
            bot, request_url, bs_soup_callable, [])

    except Exception as ex_type:
        raise CCApi(Exception("Network Error")) from ex_type
    soup = bs_soup_callable(from_net)
    return soup


async def get_user_star(bot: commands.Bot, username: str) -> str:
    '''Return role name'''
    soup = await get_user_data(bot, username)
    star = soup.select('span[class="rating"]')
    star_text = str()
    if len(star) == 0:
        star_text = "0*"
    else:
        star_text = star[0].getText()

    star_text = star_text.replace('★', '*')
    return f"Codechef {star_text}"
