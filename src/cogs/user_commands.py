'''General commands used by people'''
from disnake.ext import commands
import disnake
from src.utils import codeforces_external, codechef_external, user_functions
from src.utils.constants import UPDATECHOICES, UPDATECHOICELIST


class UserCommand(commands.Cog):
    "A cog for all of commands regarding general Discord stuff"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def user(self, inter: disnake.CommandInteraction, *args):
        '''Commands about an user'''

    @user.sub_command()
    async def update(self, inter: disnake.CommandInteraction, user: disnake.User,  # pylint: disable=no-self-use
                     choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/user update @<Discord>: Add someone to the handle update list without mention'''
        user_functions.user_update_choice_change(user, UPDATECHOICES[choice])
        message_content = f"{user.display_name} has been added to the update with {choice}"
        await inter.response.send_message(message_content)

    @user.sub_command()
    async def assign(self, inter: disnake.CommandInteraction,
                     user: disnake.User, handle: str,
                     choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/user assign <CF Handle>: Link user to handle'''
        await inter.response.defer()
        choice_id = UPDATECHOICES[choice]
        try:
            embed_obj = await user_functions.generate_user_embed(
                self.bot, handle, user, choice_id)
            verify_result = await user_functions.verify(self.bot, user, handle, choice_id)
            if verify_result:
                user_functions.member_handle_record(user, handle, choice_id)
                await inter.edit_original_message(
                    content=f"{user.mention} linked with {handle}", embed=embed_obj)
            else:
                await inter.edit_original_message(content="Verification failed. Restart if needed")

        except codeforces_external.CFApi as inst:
            message_content: str
            if str(inst) == "Handle Error":
                message_content = "Check provided handle"
            await inter.edit_original_message(content=message_content)

        except codechef_external.CCApi as inst:
            await inter.edit_original_message(content=f"Error occured. Error code: {str(inst)}")

    @user.sub_command()
    async def unassign(self, inter: disnake.CommandInteraction, user: disnake.User,  # pylint: disable=no-self-use
                       choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/user unassign: Delete user's handle'''
        choice_id = UPDATECHOICES[choice]
        user_functions.member_handle_record(user, "", choice_id)
        await inter.response.send_message(content=f"{user.mention} is unlinked")

    @user.sub_command()
    async def info(self, inter: disnake.CommandInteraction, user: disnake.User,
                   choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/user info @<Discord>: Get someone's CF handle'''
        choice_id = UPDATECHOICES[choice]
        handle = user_functions.member_handle_query(user, choice_id)
        if handle is None:
            message_content = f"{user.mention} not introduced yet"
            await inter.response.send_message(content=message_content)
        else:
            embed_obj = await user_functions.generate_user_embed(self.bot, handle, user, choice_id)
            await inter.response.send_message(embed=embed_obj)


def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(UserCommand(bot))
