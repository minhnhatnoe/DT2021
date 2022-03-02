from src.imports import *
class CFCommand(commands.Cog):
    "A cog for all of commands regarding Codeforces"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def introduce(inter, handle: str):
        '''/introduce <CF Handle>: Let the bot know your Codeforces handle'''
        load_dotenv()
        path = os.environ.get("DATAPATH")
        with open(f"{path}\handle.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data[str(inter.author.id)] = handle
            json.dump(json_data, json_file)
            json_file.truncate()
        await inter.response.send_message(f"{inter.author.mention} has been introduced as {handle}")

    @cf.sub_command()
    async def assign(self, inter, handle: str):
        '''/cf assign <CF Handle>: Let the bot know your Codeforces handle'''
        # try:
        embedobj = await Funcs.CFExternal.get_user_embed(handle, inter.user.id)
        await inter.response.send_message(f"{inter.author.mention} has been introduced as {handle}", embed = embedobj)
        Funcs.CFInternal.assign_handle(inter.author.id, handle)
        # except:
            # await inter.response.send_message(f"Error occurred. Please carefully check provided handle")

    @cf.sub_command()
    async def info(self, inter, user: disnake.User):
        '''/cf info @<Discord>: Get someone's CF handle'''
        handle = Funcs.CFInternal.get_handle(user.id)
        if handle is None:
            await inter.response.send_message(f"{user.mention} has not been introduced yet")
        else:
            # await inter.response.send_message(f"{user.mention}'s handle is {handle}", embed = await Funcs.getUserEmbed(handle, user.name))
            await inter.response.send_message(embed = await Funcs.CFExternal.get_user_embed(handle, user.name))
                
def setup(bot: commands.Bot):
    bot.add_cog(CFCommand(bot))