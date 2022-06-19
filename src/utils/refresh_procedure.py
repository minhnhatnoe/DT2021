'''Procedure for all role refresh'''
from datetime import datetime
from typing import Dict, List
from src.utils.platform_class import PLATFORM_CLASS, PLATFORMIDS, UPDATECHOICES
from src.utils import user_functions, handle_functions, guild_functions, \
    json_file


async def refresh_roles_of_bot() -> None:
    '''Refresh all roles in all guilds'''
    change_queries = await create_refresh_job_list()
    handle_functions.write_handle_attr_to_dict(change_queries)

    # Get role to change of queries
    for platform in PLATFORMIDS:
        await write_role_attr_to_dict(change_queries[platform], platform)
        for (user, _), user_data in change_queries[platform].items():
            if "role" in user_data:
                role = user_data["role"]
                await user_functions.member_assign_role(user, [role])
    print("Refreshed all guilds on: ", datetime.now())


async def create_refresh_job_list() -> Dict:
    '''Returns a dict of jobs'''
    task_list = json_file.load_from_json("/update")
    configs = json_file.load_from_json("/server_config")

    # Some sets of disnake.user - guild/handle/role pairs
    change_queries = {key: {} for key in UPDATECHOICES.values()}

    # Get the list of users and partition them to the respective platform
    for guild_id, users in task_list.items():
        guild = await guild_functions.standardize_guild(guild_id) # TODO: Do not create roles for guilds that have disabled
        if guild is None: continue

        for user_id, user_choice in users.items():
            if user_choice == 0: continue
            platform_name = PLATFORM_CLASS[user_choice].PLATFORM_NAME
            if configs[str(guild_id)]["roles"][platform_name] is False:
                continue

            user = guild.get_member(int(user_id))
            if user is not None:
                change_queries[user_choice][(user, guild)] = {}

    return change_queries


async def write_role_attr_to_dict(platform_queries: Dict, platform: int) -> None:
    '''Recieves a dict of {(user, guild): {handle}}, add property role of disnake.Role.
    The key is user, guild for hashing'''
    handle_list = []
    for person_data in platform_queries.values():
        handle_list.append(person_data["handle"])

    ranks_dict = await generate_dict_of_rank(handle_list, platform)
    for (_, guild), person_data in platform_queries.items():
        handle = person_data["handle"].lower()
        role_name = ranks_dict[handle]
        person_data["role"] = \
            guild_functions.get_role_with_name(guild, role_name)


async def generate_dict_of_rank(user_list: List, handle_type: int) -> Dict:
    '''Generate a dict of handle-rank, accepting list of str only'''
    platform = PLATFORM_CLASS[handle_type]()
    return await platform.generate_dict_of_rank(user_list)
