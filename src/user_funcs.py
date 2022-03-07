'''Functions concerning a particular user'''
from os import environ
import json
from dotenv import load_dotenv
from src.utils.Codeforces import guild_funcs


def update_change(guildid: str, userid: str, val: int):
    '''Add user to update list. 0 is None, 1 is Codeforces, 2 is Codechef'''
    guildid = str(guildid)
    userid = str(userid)

    load_dotenv()
    path = environ.get("DATAPATH")
    with open(f"{path}/update.json", "r+") as json_file:
        json_data = json.load(json_file)
        json_file.seek(0)
        if guildid not in json_data:
            json_data[guildid] = {}
        json_data[guildid][userid] = val
        json.dump(json_data, json_file)
        json_file.truncate()


# async def clear_user_role(guild, user):
#     '''Clear role of a user from a guild'''
#     rolelist = guild_funcs.get_roles(guild.id)

#     if rolelist is None:
#         return
#     for role in user.roles:
#         if role.id in rolelist.values():
#             await user.remove_roles(role)
