'''Functions concerning users as individuals'''
import disnake
from disnake import Embed
from disnake.ext import commands
from src.utils import json_file
from src.utils.constants import RANKCOLOR
from src.utils.codechef_external import CodeChefEmbed
from src.utils.codeforces_external import CodeForcesEmbed

def user_update_choice_change(member: disnake.Member, update_type: int):
    '''Add user to update list. 0 is None, 1 is Codeforces, 2 is Codechef'''
    update_dict = json_file.load_from_json("/update")
    update_dict[str(member.guild.id)][str(member.id)] = update_type
    json_file.write_to_json("/update", update_dict)


async def member_assign_role(member: disnake.Member, roles_to_add) -> None:
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


def member_handle_record(member: disnake.Member, handle: str, handle_type: int):
    '''Assign handle to user, 1 is codeforces, 2 is codechef. Also changes update list'''
    handle_dict = json_file.load_from_json(file_names[handle_type])
    if handle == "":
        if str(member.id) in handle_dict:
            handle_dict.pop(str(member.id))
        user_update_choice_change(member, 0)
    else:
        handle_dict[str(member.id)] = handle
        user_update_choice_change(member, handle_type)
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


def write_handle_attr_to_dict(users, handle_type: int):
    '''Query a bunch of user's handle, 1 is codeforces, 2 is codechef.
    Returns a dict of user_id-handle pair. If not found value is None'''
    handle_dict = json_file.load_from_json(file_names[handle_type])
    for (user, _), user_data in users.items():
        if str(user.id) in handle_dict:
            user_data["handle"] = handle_dict[str(user.id)]
        else:
            user_data["handle"] = None

def generate_user_embed(bot: commands.Bot, handle: str, member: disnake.Member, choice_id: int) -> Embed:
    embed_generator: function
    if choice_id == 1:
        embed_generator = CodeForcesEmbed.generate_user_embed
    elif choice_id == 2:
        embed_generator = CodeChefEmbed.generate_user_embed
    else:
        raise Exception("Invalid choice")
    return embed_generator(bot, handle, member)