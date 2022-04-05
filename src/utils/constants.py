'''Commonly used constants'''
RANKCOLOR = {
    "Codechef 0*": 0x000000,
    "Codechef 1*": 0x000000,
    "Codechef 2*": 0x000000,
    "Codechef 3*": 0x000000,
    "Codechef 4*": 0x000000,
    "Codechef 5*": 0x000000,
    "Codechef 6*": 0x000000,
    "Codechef 7*": 0x000000,
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

UPDATECHOICES = {
    "None": 0,
    "Codeforces": 1,
    "Codechef": 2
}

UPDATECHOICELIST = [name for name in UPDATECHOICES if name != "None"]
