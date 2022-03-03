'''All functions regarding a guild'''
from os import environ
import json
from dotenv import load_dotenv
from disnake.ext import commands
from src.funcs import CFInternal, CFExternal

RANKCOLOR = {
    "unrated": 0x000000,
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


async def refresh_roles(guildlist=None, bot: commands.bot = None):
    '''Refresh all roles in a guild. Provide either guildlist or bot'''
    if guildlist is None:
        guildlist = [bot.get_guild(int(guildid))
                     for guildid in get_guild_list()]

    for guild in guildlist:
        guildid = guild.id
        tasklist = get_update_list(guildid)

        rolelist = get_roles(guildid)
        if rolelist is None:
            print(f"No rolelist found in {guildid}")
            await make_roles(guild)
            rolelist = get_roles(guildid)

        cfquery = {}
        for userid in tasklist:
            user = guild.get_member(int(userid))
            if user is None:
                print(f"{userid} in {guildid} not found")
                continue

            for role in user.roles:
                if role.id in rolelist.values():
                    await user.remove_roles(role)

            handle = CFInternal.get_handle(userid)
            if handle is not None:
                cfquery[handle] = user

        if len(cfquery) != 0:
            ranks = await CFExternal.get_roles(cfquery.keys())
            for (handle, user), rankname in zip(cfquery.items(), ranks):
                rolefromrank = guild.get_role(rolelist[rankname])
                await user.add_roles(rolefromrank)


async def make_roles(guild):
    '''Add roles to a guild, also adding them to the database'''
    rolelist = {}
    for rank, color in reversed(list(RANKCOLOR.items())):
        role = await guild.create_role(name=rank, color=color, hoist=True)
        rolelist[rank] = role.id
    add_roles(guild.id, rolelist)


def get_update_list(guildid: str):
    '''Get user update list in a guild'''
    guildid = str(guildid)
    load_dotenv()
    path = environ.get("DATAPATH")
    with open(f"{path}/update.json", "r+") as json_file:
        json_data = json.load(json_file)
        json_file.seek(0)
        if guildid not in json_data:
            json_data[guildid] = {}
            json.dump(json_data, json_file)
            json_file.truncate()

        retval = []
        for key, value in json_data[guildid].items():
            if value:
                retval.append(key)
        return retval


def get_guild_list():
    '''Get the guild update list'''
    load_dotenv()
    path = environ.get("DATAPATH")
    with open(f"{path}/update.json", "r") as json_file:
        json_data = json.load(json_file)
        return json_data.keys()


def add_roles(guildid: str, rolelist: dict):
    '''Record role ids of a guild'''
    guildid = str(guildid)
    load_dotenv()
    path = environ.get("DATAPATH")
    with open(f"{path}/role.json", "r+") as json_file:
        json_data = json.load(json_file)
        json_file.seek(0)
        json_data[guildid] = rolelist
        json.dump(json_data, json_file)
        json_file.truncate()


def get_roles(guildid: str):
    '''Get role ids of a guild'''
    guildid = str(guildid)
    load_dotenv()
    path = environ.get("DATAPATH")
    with open(f"{path}/role.json", "r") as json_file:
        json_data = json.load(json_file)
        if guildid in json_data:
            return json_data[guildid]
        else:
            return None


def remove_guild(guildid: str):
    '''Delete data abt a guild'''
    guildid = str(guildid)
    load_dotenv()
    path = environ.get("DATAPATH")
    with open(f"{path}/role.json", "r+") as json_file:
        json_data = json.load(json_file)
        json_file.seek(0)
        if str(guildid) in json_data:
            json_data.pop(str(guildid))
        json.dump(json_data, json_file)
        json_file.truncate()
