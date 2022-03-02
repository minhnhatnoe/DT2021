from include import *

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

async def makeroles(guild):
    rolelist = {}
    for rank, color in rankcolor.items():
        role = await guild.create_role(name=rank, color=color, hoist = True)
        rolelist[rank] = role.id
    JsonHandler.add_roles(guild.id, rolelist)