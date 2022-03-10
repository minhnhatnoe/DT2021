# guild_functions (cc)
'''A file containing helper functions about guilds'''

import disnake

def get_role_with_name(guild: disnake.Guild, role_name: str) -> disnake.Role:
    all_roles = guild.roles

    for role in all_roles:
        if role.name == role_name:
            return role
    
    raise Exception("Role not found")

async def modify_role(member: disnake.Member, remove_role_list, add_role_list) -> None:
    for role in remove_role_list:
        if role in member.roles:
            if role not in add_role_list:
                await member.remove_roles(role)
    
    for role in add_role_list:
        if role not in member.roles:
            await member.add_roles(role)

# Codechef external
'''Module for fetching data from Codechef'''

import aiohttp
from bs4 import BeautifulSoup
class CCApi(Exception):
    "Base class for all exception raised from getting information from Codechef"

class CodechefData:
    def __init__(self, username: str):
        self.data = self.get_user_data(username)

    async def get_user_data(self, username: str) -> BeautifulSoup:
        '''Returns a soup'''
        request_url = f"https://codechef.com/users/{username}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(request_url) as response:
                    from_net = await response.text()
        except Exception as ex_type:
            raise CCApi(Exception("Network Error")) from ex_type

        soup = BeautifulSoup(from_net, features="html.parser")
        return soup

    def get_user_star(self):
        '''Return star text that can be used to derive role name (ie. 1*, 2*)'''
        star = self.data.select('span[class="rating"]')
        startext = star[0].getText()

        startext = startext.replace('★', '*')
        return startext

@codechef.sub_command()
async def refresh_all(inter):
    '''/cc refresh_all: Refresh all roles for Codechef ranks'''
    await inter.response.defer()
    
    # TODO: Support adding roles to new guilds

    all_guild_member_list = load_from_json("/Codechef/username")

    all_codechef_role = set()
    for star in range(1, 8):
        all_codechef_role.add(guild_functions.get_role_with_name(inter.guild, f"Codechef {star}*"))

    for member_list in all_guild_member_list.values():
        for member_id in member_list.keys():
            member_id = int(member_id)
            member = inter.guild.get_member(member_id)
            codechef_username = member_list[str(member_id)]
            # TODO: add error handling

            star_text = codechef.CodechefData(codechef_username).get_user_star()

            role = guild_functions.get_role_with_name(inter.guild, f"Codechef {star_text}")

            await guild_functions.modify_role(member, all_codechef_role, {role})

    await inter.edit_original_message(content = "All roles refreshed")