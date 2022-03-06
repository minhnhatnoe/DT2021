'''A file containing helper functions about guilds'''

import disnake

def get_role_with_name(guild: disnake.Guild, role_name: str) -> disnake.Role:
    all_roles = guild.roles

    for role in all_roles:
        if role.name == role_name:
            return role
    
    raise Exception("Role not found")

async def modify_role(member: disnake.Member, remove_role_list: set[disnake.Role], add_role_list: set[disnake.Role]) -> None:
    for role in remove_role_list:
        if role in member.roles:
            if role not in add_role_list:
                await member.remove_roles(role)
    
    for role in add_role_list:
        if role not in member.roles:
            await member.add_roles(role)