'''All functions regarding a guild'''
import disnake
from disnake.ext import commands
from src.utils import json_file, cf_external, cc_external
from src.utils.user_funcs import write_handle, change_role
from src.utils.constants import *

def get_task_list():
    '''Get the total update list'''
    json_data = json_file.load_from_json("/update")
    return json_data


async def refresh_roles(bot: commands.Bot):
    '''Refresh all roles in a guild. Provide either guildlist or bot'''
    task_list = get_task_list()
    # Some sets of disnake.user - guild/handle/role pairs
    change_queries = {0: {}, 1: {}, 2: {}}

    # Get the list of users and partition them to the respective platform
    for guild_id, users in task_list.items():
        guild = bot.get_guild(int(guild_id))  # TODO: Handle deleted guilds
        await create_roles(guild)
        for user_id, user_choice in users.items():
            user = guild.get_member(int(user_id))
            if user is None:
                print(f"{user_id} in {guild_id} not found")
                continue
            change_queries[user_choice][(user, guild)] = {}

    for platform in [1, 2]:
        # This is in user_funcs
        write_handle(change_queries[platform], platform)

    for platform in [1, 2]:
        await write_role(change_queries[platform], platform)
        for (user, guild), user_data in change_queries[platform].items():
            if "role" in user_data:
                role = user_data["role"]
                await change_role(user, [role])  # This is in user_funcs


def get_role_with_name(guild: disnake.Guild, role_name: str) -> disnake.Role:
    for role in guild.roles:
        if role.name == role_name:
            return role

    raise Exception("Role not found")


async def write_role(platform_queries, platform: int):
    '''Recieves a dict of {(user, guild): {handle}}, add property role of disnake.Role. The key is user, guild for hashing'''
    if platform == 1:
        handle_list = []
        for person_data in platform_queries.values():
            if person_data["handle"] is not None:
                handle_list.append(person_data["handle"])
        ranks_dict = await cf_external.generate_dict_of_rank(handle_list)

        for (member, guild), person_data in platform_queries.items():
            handle = person_data["handle"]
            if handle is None:
                continue
            handle = handle.lower()
            role_name = ranks_dict[handle]
            role = get_role_with_name(guild, role_name)
            person_data["role"] = role

    elif platform == 2:
        for (member, guild), person_data in platform_queries.items():
            handle = person_data["handle"]
            if handle is None:
                continue
            handle = handle.lower()
            role_name = await cc_external.get_user_star(handle)
            role = get_role_with_name(guild, role_name)
            person_data["role"] = role


async def create_roles(guild: disnake.Guild) -> None:
    '''Create needed roles in a guild'''
    online_guild_role_list = dict(
        [(role.name, role) for role in await guild.fetch_roles()])
    for role_name, color in reversed(list(RANKCOLOR.items())):
        if role_name not in online_guild_role_list:
            role = await guild.create_role(name=role_name, color=color, hoist=True)


async def delete_roles(guild: disnake.Guild) -> None:
    for role in guild.roles:
        if role.name in RANKCOLOR:
            await role.delete()


def remove_guild(guild: disnake.Guild):
    '''Delete data abt a guild'''
    json_data = json_file.load_from_json("/update")
    if str(guild.id) in json_data:
        json_data.pop(str(guild.id))
    json_file.write_to_json("/update", json_data)
