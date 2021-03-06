'''General commands used by people'''
from disnake.ext import commands
import disnake
from src.platforms import codechef_external
from src.platforms import codeforces_external
from src.utils import user_functions, guild_functions, handle_functions, refresh_procedure
from src.utils.platform_class import UPDATECHOICES, UPDATECHOICELIST


class UserCommand(commands.Cog):
    "A cog for all of commands regarding general Discord stuff"

    def __init__(self):
        '''Init the cog'''

    @commands.slash_command()
    async def user(self, inter: disnake.CommandInteraction, *args):
        '''Commands about an user'''

    @user.sub_command()
    async def update(self, inter: disnake.CommandInteraction, user: disnake.User,
                     choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/user update @<Discord>: Add someone to the handle update list without mention'''
        user_functions.user_update_choice_change(user, UPDATECHOICES[choice])
        message_content = f"{user.display_name} has been added to the update with {choice}"
        await inter.response.send_message(message_content)
        await refresh_procedure.refresh_roles_of_bot()

    @user.sub_command()
    async def assign(self, inter: disnake.CommandInteraction,
                     user: disnake.User, handle: str,
                     choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/user assign <CF Handle>: Link user to handle'''
        await inter.response.defer()
        choice_id = UPDATECHOICES[choice]
        try:
            embed_obj = await user_functions.generate_user_embed(handle, user, choice_id)
            verify_result = await user_functions.verify(user, handle, choice_id)
            if verify_result:
                handle_functions.member_handle_record(user, handle, choice_id)
                user_functions.user_update_choice_change(user, choice_id)
                await inter.edit_original_message(
                    content=f"{user.mention} linked with {handle}", embed=embed_obj)
                await refresh_procedure.refresh_roles_of_bot()
            else:
                await inter.edit_original_message(content="Verification failed. Restart if needed")
        except codeforces_external.CodeForcesApi as inst:
            message_content: str
            if str(inst) == "Handle Error":
                message_content = "Check provided handle"
            else:
                message_content = f"Error occurred, error code: {inst}"
            await inter.edit_original_message(content=message_content)

        except codechef_external.CodeChefApi as inst:
            await inter.edit_original_message(content=f"Error occured. Error code: {str(inst)}")

    @user.sub_command()
    async def unassign(self, inter: disnake.CommandInteraction, user: disnake.User,
                       choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/user unassign: Delete user's handle'''
        choice_id = UPDATECHOICES[choice]
        handle_functions.member_handle_record(user, "", choice_id)
        user_functions.user_update_choice_change(user, 0)
        await inter.response.send_message(content=f"{user.mention} is unlinked")

    @user.sub_command()
    async def info(self, inter: disnake.CommandInteraction, user: disnake.User,
                   choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/user info @<Discord>: Get someone's CF handle'''
        choice_id = UPDATECHOICES[choice]
        handle = handle_functions.member_handle_query(user, choice_id)
        if not guild_functions.info_allowed(inter.guild, choice):
            await inter.response.send_message(content=
                "This function has been disabled by an admin.")
            return
        if handle is None:
            message_content = f"{user.mention} not introduced yet"
            await inter.response.send_message(content=message_content)
            return
        embed_obj = await user_functions.generate_user_embed(handle, user, choice_id)
        await inter.response.send_message(embed=embed_obj)


def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(UserCommand())
