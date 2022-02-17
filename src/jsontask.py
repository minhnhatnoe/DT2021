from dotenv import load_dotenv
from os import environ
import json

class jsontask:
    def add_to_update(guildid: str, userid: str):
        guildid = str(guildid)
        userid = str(userid)

        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\update.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            if guildid not in json_data:
                json_data[str(guildid)] = []
            json_data[guildid].append(userid)
            json.dump(json_data, json_file)
            json_file.truncate()
    
    def get_update_list():
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\update.json", "r") as json_file:
            json_data = json.load(json_file)
            return json_data

    def add_roles(guildid: str, rolelist: dict):
        guildid = str(guildid)
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data[guildid] = rolelist
            json.dump(json_data, json_file)
            json_file.truncate()

    def get_roles(guildid: str):
        guildid = str(guildid)
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r") as json_file:
            json_data = json.load(json_file)
            if guildid in json_data:
                return json_data[guildid]
            else:
                return None

    def remove_guild(guildid: str):
        guildid = str(guildid)
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            if str(guildid) in json_data: json_data.pop(str(guildid))
            json.dump(json_data, json_file)
            json_file.truncate()
        
        with open(f"{path}\\update.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            if str(guildid) in json_data: json_data.pop(str(guildid))
            json.dump(json_data, json_file)
            json_file.truncate()
        
    def assign_handle(userid: str, handle: str):
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\handle.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data[userid] = handle
            json.dump(json_data, json_file)
            json_file.truncate()

    def get_handle(userid: str):
        userid = str(userid)
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\handle.json", "r") as json_file:
            json_data = json.load(json_file)
            if userid in json_data:
                return json_data[userid]
            else:
                return None