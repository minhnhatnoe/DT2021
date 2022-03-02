from src.imports import *
rankcolor = {
    "unrated": 0x000000,
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

class UserFuncs:
    def add_to_update(guildid: str, userid: str):
        '''Add user to update list'''
        guildid = str(guildid)
        userid = str(userid)

        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\update.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            if guildid not in json_data:
                json_data[str(guildid)] = []
            json_data[guildid].append(userid)
            json.dump(json_data, json_file)
            json_file.truncate()


class GuildFuncs:
    async def make_roles(guild):
        rolelist = {}
        for rank, color in reversed(list(rankcolor.items())):
            role = await guild.create_role(name=rank, color=color, hoist=True)
            rolelist[rank] = role.id
        GuildFuncs.add_roles(guild.id, rolelist)
    
    def get_update_list(guildid: str):
        '''Get user update list in a guild'''
        guildid = str(guildid)
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\update.json", "r") as json_file:
            json_data = json.load(json_file)
            return json_data[guildid]

    def add_roles(guildid: str, rolelist: dict):
        '''Record role ids of a guild'''
        guildid = str(guildid)
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data[guildid] = rolelist
            json.dump(json_data, json_file)
            json_file.truncate()

    def get_roles(guildid: str):
        '''Get role ids of a guild'''
        guildid = str(guildid)
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r") as json_file:
            json_data = json.load(json_file)
            if guildid in json_data:
                return json_data[guildid]
            else:
                return None

    def remove_guild(guildid: str):
        '''Delete data abt a guild'''
        guildid = str(guildid)
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\role.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            if str(guildid) in json_data:
                json_data.pop(str(guildid))
            json.dump(json_data, json_file)
            json_file.truncate()

        with open(f"{path}\\update.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            if str(guildid) in json_data:
                json_data.pop(str(guildid))
            json.dump(json_data, json_file)
            json_file.truncate()


class CFInternal:
    def assign_handle(userid: str, handle: str):
        '''Assign CF handle to user'''
        userid = str(userid)
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\handle.json", "r+") as json_file:
            json_data = json.load(json_file)
            json_file.seek(0)
            json_data[userid] = handle
            json.dump(json_data, json_file)
            json_file.truncate()

    def get_handle(userid: str):
        '''Query a CF handle of someone'''
        userid = str(userid)
        load_dotenv()
        path = environ.get("DATAPATH")
        with open(f"{path}\\handle.json", "r") as json_file:
            json_data = json.load(json_file)
            if userid in json_data:
                return json_data[userid]
            else:
                return None


class CFExternal:
    async def get_user_data(userlist):
        '''Get user data abt someone from CF'''
        try:
            # fromnet = rqget(f"https://codeforces.com/api/user.info?handles={';'.join(userlist)}").text
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://codeforces.com/api/user.info?handles={';'.join(userlist)}") as response:
                    fromnet = await response.text()
        except:
            raise("Network Error")

        json_data = json.loads(fromnet)
        if json_data["status"] == "FAILED":
            raise Exception("Handle Error")
        return json_data["result"]

    async def get_roles(userlist):
        '''Get role of someone based on their CF ranking'''
        data = await CFExternal.get_user_data(userlist)
        ranklist = [user["rank"] for user in data]
        return ranklist

    async def get_user_embed(handle: str, dischand: str):
        '''Create an embed that represent a user'''
        data = await CFExternal.get_user_data([handle])
        data = data[0]
        if "rank" not in data:
            data["rank"] = "unrated"
        obj = Embed(
            title=dischand, color=rankcolor[data["rank"]], description=data["rank"].title())
        obj.set_thumbnail(url=data["titlePhoto"])
        if "firstName" in data and "lastName" in data:
            if data["firstName"] != "" and data["lastName"] != "":
                obj.add_field(
                    "Name", data["firstName"] + " " + data["lastName"])

        fields = [
            "handle",
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
