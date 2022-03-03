from src.imports import *
from src import Funcs
from src import keep_alive
load_dotenv()
guilds = [int(v) for v in environ.get("TEST_GUILDS").split(",")]
bot = commands.Bot(test_guilds=guilds, intents=disnake.Intents.all())


@tasks.loop(minutes=30)
async def refresh_all_roles():
    await Funcs.GuildFuncs.refresh_roles(bot=bot)
    print("Refreshed all guilds on: ", datetime.now())


@bot.event
async def on_guild_join(guild):
    '''Add the bot to a guild'''
    await Funcs.GuildFuncs.make_roles(guild)
  

@bot.event
async def on_guild_remove(guild: disnake.Guild):
    '''Remove the bot from a guild'''
    Funcs.GuildFuncs.remove_guild(guild.id)


@bot.event
async def on_ready():
    print("Logged in")
    if not refresh_all_roles.is_running():
        refresh_all_roles.start()


@bot.slash_command()
async def helpme(inter):
    '''/helpme: Show this help message'''
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

bot.load_extension("src.Codeforces")
bot.load_extension("src.General")

if __name__ == "__main__":
    load_dotenv()
    keep_alive.keep_alive()
    bot.run(environ.get("TOKEN"))
