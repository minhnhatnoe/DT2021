'''Functions concerning users as individuals'''
import disnake
from src.utils import json_file
from src.utils.constants import *


def update_change(member: disnake.Member, update_type: int):
    '''Add user to update list. 0 is None, 1 is Codeforces, 2 is Codechef'''
    json_data = json_file.load_from_json("/update")
    json_data[str(member.guild.id)][str(member.id)] = update_type
    json_file.write_to_json("/update", json_data)


class Handle(Exception):
    '''Class for throwing handle-related Exceptions'''


file_names = ["", "/cfhandle", "/cchandle"]


def assign_handle(member: disnake.Member, handle: str, handle_type: int):
    '''Assign handle to user, 1 is codeforces, 2 is codechef'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))

    json_data = json_file.load_from_json(file_names[handle_type])
    json_data[str(member.id)] = handle
    json_file.write_to_json(file_names[handle_type], json_data)


def get_handle(member: disnake.Member, handle_type: int):
    '''Query user's handle, 1 is codeforces, 2 is codechef'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))

    json_data = json_file.load_from_json(file_names[handle_type])
    if str(member.id) not in json_data:
        return None
    return json_data[str(member.id)]


def get_all_handle(handle_type: int):
    '''Get the dict off all handles'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))

    json_data = json_file.load_from_json(file_names[handle_type])
    return json_data


def write_handle(users, handle_type: int):
    '''Query a bunch of user's handle, 1 is codeforces, 2 is codechef.
    Returns a dict of user_id-handle pair. If not found value is None'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))
    json_data = json_file.load_from_json(file_names[handle_type])

    for (user, guild), user_data in users.items():
        if str(user.id) in json_data:
            user_data["handle"] = json_data[str(user.id)]
        else:
            user_data["handle"] = None


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
