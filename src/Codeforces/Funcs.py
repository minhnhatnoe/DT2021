from disnake import Embed
import json
from requests import get as rqget

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

def getUserData(userlist):
    try:
        fromnet = rqget(f"https://codeforces.com/api/user.info?handles={';'.join(userlist)}").text
    except:
        raise("Network Error")
    json_data = json.loads(fromnet)
    if json_data["status"] == "Failed":
        raise("Server Error")
    # print(userlist, fromnet)
    return json_data["result"]

def getRoles(userlist):
    data = getUserData(userlist)
    ranklist = [user["rank"] for user in data]
    return ranklist

def getUserEmbed(handle: str, dischand: str):
    data = getUserData([handle])[0]

    obj = Embed(title = dischand, color=rankcolor[data["rank"]], description=data["rank"].title())
    obj.set_thumbnail(url=data["titlePhoto"])
    if "firstName" in data and "lastName" in data:
        if data["firstName"] != "" and data["lastName"] != "":
            obj.add_field("Name", data["firstName"] + " " + data["lastName"])

    fields = [
        "handle"
        "country",
        "city",
        "organization",
        "rating"
    ]
    for field in fields:
        if field in data:
            if data[field] != "":
                obj.add_field(field.title(), data[field])
    return obj