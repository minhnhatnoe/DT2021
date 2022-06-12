'''Rituals to be done every time the bot starts (for example: check if all guilds are configured)'''
from disnake.ext import commands
from src import cfg
from src.utils import json_file


def check_guilds_config() -> bool:
    config = json_file.load_from_json("/server_config.json")
    for guild in cfg.bot.guilds:
        if str(guild.id) not in config:
            choice = input(f"Guild {guild.name} with id {guild.id} has \
not been configured. Configure with default params? (Y/N)").upper()
            if choice == "Y":
                config[str(guild.id)] = {
                    "roles": {
                        "codefun": False,
                        "codeforces": False,
                        "codechef": False
                    },
                    "info": {
                        "codefun": False,
                        "codeforces": False,
                        "codechef": False
                    }
                }
    json_file.write_to_json("/server_config.json", config)
