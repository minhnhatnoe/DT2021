'''Module for fetching data from Codechef'''

import aiohttp
from bs4 import BeautifulSoup
class CCApi(Exception):
    "Base class for all exception raised from getting information from Codechef"

async def get_user_data(username: str) -> BeautifulSoup:
    '''Returns a soup'''
    request_url = f"https://codechef.com/users/{username}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as response:
                from_net = await response.text()
    except Exception as ex_type:
        raise CCApi(Exception("Network Error")) from ex_type

    soup = BeautifulSoup(from_net, features="html.parser")
    return soup

async def get_user_star(username: str):
    '''Return role name'''
    soup = await get_user_data(username)
    star = soup.select('span[class="rating"]')
    star_text = star[0].getText()

    star_text = star_text.replace('★', '*')
    return f"Codechef {star_text}"
