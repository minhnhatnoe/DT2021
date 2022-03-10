'''Functions concerning users as individuals'''
import json
from src.utils import json_file


def update_change(guild_id: str, user_id: str, update_type: int):
    '''Add user to update list. 0 is None, 1 is Codeforces, 2 is Codechef'''
    json_data = json_file.load_from_json("/update")
    json_data[str(guild_id)][str(user_id)] = update_type
    json_file.write_to_json("/update", json_data)


class Handle(Exception):
    '''Class for throwing handle-related Exceptions'''


file_names = ["", "/cfhandle", "/cchandle"]


def assign_handle(user_id: str, handle: str, handle_type: int):
    '''Assign handle to user, 1 is codeforces, 2 is codechef'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))

    json_data = json_file.load_from_json(file_names[handle_type])
    json_data[str(user_id)] = handle
    json_file.write_to_json(file_names[handle_type], json_data)


def get_handle(user_id: str, handle_type: int):
    '''Query user's handle, 1 is codeforces, 2 is codechef'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))

    json_data = json_file.load_from_json(file_names[handle_type])
    return json_data[str(user_id)]


def write_handle(users, handle_type: int):
    '''Query a bunch of user's handle, 1 is codeforces, 2 is codechef.
    Returns a dict of user_id-handle pair. If not found value is None'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))
    json_data = json_file.load_from_json(file_names[handle_type])

    for user in users:
        if str(user.id) in json_data:
            users[user]["handle"] = json_data[str(user.id)]
        else:
            users[user]["handle"] = None