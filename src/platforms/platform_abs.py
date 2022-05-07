'''Abstract class for platform'''
from abc import ABC
from typing import Dict
import disnake
from src import cfg
class PlatForm(ABC):
    '''Abstract base class for a platform'''
    RANKCOLOR = {}
    PLATFORM_NAME = "Nothing"
    HANDLE_FILE_NAME = "/abc"

    def __init__(self) -> None:
        self.bot = cfg.bot

    async def verify(self, member: disnake.Member, handle: str) -> bool:  # pylint: disable=no-self-use,unused-argument
        '''Default verification procedure (returns True)'''
        return True

    async def generate_user_embed(self, handle: str, member: disnake.Member) -> disnake.Embed:  # pylint: disable=no-self-use,unused-argument
        '''Generates a blank embed'''
        return disnake.Embed()

    async def generate_dict_of_rank(self, user_list) -> Dict: # pylint: disable=no-self-use,unused-argument
        '''Generate blank dict'''
        return {}
