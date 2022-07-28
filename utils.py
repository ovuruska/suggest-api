import json
from copy import deepcopy

number_of_clones = {
    1:1,
    2:3,
    3:9
}

with open("champion_metadata.json") as fp:
    champions = json.load(fp)

all_champions = {
    champions[key]["name"]:0   for key in champions.keys()
}


def get_comp_array_from_comp_key(comp_key):
    ...


def get_comp_array(comp_data):

    comp_data = list(map(lambda champion: {
        "key": [key for key in champions.keys() if champions[key]["name"] == champion.name][0],
        "level": champion.level,
        "name": champion.name,

    },comp_data))

    comp_data = list(map(lambda champion: {
        "name": champion["name"],
        "level": champion["level"],
        "key": champion["key"],
        "total_cost": number_of_clones[champion["level"]] * champions[champion["key"]]["cost"]

    }, comp_data))
    comp_champs = deepcopy(all_champions)
    for champion in comp_data:
        comp_champs[champion["name"]] = max(comp_champs[champion["name"]], champion["total_cost"])

    return list(comp_champs.values())
