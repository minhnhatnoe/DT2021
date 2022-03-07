'''Functions concerning users as individuals'''
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

def bulk_get_handle(user_ids, handle_type: int):
    '''Query a bunch of user's handle, 1 is codeforces, 2 is codechef
    Returns a dict of user_id-handle pair'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))
    
    json_data = json_file.load_from_json(file_names[handle_type])
    result = dict([(str(user_id), json_data[str(user_id)]) for user_id in user_ids])
    return result