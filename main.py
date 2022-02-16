import disnake
from disnake.ext import commands
import os  # TODO: Minimize footprint of os
from dotenv import load_dotenv
import json
import src.Codeforces.Funcs

class jsontask:
    def add_to_update(guildid: str, userid: str):
        guildid = str(guildid)
        userid = str(userid)

        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\\update.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            if guildid not in json_data:
                json_data[str(guildid)] = []
            json_data[guildid].append(userid)
            json.dump(json_data, json_file)
            json_file.truncate()
    
    def get_update_list():
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\\update.json", "r") as json_file:
            json_data = json.load(json_file)
            return json_data

    def add_roles(guildid: str, rolelist: dict):
        guildid = str(guildid)
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data[guildid] = rolelist
            json.dump(json_data, json_file)
            json_file.truncate()

    def get_roles(guildid: str):
        guildid = str(guildid)
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r") as json_file:
            json_data = json.load(json_file)
            if guildid in json_data:
                return json_data[guildid]
            else:
                return None

    def remove_guild(guildid: str):
        guildid = str(guildid)
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            if str(guildid) in json_data: json_data.pop(str(guildid))
            json.dump(json_data, json_file)
            json_file.truncate()
        
        with open(f"{path}\\update.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            if str(guildid) in json_data: json_data.pop(str(guildid))
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

@bot.slash_command()
async def refresh(inter):
    '''/refresh: Refresh all color-based roles'''
    tasklist = jsontask.get_update_list()
    for guildid in tasklist:
        rolelist = jsontask.get_roles(guildid)
        guild = bot.get_guild(guildid)
        if guild is None:
            print(f"{guildid} cannot be updated")
            continue
        if rolelist is None:
            # TODO: Add relevant roles 
            pass
        for userid in tasklist[guildid]:
            user = guild.get_member(userid)
            if user is None:
                continue
            for role in user.roles:
                if role.id in rolelist:
                    await user.remove_role(role)
            rankname = src.Codeforces.Funcs.getRoles([userid])[0]
            rolefromrank = guild.get_role(rolelist[rankname])
            await user.add_roles(rolefromrank)
    await inter.response.send_message("All roles refreshed")

@bot.event
async def on_guild_join(guild):
    '''Add the bot to a guild'''
    rolelist = {}
    for rank, color in rankcolor.items():
        role = await guild.create_role(name=rank, color=color)
        rolelist[rank] = role.id
    jsontask.add_roles(guild.id, rolelist)

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