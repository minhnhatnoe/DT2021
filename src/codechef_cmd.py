'''Commands relating to Codechef'''

import disnake
from disnake.ext import commands
from src.utils.json_file import load_from_json, write_to_json
import src.utils.guild_functions as guild_functions
import src.utils.codechef_external as codechef

class CodechefCommand(commands.Cog):
    '''A cog for all commands relating to Codechef'''

    def __init__(self, bot = commands.Bot):
        '''Assign bot for future use'''
        self.bot = bot

    @commands.slash_command(name = "cc")
    async def codechef(inter, *args):
        '''Slash command group for Codechef command'''

    @codechef.sub_command()
    async def assign(inter, user: disnake.User, username: str):
        '''/cc assign <Discord user> <Codechef username>: Assign an user to an username'''
        await inter.response.defer()

        data = load_from_json("/Codechef/username")
        current_guild_id = inter.guild.id
        userid = user.id

        if str(current_guild_id) not in data:
            data[str(current_guild_id)] = dict()

        data[str(current_guild_id)][str(userid)] = username

        write_to_json("/Codechef/username", data)

        await inter.edit_original_message(
            content = f"{user.mention} has been assigned to {username}"
        )

    # Currently not working
    
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

        


def setup(bot: commands.Bot):
    '''Add the cog to bot'''
    bot.add_cog(CodechefCommand(bot))