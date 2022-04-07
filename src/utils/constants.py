'''Commonly used constants'''
from src.platforms.codefun_external import CodeFun
from src.platforms.codechef_external import CodeChef
from src.platforms.codeforces_external import CodeForces

PLATFORM_CLASS = {
    1: CodeForces,
    2: CodeChef,
    3: CodeFun
}

RANKCOLOR = {}
UPDATECHOICES = {"None": 0}

for platform in PLATFORM_CLASS.values():
    RANKCOLOR |= platform.RANKCOLOR
    UPDATECHOICES |= platform.PLATFORM_CODE

UPDATECHOICELIST = [name for name in UPDATECHOICES if name != "None"]

PLATFORMIDS = [handle_type for handle_type in UPDATECHOICES.values()
               if handle_type != 0]
