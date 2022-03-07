'''Functions concerning a particular user'''
from src.utils import json_file

def update_change(guild_id: str, user_id: str, update_type: int):
    '''Add user to update list. 0 is None, 1 is Codeforces, 2 is Codechef'''
    json_data = json_file.load_from_json("update")
    json_data[str(guild_id)][str(user_id)] = update_type
    json_file.write_to_json("update")

class Handle(Exception):
    '''Class for throwing handle-related Exceptions'''

file_names = ["", "cfhandle", "cchandle"]
def assign_handle(user_id: str, handle: str, handle_type: int):
    '''Assign handle to user, 1 is codeforces, 2 is codechef'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))

    json_data = json_file.load_from_json("cfhandle")
    json_data[str(user_id)] = handle
    json_file.write_to_json("cfhandle", json_data)


def get_handle(user_id: str, handle_type: int):
    '''Query user's handle, 1 is codeforces, 2 is codechef'''
    if handle_type not in [1, 2]:
        raise Handle(Exception("Invalid handle type"))

    json_data = json_file.load_from_json("cfhandle")
    return json_data[str(user_id)]
