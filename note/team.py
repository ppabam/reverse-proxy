import random
import pprint

names = [
    "조민규", "강현룡", "권오준", "서민혁", 
    "백지원", "안재영", "전희진", "배형균", "조성근"
]

random.shuffle(names)

teams = {
    "Team 1" : names[0:3],
    "Team 2" : names[3:6],
    "Team 3" : names[6:9],
}

pprint.pp(teams)