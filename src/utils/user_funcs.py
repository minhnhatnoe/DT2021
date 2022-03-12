'''Functions concerning users as individuals'''
import disnake
from disnake.ext import commands
from src.utils import json_file
from src.utils.constants import RANKCOLOR


def update_change(member: disnake.Member, update_type: int):
    '''Add user to update list. 0 is None, 1 is Codeforces, 2 is Codechef'''
    update_dict = json_file.load_from_json("/update")
    update_dict[str(member.guild.id)][str(member.id)] = update_type
    json_file.write_to_json("/update", update_dict)


async def change_role(member: disnake.Member, roles_to_add) -> None:
    '''Remove current role and add specified role if differs.
    All roles are added and removed at once to reduce request count'''
    rm_list = []
    for role in member.roles:
        if role.name in RANKCOLOR and role not in roles_to_add:
            rm_list.append(role)
    if len(rm_list) != 0:
        await member.remove_roles(*rm_list)

    add_list = []
    for role in roles_to_add:
        if role not in member.roles:
            add_list.append(role)
    if len(roles_to_add) != 0:
        await member.add_roles(*add_list)


class Handle(Exception):
    '''Class for throwing handle-related Exceptions'''


file_names = ["", "/cfhandle", "/cchandle"]


def assign_handle(member: disnake.Member, handle: str, handle_type: int):
    '''Assign handle to user, 1 is codeforces, 2 is codechef. Also changes update list'''
    handle_dict = json_file.load_from_json(file_names[handle_type])
    if handle == "":
        if str(member.id) in handle_dict:
            handle_dict.pop(str(member.id))
        update_change(member, 0)
    else:
        handle_dict[str(member.id)] = handle
        update_change(member, handle_type)
    json_file.write_to_json(file_names[handle_type], handle_dict)


def get_handle(member: disnake.Member, handle_type: int):
    '''Query user's handle, 1 is codeforces, 2 is codechef'''
    handle_dict = json_file.load_from_json(file_names[handle_type])

    if str(member.id) not in handle_dict:
        return None
    return handle_dict[str(member.id)]


def align(name: disnake.User) -> str:
    '''Align strings as if using tab'''
    name = name.display_name
    return name + " "*(20-len(name))


def dump_all_handle(bot: commands.Bot, handle_type: int):
    '''Get a string containing all handles and respective usernames'''
    handle_dict = json_file.load_from_json(file_names[handle_type])

    message_content = '```\n'
    for user_id, handle in handle_dict.items():
        name = bot.get_user(int(user_id)).display_name
        message_content += f'{align(name)}: {handle}\n'
    message_content += '\n```'
    return message_content


def write_handle(users, handle_type: int):
    '''Query a bunch of user's handle, 1 is codeforces, 2 is codechef.
    Returns a dict of user_id-handle pair. If not found value is None'''
    handle_dict = json_file.load_from_json(file_names[handle_type])
    for (user, guild), user_data in users.items():  # pylint: disable=unused-variable
        if str(user.id) in handle_dict:
            user_data["handle"] = handle_dict[str(user.id)]
        else:
            user_data["handle"] = None
