import requests
import json
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

def getuser(userlist):
    try:
        fromnet = requests.get(f"codeforces.com/api/user.info?handles={';'.join(userlist)}")
    except:
        raise("Network Error")
    json_data = json.loads(fromnet)
    if json_data["status"] == "Failed":
        raise("Server Error")
    return json_data["result"]

def refreshrank():
    pass