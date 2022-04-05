import disnake
from disnake.ext import commands
from src.utils import codeforces_external, user_functions

async def update_handle(bot: commands.Bot, inter: disnake.CommandInteraction,
                        user: disnake.User, handle: str, choice_id: int):
    if handle == "":
        user_functions.member_handle_record(user, handle, choice_id)
        await inter.response.send_message(f"{user.mention} is unlinked")
        return
    
    try:
        embed_obj = await codeforces_external.generate_user_embed(bot, handle, user)
        user_functions.member_handle_record(user, handle, 1)
        await inter.response.send_message(
            f"{user.mention} linked with {handle}", embed=embed_obj)
    except codeforces_external.CFApi as inst:
        if str(inst) == "Handle Error":
            message_content = "Error occurred. Check provided handle"
        await inter.response.send_message(message_content)
        
        
        user_functions.member_handle_record(user, handle, 2)
        if handle == "":
            message_content = f"{user.mention} is unlinked"
        else:
            message_content = f"{user.mention} is linked with Codechef account {handle}"
        await inter.edit_original_message(content=message_content)
