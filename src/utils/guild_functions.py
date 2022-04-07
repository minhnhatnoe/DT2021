'''All functions regarding a guild'''
import disnake
from disnake.ext import commands
from src.utils import json_file
from src.utils.constants import RANKCOLOR


async def standardize_guild(bot: commands.Bot, guild_id: int):
    '''Make roles in a guild and return that guild'''
    guild = bot.get_guild(int(guild_id))
    if guild is None:
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
