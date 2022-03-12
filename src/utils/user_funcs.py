'''Functions concerning users as individuals'''
import disnake
from disnake.ext import commands
from src.utils import json_file
from src.utils.constants import RANKCOLOR


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


def align(name: disnake.User) -> str:
    '''Align strings as if using tab'''
    name = name.display_name
    return name + " "*(20-len(name))


def dump_all_handle(bot: commands.Bot, handle_type: int):
    '''Get the dict off all handles'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))

    json_data = json_file.load_from_json(file_names[handle_type])
    data = [(bot.get_user(int(user_id)), handle)
            for user_id, handle in json_data.items()]
    message_content = '\n'.join(
        [f"{align(user)}: {handle}" for user, handle in data])
    message_content = '```\n' + message_content + "\n```"
    return message_content


def write_handle(users, handle_type: int):
    '''Query a bunch of user's handle, 1 is codeforces, 2 is codechef.
    Returns a dict of user_id-handle pair. If not found value is None'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))
    json_data = json_file.load_from_json(file_names[handle_type])

    for (user, guild), user_data in users.items():  # pylint: disable=unused-variable
        if str(user.id) in json_data:
            user_data["handle"] = json_data[str(user.id)]
        else:
            user_data["handle"] = None


async def change_role(member: disnake.Member, roles_to_add) -> None:
    '''Remove current role and add specified role if differs.
    All roles are added and removed at once to reduce request count'''
    rm_list = list()
    for role in member.roles:
        if role.name in RANKCOLOR and role not in roles_to_add:
            rm_list.append(role)
    if len(rm_list) != 0:
        await member.remove_roles(*rm_list)

    add_list = list()
    for role in roles_to_add:
        if role not in member.roles:
            add_list.append(role)
    if len(roles_to_add) != 0:
        await member.add_roles(*add_list)
