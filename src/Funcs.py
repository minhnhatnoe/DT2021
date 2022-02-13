from disnake import Embed
import json
import requests

rankcolor = {
    "newbie": 0xCCCCCC,
    "pupil": 0x77FF77,
    "specialist": 0x77DDBB,
    "expert": 0xAAAAFF,
    "candidate master": 0xFF88FF,
    "master": 0xFFCC88,
    "international master": 0xFFBB55,
    "grandmaster": 0xFF7777,
    "international grandmaster": 0xFF3333,
    "legendary grandmaster": 0xAA0000
}

def getuser(userlist):
    try:
        fromnet = requests.get(f"https://codeforces.com/api/user.info?handles={';'.join(userlist)}").text
    except:
        raise("Network Error")
    json_data = json.loads(fromnet)
    if json_data["status"] == "Failed":
        raise("Server Error")
    return json_data["result"]

def userEmbed(handle: str, dischand: str):
    data = getuser([handle])[0]
    obj = Embed(title = dischand, color=rankcolor[data["rank"]], description=data["rank"].title())
    # obj.set_image(url=data["titlePhoto"])
    obj.set_thumbnail(url=data["avatar"])
    obj.add_field("Handle", data["handle"])
    if "firstName" in data and "lastName" in data:
        obj.add_field("Name", data["firstName"] + " " + data["lastName"])
    if "country" in data:
        obj.add_field("Country", data["country"])
    if "city" in data:
        obj.add_field("City", data["city"])
    if "organization" in data:
        obj.add_field("Organization", data["organization"])
    obj.add_field("Rating", data["rating"])
    return obj