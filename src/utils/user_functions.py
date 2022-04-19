'''Functions concerning users as individuals'''
import disnake
from disnake import Embed
from src.utils.platform_class import RANKCOLOR, PLATFORM_CLASS
from src.utils import json_file


def user_update_choice_change(member: disnake.Member, update_type: int):
    '''Add user to update list. 0 is None, 1 is Codeforces, 2 is Codechef'''
    update_dict = json_file.load_from_json("/update")
    if str(member.guild.id) not in update_dict:
        update_dict[str(member.guild.id)] = {}
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


def generate_user_embed(handle: str, member: disnake.Member, choice_id: int) -> Embed:
    '''Generate an user embed'''
    platform_class = PLATFORM_CLASS[choice_id]()
    return platform_class.generate_user_embed(handle, member)


async def verify(member: disnake.Member, handle: str, choice_id: int) -> bool:
    '''Perform verification process, assuming handle exist'''
    platform_class = PLATFORM_CLASS[choice_id]()
    return await platform_class.verify(member, handle)
