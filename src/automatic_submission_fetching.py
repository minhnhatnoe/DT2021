'''Module for automatically fetching new submissions from a contest'''

import disnake
from disnake.ext import commands, tasks

class SubmissionFetching:
    '''A class for fetching submissions'''

    def __init__(self, bot, channel, id):
        '''Initialization'''
        self.bot = bot
        self.destination_channel = channel
        self.contest_id = id

    def set_active_range(self, start_time: int, end_time: int) -> None:
        pass

    @tasks.loop()
    async def begin_loop(self) -> None:
        self.fetch.start()

    @tasks.loop()
    async def end_loop(self) -> None:
        self.fetch.stop()

    @tasks.loop(seconds = 15.0)
    async def fetch(self) -> None:
        print(f"Fetching submissions for contest ID = {self.contest_id}")
        await self.destination_channel.send(content = "Testing...")

class SubmissionFetchingCog(commands.Cog):
    '''A cog for creating SubmissionFetching instance'''

    def __init__(self, bot):
        '''Initialization'''
        self.bot = bot

    @commands.slash_command(name = "fetch")
    async def setup(self, inter, contest_id: int) -> None:
        '''Setup an instance of SubmissionFetching for fetching'''
        fetch_module = SubmissionFetching(self.bot, inter.channel, int(contest_id))
        # TODO: Set start_time and end_time, handle: (before contest, in contest, after contest)
        await inter.response.send_message(f"Setup to fetch submission from contest with ID: {contest_id} (Not functioning yet)")

def setup(bot: commands.Bot):
    '''Add the cog to the bot'''
    bot.add_cog(SubmissionFetchingCog(bot))