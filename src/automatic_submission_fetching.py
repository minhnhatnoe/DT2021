'''Module for automatically fetching new submissions from a contest'''

import disnake
from disnake.ext import commands, tasks

class SubmissionFetching(commands.Cog):
    '''Cog for fetching submissions'''

    def __init__(self, bot):
        '''Initialization'''
        self.bot = bot
        self.destination_channel = None
        self.contest_id = None

    @commands.slash_command(name = "fetch")
    async def setup(self, inter, contest_id: int) -> None:
        self.contest_id = int(contest_id)
        self.destination_channel = inter.channel
        self.fetch.start()
        await inter.response.send_message(f"Setup to fetch submission from contest with ID: {contest_id} (Not functioning yet)")

    @tasks.loop(seconds = 10.0)
    async def fetch(self):
        print(f"Fetching submissions for contest ID = {self.contest_id}")
        await self.destination_channel.send(content = "Testing...")

def setup(bot: commands.Bot):
    '''Add the cog to the bot'''
    bot.add_cog(SubmissionFetching(bot))