import disnake
from disnake.ext import commands
import os  # TODO: Minimize footprint of os
from dotenv import load_dotenv
import json
import src.Codeforces.Funcs

class jsontask:
    def add_to_update(guildid: str, userid: str):
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\\update.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            if guildid not in json_data:
                json_data[guildid] = []
            json_data[guildid].append(userid)
            json.dump(json_data, json_file)
            json_file.truncate()

    def add_roles(guildid: str, rolelist: dict):
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data[guildid] = rolelist
            json.dump(json_data, json_file)
            json_file.truncate()

    def remove_guld(guildid: str):
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data.pop(str(guildid))
            json.dump(json_data, json_file)
            json_file.truncate()
        
        with open(f"{path}\\update.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data.pop(str(guildid))
            json.dump(json_data, json_file)
            json_file.truncate()

load_dotenv()
guilds = [int(v) for v in os.environ.get("TEST_GUILDS").split(", ")]
bot = commands.Bot(test_guilds=guilds)

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

@bot.slash_command()
async def ping(inter):
    '''/ping: Get the bot's latency'''
    await inter.response.send_message(f"Pong! ({inter.bot.latency * 1000:.0f}ms)")

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

@bot.slash_command()
async def updateme(inter, user: disnake.User):
    '''/updateme @<Discord>: Add someone to the handle update list'''
    jsontask.add_to_update(inter.guild.id, user.id)
    await inter.response.send_message(f"{user.mention} has been added to the update list")

# @bot.slash_command()
# async def refresh():
#     '''/refresh: Refresh all color-based roles'''
#     path = os.environ.get("DATAPATH")
#     with open(f"{path}\\update.json", "r") as json_file:
#         json_data = json.load(json_file)
#         for guildid in json_data:
#             guild = bot.get_guild(int(guildid))
#             for userid in json_data[guild]:
#                 user = guild.get_member(int(userid))
#                 rolename = src.Codeforces.Funcs.getRoles(user, guild)[0]
#                 guild.find_role() # TODO
#                 user.add_roles()
#     await bot.response.send_message("Refreshed all roles")

@bot.event
async def on_guild_join(guild):
    '''Add the bot to a guild'''
    rolelist = []
    for rank, color in rankcolor:
        role = await guild.create_role(name=rank, color=color)
        rolelist[rank] = role.id
    jsontask.add_guild(guild.id, rolelist)

@bot.event
async def on_guild_remove(guild):
    '''Remove the bot from a guild'''
    jsontask.remove_guild(guild.id)

@bot.event
async def on_ready():
    print("Logged in")

bot.load_extension("src.Codeforces.Commands")

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get("TOKEN"))