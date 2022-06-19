'''Module for admin-only commands in guilds'''
import disnake
from disnake.ext import commands
from src.utils import guild_functions


class AdminCommands(commands.Cog):
    '''Cog for admin-only commands'''

    @commands.slash_command()
    async def admin(self, inter: disnake.CommandInteraction, *args):
        '''Admin cog'''

    @admin.sub_command()
    async def clear(self, inter: disnake.CommandInteraction):
        '''/admin clear: Clear all roles with matching names from server'''
        if inter.author.guild_permissions.administrator:
            await inter.response.defer()
            await guild_functions.remove_roles_in_guild(inter.guild)
            await inter.edit_original_message(content="All roles cleared")
        else:
            await inter.response.send_message("You're not an admin, why bother with this?")

    @admin.sub_command()
    async def show(self, inter: disnake.CommandInteraction):
        '''/admin show: Show whether the bot considers you to be an admin or not'''
        if inter.author.guild_permissions.administrator:
            await inter.response.send_message("You are an admin")
        else:
            await inter.response.send_message("You are not an admin")

    @admin.sub_command_group()
    async def edit(self, inter: disnake.CommandInteraction, *args):
        '''Edit configs for a specific guild'''


def setup(bot: commands.Bot):
    '''Add the AdminCommands cog'''
    bot.add_cog(AdminCommands())

# TODO: Change server configs
