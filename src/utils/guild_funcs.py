'''All functions regarding a guild'''
import json
from os import environ
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
from src.utils.Codeforces import cf_internal
from src.utils.Codeforces import cf_external
from src.utils import json_file

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

async def refresh_roles(bot: commands.Bot):
    '''Refresh all roles in a guild. Provide either guildlist or bot'''
    task_list = get_task_list()
    process_list = {0: {}, 1: {}, 2: {}}

    for guild_id, users in task_list.items():
        guild = bot.get_guild(int(guild_id)) # TODO: Handle guild deleted
        guild_role = get_roles(guild)

        for user_id, user_choice in task_list[guild_id].items():
            user = guild.get_member(int(user_id))
            if user is None:
                print(f"{user_id} in {guild_id} not found")
                continue

            process_list[user_choice][user] = None # Then process handles
    


def get_task_list():
    '''Get the total update list'''
    json_data = json_file.load_from_json("update")

async def get_roles(guild: disnake.Guild):
    '''Get role ids of a guild'''
    json_data = json_file.load_from_json("role")
    key = str(guild.id)
    if key not in json_data:
        json_data[key] = {}
    
    for role_name, color in reversed(list(RANKCOLOR.items())):
        if role_name not in json_data[key]:
            role = await guild.create_role(name=role_name, color=color, hoist=True)
            json_data[key][role_name] = role.id
    
    json_file.write_to_json("role", json_data)


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
