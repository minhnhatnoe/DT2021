'''All functions regarding a guild'''
import json
import disnake
from disnake.ext import commands
from disnake.utils import get
from src.utils import json_file
from src.utils.Codeforces import cf_external
from src.utils.Codechef import cc_external
from src.utils.user_funcs import write_handle
RANKCOLOR = {
    "Codechef 1*": 0x000000,
    "Codechef 2*": 0x000000,
    "Codechef 3*": 0x000000,
    "Codechef 4*": 0x000000,
    "Codechef 5*": 0x000000,
    "Codechef 6*": 0x000000,
    "Codechef 7*": 0x000000,
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
    # Some sets of disnake.user - guild/handle/role pairs
    change_queries = {0: {}, 1: {}, 2: {}}

    # Get the list of users and partition them to the respective platform
    for guild_id, users in task_list.items():
        guild = bot.get_guild(int(guild_id))  # TODO: Handle deleted guilds

        for user_id, user_choice in users.items():
            user = guild.get_member(int(user_id))
            if user is None:
                print(f"{user_id} in {guild_id} not found")
                continue
            change_queries[user_choice][user] = {"guild": guild}

    for platform in [1, 2]:
        write_handle(change_queries[platform], platform)

    for platform in [1, 2]:
        await write_role(change_queries[platform], platform)
        for user in change_queries[platform]:
            if "role" in change_queries[platform][user]:
                print(role)
                role = change_queries[platform][user]["role"]
                await change_role(user, [role])


async def write_role(platform_queries, platform: int):
    '''Recieves a dict of {user: {guild, handle}}, add property role of disnake.Role'''
    if platform == 1:
        handle_list = []
        for person_data in platform_queries.values():
            if person_data["handle"] is not None:
                handle_list.append(person_data["handle"])
        ranks_dict = await cf_external.generate_dict_of_rank(handle_list)

        for person_data in platform_queries.values():
            handle = person_data["handle"]
            if handle is None:
                continue
            handle = handle.lower()
            guild = person_data["guild"]
            guild_roles = await get_roles(guild)
            role_name = ranks_dict[handle]
            role = guild_roles[role_name]
            person_data["role"] = role
    
    elif platform==2:
        for person_data in platform_queries.values():
            handle = person_data["handle"]
            if handle is None:
                continue
            handle = handle.lower()
            guild = person_data["guild"]
            guild_roles = await get_roles(guild)
            role_name = await cc_external.get_user_star(handle)
            role = guild_roles[role_name]
            person_data["role"] = role


def get_task_list():
    '''Get the total update list'''
    json_data = json_file.load_from_json("/update")
    return json_data


async def get_roles(guild: disnake.Guild) -> dict:
    '''Find or create needed roles in a guild.
    Returns a dict of role.name-disnake.Role pairs'''
    result = dict()
    online_guild_role_list = dict(
        [(role.name, role) for role in await guild.fetch_roles()])
    for role_name, color in reversed(list(RANKCOLOR.items())):
        if role_name not in online_guild_role_list:
            role = await guild.create_role(name=role_name, color=color, hoist=True)
            result[role_name] = role
        else:
            result[role_name] = online_guild_role_list[role_name]
    return result


def remove_guild(guild_id: str):
    '''Delete data abt a guild'''
    json_data = json_file.load_from_json("/update")
    if str(guild_id) in json_data:
        json_data.pop(str(guild_id))
    json_file.write_to_json("/update", json_data)


def get_role_with_name(guild: disnake.Guild, role_name: str) -> disnake.Role:
    all_roles = guild.roles

    for role in all_roles:
        if role.name == role_name:
            return role

    raise Exception("Role not found")


async def change_role(member: disnake.Member, roles_to_add) -> None:
    '''Remove current role and add specified role if differs. 
    All roles are added and removed at once to reduce request count'''
    # TODO: Limit to 2 requests per call
    # roles_to_remove = list()
    for role in member.roles:
        if role.name in RANKCOLOR and role not in roles_to_add:
            # roles_to_remove.append(role)
            await member.remove_roles(role)
    # await member.remove_roles(*roles_to_remove)

    # roles_to_add = list()
    for role in roles_to_add:
        if role not in member.roles:
            # roles_to_add.append(role)
            await member.add_roles(role)
    # await member.add_roles(*roles_to_add)
