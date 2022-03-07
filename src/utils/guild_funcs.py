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
    # A set of role-handle pairs
    process_list = {0: {}, 1: {}, 2: {}}

    for guild_id, users in task_list.items():
        guild = bot.get_guild(int(guild_id)) # TODO: Handle guild deleted

        for user_id, user_choice in task_list[guild_id].items():
            user = guild.get_member(int(user_id))
            if user is None:
                print(f"{user_id} in {guild_id} not found")
                continue
            process_list[user_choice][user] = None

    # TODO: Process handles, then get role from rank

def get_task_list():
    '''Get the total update list'''
    json_data = json_file.load_from_json("update")

async def get_roles(guild: disnake.Guild) -> dict:
    '''Get role ids of a guild (find or create role if not in record)
    Returns a dict of role.name-role.id pairs'''
    json_data = json_file.load_from_json("role")
    key = str(guild.id)
    if key not in json_data:
        json_data[key] = {}
    
    for role_name, color in reversed(list(RANKCOLOR.items())):
        online_guild_role_list = dict(
            [(role.name, role) for role in guild.roles])

        if role_name not in json_data[key]:
            if role_name not in online_guild_role_list:
                role = await guild.create_role(name=role_name, color=color, hoist=True)
                json_data[key][role_name] = role.id
            else:
                json_data[key][role_name] = online_guild_role_list[role_name].id
    
    json_file.write_to_json("role", json_data)


def remove_guild(guild_id: str):
    '''Delete data abt a guild'''
    json_data = json_file.load_from_json("role")
    if str(guild_id) in json_data:
        json_data.pop(str(guild_id))
    json_file.write_to_json("role", json_data)
