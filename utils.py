import json
from copy import deepcopy

number_of_clones = {
    1:1,
    2:3,
    3:9
}

with open("champion_metadata.json") as fp:
    champions = json.load(fp)

champions_by_name = {
    value["name"]:value for key,value in champions.items()
}

all_champions = {
    champions[key]["name"]:0   for key in champions.keys()
}

champion_names = list(all_champions.keys())


def get_champion_difference(current:[int],target:[int]):

    out = []
    for ind,(current_champ,target_champ) in enumerate(zip(current,target)):
        if target_champ > current_champ:
            champ_name = champion_names[ind]
            champion_cost = champions_by_name[champ_name]["cost"]
            number_of_clones = target_champ / champion_cost
            if number_of_clones == 9:
                tier = 3
            elif number_of_clones == 3:
                tier = 2
            else:
                tier = 1

            out.append({
                "name": champ_name,
                "tier": tier,
            })

        if current_champ > 0 and  target_champ == 0:
            champ_name = champion_names[ind]
            out.append({
                "name": champ_name,
                "tier": -1,
            })

    return list(sorted(out,key=lambda champion:champions_by_name[champ_name]["cost"]))[:3]

def get_comp_array_from_comp_key(comp_key):
    ...


def get_comp_array(comp_data):

    comp_data = list(map(lambda champion: {
        "key": [key for key in champions.keys() if champions[key]["name"] == champion.name][0],
        "tier": champion.tier,
        "name": champion.name,

    },comp_data))

    comp_data = list(map(lambda champion: {
        "name": champion["name"],
        "tier": champion["tier"],
        "key": champion["key"],
        "total_cost": number_of_clones[champion["tier"]] * champions[champion["key"]]["cost"]

    }, comp_data))
    comp_champs = deepcopy(all_champions)
    for champion in comp_data:
        comp_champs[champion["name"]] = max(comp_champs[champion["name"]], champion["total_cost"])

    return list(comp_champs.values())
