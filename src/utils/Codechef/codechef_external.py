'''Module for fetching data from Codechef'''

import aiohttp
from bs4 import BeautifulSoup
class CCApi(Exception):
    "Base class for all exception raised from getting information from Codechef"

class CodechefData:
    def __init__(self, username: str):
        self.data = self.get_user_data(username)

    async def get_user_data(self, username: str) -> BeautifulSoup:
        request_url = f"https://codechef.com/users/{username}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(request_url) as response:
                    from_net = await response.text()
        except Exception as ex_type:
            raise CCApi(Exception("Network Error")) from ex_type

        soup = BeautifulSoup(from_net, features="html.parser")
        return soup

    def get_user_star(self):
        star = self.data.select('span[class="rating"]')
        startext = star[0].getText()

        startext = startext.replace('★', '*')
        return startext
