'''Functions concerning users as individuals'''
import disnake
from disnake import Embed
from disnake.ext import commands
from src.utils import json_file, codechef_external, codeforces_external
from src.utils.constants import RANKCOLOR


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


def generate_user_embed(bot: commands.Bot, handle: str,
                        member: disnake.Member, choice_id: int) -> Embed:
    '''Generate an user embed'''
    # I dont know how to declare a function without pylint warning
    embed_generator: codeforces_external.generate_user_embed

    if choice_id == 1:
        embed_generator = codeforces_external.generate_user_embed
    elif choice_id == 2:
        embed_generator = codechef_external.generate_user_embed
    else:
        raise Exception("Invalid choice")
    return embed_generator(bot, handle, member)


async def verify(bot: commands.Bot, member: disnake.Member, handle: str, choice_id: int) -> bool:
    '''Perform verification process, assuming handle exist'''
    if choice_id == 1:
        return await codeforces_external.verify(bot, member, handle)
    if choice_id == 2:
        return await codechef_external.verify(bot, member, handle)
