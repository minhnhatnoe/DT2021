'''Commonly used constants'''
from src.platforms.codefun_external import CodeFun
from src.platforms.codechef_external import CodeChef
from src.platforms.codeforces_external import CodeForces

PLATFORM_CLASS = {
    1: CodeForces,
    2: CodeChef,
    4: CodeFun
}

RANKCOLOR = {}
UPDATECHOICES = {"None": 0}
HANDLE_FILES = {}

for platform_id, platform in PLATFORM_CLASS.items():
    RANKCOLOR |= platform.RANKCOLOR
    UPDATECHOICES[platform.PLATFORM_NAME] = platform_id
    HANDLE_FILES[platform_id] = platform.HANDLE_FILE_NAME

UPDATECHOICELIST = [name for name in UPDATECHOICES if name != "None"]

PLATFORMIDS = [handle_type for handle_type in UPDATECHOICES.values()
               if handle_type != 0]
