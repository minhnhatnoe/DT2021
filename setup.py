'''Script to setup everything'''
from os import system
import platform


def dependencies_check():
    '''Check and install dependencies'''
    try:
        import dotenv
        import disnake
        import flask
        import aiohttp
        import bs4
    except ImportError:
        # Determine OS, documentation: https://docs.python.org/3/library/platform.html
        running_os = platform.system()
        if running_os == "":
            a = input(
                "Cannot detect OS. Type command for installing required dependencies:")
        if running_os == "Windows":
            system("pip install -r requirements.txt")
        elif running_os == "Linux":
            system("pip3 install -r requirements.txt")
        else:
            print(
                f"OS not supported. OS: {running_os}. Pls try installing the required dependencies manually")


def create_dotenv():
    '''Create the required dotenv file'''
    bot_token = input("Specify bot's token: ")
    test_guilds = input(
        "Specify test guilds for this bot (Seperated by comma): ")
    data_path = input("Specify database path (defaults to ./Data): ")
    with open(".env", "w") as env_file:
        env_file.write(
            f'TOKEN = {bot_token}\nDATAPATH = {data_path}\nTEST_GUILDS = {test_guilds}')


def data_create():
    from dotenv import load_dotenv
    from os import environ
    load_dotenv()
    path = environ.get("DATAPATH")
    for filepath in ["/update", "/cfhandle", "/cchandle"]:
        with open(f"{path}{filepath}.json", "w") as file:
            file.write("{}")


if __name__ == '__main__':
    print("Installing")
    dependencies_check()
    create_dotenv()
    data_create()