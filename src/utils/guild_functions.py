'''All functions regarding a guild'''
import disnake
from src import cfg
from src.utils import json_file
from src.utils.platform_class import RANKCOLOR


def info_allowed(guild: disnake.Guild, choice: str) -> bool:
    '''Check if the provided guild allows for info query'''
    config = json_file.load_from_json("/server_config")
    return config[str(guild.id)]["info"][choice]


def role_create_allowed(guild: disnake.Guild) -> bool:
    '''Check if the provided guild allows creating roles'''
    config = json_file.load_from_json("/server_config")
    return config[str(guild.id)]["make_roles"]


async def standardize_guild(guild_id: int) -> disnake.Guild | None:
    '''Make roles in a guild and return that guild'''
    guild = cfg.bot.get_guild(int(guild_id))
    if guild is None:
        return None
    if not role_create_allowed(guild):
        return None
    await create_roles_in_guild(guild)
    return guild


def get_role_with_name(guild: disnake.Guild, role_name: str) -> disnake.Role:
    '''Get role with specified name from a guild. Returns disnake.Role obj'''
    for role in guild.roles:
        if role.name == role_name:
            return role
    raise Exception("Role not found")


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
