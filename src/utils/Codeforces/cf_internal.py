'''Codeforces Json file read/write'''
from os import environ
import json
from dotenv import load_dotenv


def assign_handle(userid: str, handle: str):
    '''Assign CF handle to user'''
    userid = str(userid)
    load_dotenv()
    path = environ.get("DATAPATH")
    with open(f"{path}/handle.json", "r+") as json_file:
        json_data = json.load(json_file)
        json_file.seek(0)
        json_data[userid] = handle
        json.dump(json_data, json_file)
        json_file.truncate()


def get_handle(userid: str):
    '''Query a CF handle of someone'''
    userid = str(userid)
    load_dotenv()
    path = environ.get("DATAPATH")
    with open(f"{path}/handle.json", "r") as json_file:
        json_data = json.load(json_file)
        if userid in json_data:
            return json_data[userid]
        return None
