'''Functions concerning a particular user'''
from os import environ
import json
from dotenv import load_dotenv
from src.funcs import GuildFuncs

def add_to_update(guildid: str, userid: str):
    '''Add user to update list'''
    guildid = str(guildid)
    userid = str(userid)

    load_dotenv()
    path = environ.get("DATAPATH")
    with open(f"{path}/update.json", "r+") as json_file:
        json_data = json.load(json_file)
        json_file.seek(0)
        if guildid not in json_data:
            json_data[guildid] = {}
        json_data[guildid][userid] = True
        json.dump(json_data, json_file)
        json_file.truncate()

def delete_from_update(guildid: str, userid: str):
    '''Remove from update list'''
    guildid = str(guildid)
    userid = str(userid)

    load_dotenv()
    path = environ.get("DATAPATH")
    with open(f"{path}/update.json", "r+") as json_file:
        json_data = json.load(json_file)
        json_file.seek(0)
        if guildid not in json_data:
            json_data[guildid] = {}
        if userid in json_data[guildid]:
            json_data[guildid][userid] = False
        json.dump(json_data, json_file)
        json_file.truncate()

async def clear_user_role(guild, user):
    '''Clear role of a user from a guild'''
    rolelist = GuildFuncs.get_roles(guild.id)

    if rolelist is None:
        return
    for role in user.roles:
        if role.id in rolelist.values():
            await user.remove_roles(role)