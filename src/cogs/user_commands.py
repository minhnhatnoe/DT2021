'''General commands used by people'''
from disnake.ext import commands
import disnake
from src.utils import user_funcs, cf_external
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
        '''/gen update @<Discord>: Add someone to the handle update list without mention'''
        user_funcs.user_update_choice_change(user, UPDATECHOICES[choice])
        message_content = f"{user.display_name} has been added to the update with {choice}"
        await inter.response.send_message(message_content)

    @user.sub_command()
    async def assign(self, inter: disnake.CommandInteraction,
                     user: disnake.User, handle: str = "",
                     choice: str = commands.Param(choices=UPDATECHOICELIST)):
        '''/cf assign <CF Handle>: Link user to handle, delete if blank'''
        await inter.response.defer()
        if UPDATECHOICES[choice] == 1:
            if handle == "":
                user_funcs.member_handle_record(user, handle, 1)
                await inter.response.send_message(f"{user.mention} is unlinked")
                return
            try:
                embed_obj = await cf_external.generate_user_embed(self.bot, handle, user)
                user_funcs.member_handle_record(user, handle, 1)
                await inter.response.send_message(
                    f"{user.mention} linked with {handle}", embed=embed_obj)
            except cf_external.CFApi as inst:
                if str(inst) == "Handle Error":
                    message_content = "Error occurred. Check provided handle"
                await inter.response.send_message(message_content)
        else:
            user_funcs.member_handle_record(user, handle, 2)
            if handle == "":
                message_content = f"{user.mention} is unlinked"
            else:
                message_content = f"{user.mention} is linked with Codechef account {handle}"
            await inter.edit_original_message(content=message_content)

    @user.sub_command()
    async def info(self, inter: disnake.CommandInteraction, user: disnake.User):
        '''/cf info @<Discord>: Get someone's CF handle'''

        handle = user_funcs.member_handle_query(user, 1)
        if handle is None:
            message_content = f"{user.mention} not introduced yet"
            await inter.response.send_message(content=message_content)
        else:
            embed_obj = await cf_external.generate_user_embed(self.bot, handle, user)
            await inter.response.send_message(embed=embed_obj)


def setup(bot: commands.Bot):
    '''Add the "gen" cog'''
    bot.add_cog(UserCommand(bot))
