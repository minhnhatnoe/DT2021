import disnake
from disnake.ext import commands


class presence:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def presence_change(self, state: str):
        game = disnake.Game(state)
        await self.bot.change_presence(status=disnake.Status.idle, activity=game)

    async def __aenter__(self):
        return self

    async def __aexit__(self, ex_type, value, traceback):
        await self.presence_change("Normal as always")
        return ex_type is None
