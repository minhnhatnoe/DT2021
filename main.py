import disnake
from disnake.ext import commands
import os  # TODO: Minimize footprint of os
from dotenv import load_dotenv
import json
import src.Codeforces.Funcs
load_dotenv()

guilds = [int(v) for v in os.environ.get("TEST_GUILDS").split(", ")]
bot = commands.Bot(test_guilds=guilds)

@bot.slash_command()
async def ping(inter):
    '''/ping: Get the bot's latency'''
    await inter.response.send_message(f"Pong! ({inter.bot.latency * 1000:.0f}ms)")

@bot.slash_command()
async def helpme(inter):
    '''/helpme: Show this help message'''

    msg = 'Here are several things I can do:'

    command_set = bot.get_guild_slash_commands(inter.guild.id)
    help_msg = []
    for cmd in command_set:
        if cmd.options:
            for opt in cmd.options:
                help_msg.append(opt.description)
        else:
            help_msg.append(cmd.description)
    
    await inter.response.send_message(msg + "```" + "\n".join(help_msg) + "```")

@bot.slash_command()
async def updateme(inter, user: disnake.User):
    '''/updateme @<Discord>: Add someone to the handle update list'''
    load_dotenv()
    path = os.environ.get("DATAPATH")
    with open(f"{path}\update.json", "r+") as json_file:
        json_data = json.load(json_file)
        json_file.seek(0)
        json_data[str(inter.guild)].append(str(user.id))
        json.dump(json_data, json_file)
        json_file.truncate()
    await inter.response.send_message(f"{user.mention} has been added to the update list")

@bot.slash_command()
async def refresh():
    '''/refresh: Refresh all color-based roles'''
    path = os.environ.get("DATAPATH")
    with open(f"{path}\update.json", "r") as json_file:
        json_data = json.load(json_file)
        for guildid in json_data:
            guild = bot.get_guild(int(guildid))
            for userid in json_data[guild]:
                user = guild.get_member(int(userid))
                user.add_roles() # TODO
    await bot.response.send_message("Refreshed all roles")

@bot.event
async def on_ready():
    print("Logged in")

bot.load_extension("src.Codeforces.Commands")

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get("TOKEN"))