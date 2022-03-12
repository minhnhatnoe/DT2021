from os import environ
from datetime import datetime
from dotenv import load_dotenv
import disnake
from disnake.ext import commands, tasks
from src.utils import guild_funcs

load_dotenv()
refresh_rate = float(environ.get("REFRESH_RATE"))


class BotExtension:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @tasks.loop(minutes=refresh_rate)
    async def refresh_all_roles(self):
        '''Refresh all roles, periodically'''
        await guild_funcs.refresh_roles(bot=self.bot)
        print("Refreshed all guilds on: ", datetime.now())

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

    async def on_ready(self):
        '''Notify the user that the bot has logged in and start to periodically refresh roles'''
        print("Logged in")
        if not self.refresh_all_roles.is_running():
            self.refresh_all_roles.start()

    async def on_guild_join(self, guild: disnake.Guild):
        '''Add the bot to a guild'''
        await guild_funcs.create_roles(guild)


    async def on_guild_remove(self, guild: disnake.Guild):
        '''Remove the bot from a guild'''
        guild_funcs.remove_guild(guild.id)


def setup(bot: commands.Bot):
    '''Add the "cf" cog'''
    instance = BotExtension(bot)
    bot.event(instance.on_ready)
    bot.event(instance.on_guild_join)
    bot.event(instance.on_guild_remove)
    bot.slash_command(name="help")(instance.help_cmd)
