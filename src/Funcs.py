from disnake import Embed
import json
import requests

rankcolor = {
    "newbie": 13421772,
    "pupil": 7864183,
    "specialist": 12311927
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