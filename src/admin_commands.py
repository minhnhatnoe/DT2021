import disnake
from disnake.ext import commands
from src.utils import guild_funcs


class AdminCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.slash_command()
    async def admin(self, inter: disnake.CommandInteraction, *args):
        '''Admin cog'''

    @admin.sub_command()
    async def clear(self, inter: disnake.CommandInteraction):  # pylint: disable=no-self-use
        '''/gen clear: Clear all roles with matching names from server'''
        if inter.author.guild_permissions.administrator:
            await inter.response.defer()
            await guild_funcs.remove_roles_in_guild(inter.guild)
            await inter.edit_original_message(content="All roles cleared")
        else:
            await inter.response.send_message("You're not an admin, why bother with this")

    @admin.sub_command()
    async def show(self, inter: disnake.CommandInteraction):
        if inter.author.guild_permissions.administrator:
            await inter.response.send_message("You are an admin")
        else:
            await inter.response.send_message("You are not an admin")


def setup(bot: commands.Bot):
    '''Add the AdminCommands cog'''
    bot.add_cog(AdminCommands(bot))
