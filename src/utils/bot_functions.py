'''Bot object functions'''
import disnake
from disnake.ext import commands
from src import cfg

class Presence:
    '''Presence change'''

    def __init__(self):
        '''Write bot var'''
        self.state: str

    async def presence_change(self, state: str) -> None:
        '''Change shown presence of bot'''
        self.state = state
        game = disnake.Game(state)
        if cfg.bot is commands.Bot:
            await cfg.bot.change_presence(status=disnake.Status.idle, activity=game)

    async def __aenter__(self):
        '''Return self for with statements'''
        return self

    async def __aexit__(self, ex_type, value, traceback) -> bool:
        '''Switch back to default presence'''
        await self.presence_change("Normal as always")
        return ex_type is None
