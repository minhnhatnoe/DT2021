from src.imports import *
from src import Funcs
load_dotenv()
guilds = [int(v) for v in environ.get("TEST_GUILDS").split(",")]
bot = commands.Bot(test_guilds=guilds, intents = disnake.Intents.all())

@bot.event
async def on_guild_join(guild):
    '''Add the bot to a guild'''
    await Funcs.GuildFuncs.make_role(guild)

@bot.event
async def on_guild_remove(guild: disnake.Guild):
    '''Remove the bot from a guild'''
    guildroles = Funcs.GuildFuncs.get_roles(guild.id)
    if guildroles is None: return
    for rolename, roleid in guildroles.items():
        role = await guild.get_role(int(roleid))
        await role.delete()
    Funcs.GuildFuncs.remove_guild(guild.id)

@bot.event
async def on_ready():
    print("Logged in")

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
    bot.run(environ.get("TOKEN"))