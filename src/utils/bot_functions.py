'''Bot object functions'''
import disnake
from disnake.ext import commands


class Presence:
    '''Presence change'''

    def __init__(self, bot: commands.Bot):
        '''Write bot var'''
        self.bot = bot

    async def presence_change(self, state: str) -> None:
        '''Change shown presence of bot'''
        game = disnake.Game(state)
        if self.bot is commands.Bot:
            await self.bot.change_presence(status=disnake.Status.idle, activity=game)

    async def __aenter__(self):
        '''Return self for with statements'''
        return self

    async def __aexit__(self, ex_type, value, traceback) -> bool:
        '''Switch back to default presence'''
        await self.presence_change("Normal as always")
        return ex_type is None
