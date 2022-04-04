'''Events and tasks to be run by the bot'''
from os import environ
from datetime import datetime
from dotenv import load_dotenv
import disnake
from disnake.ext import commands, tasks
from src.utils import guild_funcs

load_dotenv()
refresh_rate = float(environ.get("REFRESH_RATE"))


class BotExtension(commands.Cog):  # TODO: turn to cog
    '''Tasks and listeners'''

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @tasks.loop(minutes=refresh_rate)
    async def refresh_role_loop(self):
        '''Refresh all roles, periodically'''
        await guild_funcs.refresh_roles_of_bot(bot=self.bot)
        print("Refreshed all guilds on: ", datetime.now())

    @commands.slash_command(name="help")
    async def help_cmd(self, inter: disnake.CommandInteraction):
        '''/help: Show this help message'''
        msg = 'Here are several things I can do:'

        command_set = self.bot.get_guild_slash_commands(inter.guild.id)
        help_msg = []
        for cmd in command_set:
            if cmd.options:
                for opt in cmd.options:
                    help_msg.append(opt.description)
            else:
                help_msg.append(cmd.description)

        await inter.response.send_message(msg + "```" + "\n".join(help_msg) + "```")

    @commands.Cog.listener()
    async def on_ready(self):
        '''Notify the user that the bot has logged in and start to periodically refresh roles'''
        print("Logged in")
        if not self.refresh_role_loop.is_running():  # pylint: disable=no-member
            self.refresh_role_loop.start()  # pylint: disable=no-member

    @commands.Cog.listener()
    async def on_guild_join(guild: disnake.Guild):
        '''Add the bot to a guild'''
        await guild_funcs.create_roles_in_guild(guild)

    @commands.Cog.listener()
    async def on_guild_remove(guild: disnake.Guild):
        '''Remove the bot from a guild'''
        guild_funcs.remove_guild_data(guild.id)

    @commands.slash_command()
    async def ping(self, inter: disnake.CommandInteraction):  # pylint: disable=no-self-use
        '''/gen ping: Get the bot's latency'''
        await inter.response.send_message(f"Pong! ({inter.bot.latency * 1000:.0f}ms)")


def setup(bot: commands.Bot):
    '''Add bot listeners and help cmd'''
    bot.add_cog(BotExtension(bot))
