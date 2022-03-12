'''Master Bot code'''
from os import environ
from datetime import datetime
from dotenv import load_dotenv
import disnake
from disnake.ext import commands, tasks
from src import keep_alive
from src.utils import guild_funcs

load_dotenv()
guilds = [int(v) for v in environ.get("TEST_GUILDS").split(",")]
bot = commands.Bot(test_guilds=guilds, intents=disnake.Intents.all())

@tasks.loop(minutes=environ.get("REFRESH_RATE"))
async def refresh_all_roles():
    '''Refresh all roles, periodically'''
    await guild_funcs.refresh_roles(bot=bot)
    print("Refreshed all guilds on: ", datetime.now())


@bot.event
async def on_guild_join(guild: disnake.Guild):
    '''Add the bot to a guild'''
    await guild_funcs.create_roles(guild)


@bot.event
async def on_guild_remove(guild: disnake.Guild):
    '''Remove the bot from a guild'''
    guild_funcs.remove_guild(guild.id)


@bot.event
async def on_ready():
    '''Notify the user that the bot has logged in and start to periodically refresh roles'''
    print("Logged in")
    if not refresh_all_roles.is_running():
        refresh_all_roles.start()


@bot.slash_command(name='help')
async def help_cmd(inter: disnake.CommandInteraction):
    '''/help: Show this help message'''
    msg = 'Here are several things I can do:'

    command_set = bot.get_guild_slash_commands(inter.guild.id)
    help_msg = []
    for cmd in command_set:
        if cmd.options:
            for opt in cmd.options:
                help_msg.append(opt.description)
        else:
            help_msg.append(cmd.description)

    await inter.response.send_message(msg + "```" + "\n".join(help_msg) + "```")


bot.load_extension("src.general_cmd")
bot.load_extension("src.codeforces_cmd")
bot.load_extension("src.codechef_cmd")

if __name__ == "__main__":
    load_dotenv()
    # keep_alive.keep_alive()
    bot.run(environ.get("TOKEN"))
