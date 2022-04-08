from abc import ABC
from typing import Dict
import disnake
from disnake.ext import commands


class PlatForm(ABC):
    '''Abstract base class for a platform'''
    RANKCOLOR = {}
    PLATFORM_NAME = "Nothing"
    HANDLE_FILE_NAME = "/abc"

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def verify(self, member: disnake.Member, handle: str) -> bool:  # pylint: disable=no-self-use, unused argument
        '''Default verification procedure (returns True)'''
        return True

    async def generate_user_embed(self, handle: str, member: disnake.Member) -> disnake.Embed:
        '''Generates a blank embed''' # TODO
        return disnake.Embed()
    
    async def generate_dict_of_rank(self, user_list) -> Dict:
        '''Generate blank dict'''
        return {}
    