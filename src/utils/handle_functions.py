'''Things related to platform handles'''
import disnake
from disnake.ext import commands
from src.utils import json_file
from src.utils.constants import PLATFORMIDS


class Handle(Exception):
    '''Class for throwing handle-related Exceptions'''


file_names = {
    1: "/cfhandle",
    2: "/cchandle",
    4: "/cfunhandle"
}


def member_handle_record(member: disnake.Member, handle: str, handle_type: int):
    '''Assign handle to user, 1 is codeforces, 2 is codechef. Also changes update list'''
    handle_dict = json_file.load_from_json(file_names[handle_type])
    if handle == "":
        if str(member.id) in handle_dict:
            handle_dict.pop(str(member.id))
    else:
        handle_dict[str(member.id)] = handle
    json_file.write_to_json(file_names[handle_type], handle_dict)


def member_handle_query(member: disnake.Member, handle_type: int):
    '''Query user's handle, 1 is codeforces, 2 is codechef'''
    handle_dict = json_file.load_from_json(file_names[handle_type])

    if str(member.id) not in handle_dict:
        return None
    return handle_dict[str(member.id)]


def align_string(name: disnake.User) -> str:
    '''Align strings as if using tab'''
    return name + " "*(20-len(name))


def handle_database_dump(bot: commands.Bot, handle_type: int):
    '''Get a string containing all handles and respective usernames'''
    handle_dict = json_file.load_from_json(file_names[handle_type])

    message_content = '```\n'
    for user_id, handle in handle_dict.items():
        name = bot.get_user(int(user_id)).display_name
        message_content += f'{align_string(name)}: {handle}\n'
    message_content += '\n```'
    return message_content


def write_handle_attr_to_dict(change_queries):
    '''Query a bunch of user's handle, 1 is codeforces, 2 is codechef.
    Returns a dict of user_id-handle pair. If not found value is None'''
    for handle_type in PLATFORMIDS:
        handle_dict = json_file.load_from_json(file_names[handle_type])
        for (user, _), user_data in change_queries[handle_type].items():
            if str(user.id) in handle_dict:
                user_data["handle"] = handle_dict[str(user.id)]
            else:
                user_data["handle"] = None
