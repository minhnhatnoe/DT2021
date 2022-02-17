import disnake
from disnake.ext import commands
import os  # TODO: Minimize footprint of os
from dotenv import load_dotenv
import json
import src.Codeforces.Funcs
import src.Codeforces.Commands
from src.jsontask import jsontask

load_dotenv()
guilds = [int(v) for v in os.environ.get("TEST_GUILDS").split(",")]
print (guilds)
bot = commands.Bot(test_guilds=guilds, intents = disnake.Intents.all())
rankcolor = {
    "newbie": 0xCCCCCC,
    "pupil": 0x77FF77,
    "specialist": 0x77DDBB,
    "expert": 0xAAAAFF,
    "candidate master": 0xFF88FF,
    "master": 0xFFCC88,
    "international master": 0xFFBB55,
    "grandmaster": 0xFF7777,
    "international grandmaster": 0xFF3333,
    "legendary grandmaster": 0xAA0000
}

@bot.event
async def on_guild_join(guild):
    '''Add the bot to a guild'''
    rolelist = {}
    for rank, color in rankcolor.items():
        role = await guild.create_role(name=rank, color=color, hoist = True)
        rolelist[rank] = role.id
    jsontask.add_roles(guild.id, rolelist)

@bot.event
async def on_guild_remove(guild: disnake.Guild):
    '''Remove the bot from a guild'''
    guildroles = jsontask.get_roles(guild.id)
    if guildroles is None: return
    for rolename, roleid in guildroles.items():
        role = guild.get_role(int(roleid))
        await role.delete()
    jsontask.remove_guild(guild.id)

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

bot.load_extension("src.Codeforces.Commands")
bot.load_extension("src.sus")
if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get("TOKEN"))