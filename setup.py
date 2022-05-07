'''Script to setup everything'''
from os import system
import platform


def dependencies_check():
    '''Check and install dependencies'''
    try:
        import dotenv, disnake, flask, aiohttp, bs4 # pylint: disable=import-outside-toplevel,multiple-imports,unused-import
    except ImportError:
        # Determine OS, documentation: https://docs.python.org/3/library/platform.html
        running_os = platform.system()
        if running_os == "":
            cmd = input(
                "Cannot detect OS. Type command for installing required dependencies:")
            system(cmd)
        if running_os == "Windows":
            system("pip install -r requirements.txt")
        elif running_os == "Linux":
            system("pip3 install -r requirements.txt")
        else:
            print(
                f"OS not supported. OS: {running_os}. Try installing dependencies manually")


def create_dotenv():
    '''Create the required dotenv file'''
    bot_token = input("Specify bot's token: ")
    test_guilds = input(
        "Specify test guilds for this bot (Seperated by comma): ")
    data_path = input("Specify database path (defaults to ./Data): ")
    if data_path == "":
        data_path = "./Data"

    rate = input("Interval of refresh in minutes (defaults to 10min): ")
    if rate == "":
        rate = 10

    address = input("Input address for deployment ping (defaults to None)")
    if address == "":
        address = "None"
    with open(".env", "w", encoding="utf-8") as env_file:
        env_file.write(
f'''TOKEN = {bot_token}
DATAPATH = {data_path}
TEST_GUILDS = {test_guilds}
REFRESH_RATE = {rate}
DEPLOY_ADDRESS = {address}''')


def data_create():
    '''Create all files for database use'''
    from dotenv import load_dotenv # pylint: disable=import-outside-toplevel
    from os import environ # pylint: disable=import-outside-toplevel
    load_dotenv()
    path = environ.get("DATAPATH")
    for filepath in ["/update", "/cfhandle", "/cchandle", "/cfunhandle"]:
        with open(f"{path}{filepath}.json", "w", encoding="utf-8") as file:
            file.write(r"{}")


if __name__ == '__main__':
    print("Installing")
    dependencies_check()
    create_dotenv()
    data_create()
