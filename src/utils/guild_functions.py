'''All functions regarding a guild'''
from typing import Dict, List
import disnake
from disnake.ext import commands
from src.utils import codechef_external, codeforces_external, json_file, user_functions
from src.utils.constants import RANKCOLOR


async def refresh_roles_of_bot(bot: commands.Bot) -> None:
    '''Refresh all roles in all guilds'''
    task_list = json_file.load_from_json("/update")

    # Some sets of disnake.user - guild/handle/role pairs
    change_queries = {0: {}, 1: {}, 2: {}}
    # Get the list of users and partition them to the respective platform
    for guild_id, users in task_list.items():
        guild = bot.get_guild(int(guild_id))
        if guild is None:
            continue
        await create_roles_in_guild(guild)
        for user_id, user_choice in users.items():
            user = guild.get_member(int(user_id))
            if user is None:
                continue
            change_queries[user_choice][(user, guild)] = {}

    # Get handles of queries
    for platform in [1, 2]:
        user_functions.write_handle_attr_to_dict(
            change_queries[platform], platform)

    # Get role to change of queries
    for platform in [1, 2]:
        await write_role_attr_to_dict(bot, change_queries[platform], platform)
        for (user, guild), user_data in change_queries[platform].items():
            if "role" in user_data:
                role = user_data["role"]
                await user_functions.member_assign_role(user, [role])


def get_role_with_name(guild: disnake.Guild, role_name: str) -> disnake.Role:
    '''Get role with specified name from a guild. Returns disnake.Role obj'''
    for role in guild.roles:
        if role.name == role_name:
            return role
    raise Exception("Role not found")


async def write_role_attr_to_dict(bot: commands.Bot, platform_queries: Dict, platform: int) -> None:
    '''Recieves a dict of {(user, guild): {handle}}, add property role of disnake.Role.
    The key is user, guild for hashing'''
    handle_list = []
    for person_data in platform_queries.values():
        if person_data["handle"] is not None:
            handle_list.append(person_data["handle"])

    ranks_dict = await generate_dict_of_rank(bot, handle_list, platform)

    for (_, guild), person_data in platform_queries.items():
        handle = person_data["handle"]
        if handle is None:
            continue
        handle = handle.lower()
        role_name = ranks_dict[handle]
        role = get_role_with_name(guild, role_name)
        person_data["role"] = role


async def generate_dict_of_rank(bot: commands.Bot, user_list: List, handle_type: int) -> Dict:
    '''Generate a dict of handle-rank, accepting list of str only'''
    result = {}
    if handle_type == 1:
        data = await codeforces_external.get_user_data_from_net(bot, user_list)
        for person in data:
            handle = person["handle"].lower()
            result[handle] = person["rank"]

    elif handle_type == 2:
        for person in user_list:
            handle = person.lower()
            result[handle] = await codechef_external.get_user_role_name(bot, handle)

    return result


async def create_roles_in_guild(guild: disnake.Guild) -> None:
    '''Create needed roles in a guild'''

    fetched_data = await guild.fetch_roles()
    online_guild_role_list = {role.name: role for role in fetched_data}
    for role_name, color in reversed(list(RANKCOLOR.items())):
        if role_name not in online_guild_role_list:
            await guild.create_role(name=role_name, color=color, hoist=True)


async def remove_roles_in_guild(guild: disnake.Guild) -> None:
    '''Delete roles from a discord guild. Deleted roles are specified in RANKCOLOR'''

    for role in guild.roles:
        if role.name in RANKCOLOR:
            await role.delete()


def remove_guild_data(guild: disnake.Guild) -> None:
    '''Delete data abt a guild'''

    json_data = json_file.load_from_json("/update")
    if str(guild.id) in json_data:
        json_data.pop(str(guild.id))
    json_file.write_to_json("/update", json_data)
