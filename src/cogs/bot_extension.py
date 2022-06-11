'''Events and tasks to be run by the bot'''
from os import environ
from dotenv import load_dotenv
import disnake
from disnake.ext import commands, tasks
from src import cfg
from src.utils import guild_functions, refresh_procedure

load_dotenv()
refresh_rate = float(environ.get("REFRESH_RATE"))


class BotExtension(commands.Cog):
    '''Tasks and listeners'''

    def __init__(self) -> None:
        '''Init the cog'''

    @tasks.loop(minutes=refresh_rate)
    async def refresh_role_loop(self):  # pylint: disable=no-self-use
        '''Refresh all roles, periodically'''
        await refresh_procedure.refresh_roles_of_bot()

    @commands.slash_command(name="help")
    async def help_cmd(self, inter: disnake.CommandInteraction):  # pylint: disable=no-self-use
        '''/help: Show this help message'''
        msg = 'Here are several things I can do:'

        command_set = cfg.bot.get_guild_slash_commands(inter.guild.id)
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
        print(f"Logged in as {cfg.bot.user.name}#{cfg.bot.user.discriminator}, with ping {cfg.bot.latency * 1000:.0f}ms")
        if not self.refresh_role_loop.is_running():  # pylint: disable=no-member
            self.refresh_role_loop.start()  # pylint: disable=no-member

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):  # pylint: disable=no-self-use
        '''Add the bot to a guild'''
        await guild_functions.create_roles_in_guild(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: disnake.Guild):  # pylint: disable=no-self-use
        '''Remove the bot from a guild'''
        guild_functions.remove_guild_data(guild.id)

    @commands.slash_command()
    async def ping(self, inter: disnake.CommandInteraction):  # pylint: disable=no-self-use
        '''/ping: Get the bot's latency'''
        await inter.response.send_message(f"Pong! ({cfg.bot.latency * 1000:.0f}ms)")


def setup(bot: commands.Bot):
    '''Add bot listeners and help cmd'''
    bot.add_cog(BotExtension())
