from disnake.ext import commands
import os  # TODO: Minimize footprint of os
from dotenv import load_dotenv

load_dotenv()

guilds = [int(v) for v in os.environ.get("TEST_GUILDS").split(", ")]
bot = commands.Bot(test_guilds=guilds)

@bot.slash_command()
async def ping(inter):
    '''/ping: Get the bot's latency'''
    await inter.response.send_message("Pong!")

@bot.slash_command()
async def helpme(inter):
    '''/helpme: Show this help message'''

    msg = 'Here are several things I can do:'

    command_set = bot.get_guild_slash_commands(inter.guild.id)
    help_msg = []
    for cmd in command_set:
        help_msg.append(cmd.description)
    
    await inter.response.send_message(msg + "```" + "\n".join(help_msg) + "```")

@bot.event
async def on_ready():
    print("Logged in")

bot.load_extension("src.Codeforces.Commands")

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.environ.get("TOKEN"))