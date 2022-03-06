'''Module for fetching data from Codechef'''

import requests
from bs4 import BeautifulSoup

class CodechefData:
    def __init__(self, username: str):
        self.data = self.get_user_data(username)

    def get_user_data(self, username: str) -> BeautifulSoup:
        request_url = f"https://codechef.com/users/{username}"
        request = requests.get(request_url)

        soup = BeautifulSoup(request.text, features = "html.parser")
        return soup

    def get_user_star(self):
        star = self.data.select('span[class="rating"]')
        startext = star[0].getText()

        startext = startext.replace('★', '*')
        return startext