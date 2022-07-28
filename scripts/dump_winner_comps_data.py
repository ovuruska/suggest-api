import glob
import os
import json
from copy import deepcopy

from pymongo import MongoClient
from tqdm import tqdm

if __name__ == "__main__":

    files = glob.glob(os.path.join("winner_comps", "*.json"))

    filter_list = [
        "TFT7_TrainerDragon",
    ]

    with open("../champion_metadata.json") as fp:
        champions = json.load(fp)

    all_champions = {
        champions[key]["name"]:0   for key in champions.keys()
    }
    number_of_clones = {
        1:1,
        2:3,
        3:9
    }



    out_json = []
    for file_path in tqdm(files,desc="Uploading comp data"):
        comp_basename = os.path.basename(file_path)
        comp_key,_ = os.path.splitext(comp_basename)
        comp_data = json.loads(comp_key)
        comp_data = list(filter(lambda x:x[:-1] not in filter_list,comp_data))

        comp_data = list(sorted(comp_data,key=lambda x:champions[x[:-1]]["cost"]))
        comp_data = list(map(lambda x:{
            "name":champions[x[:-1]]["name"],
            "level":int(x[-1]),
            "total_cost":number_of_clones[int(x[-1])] * champions[x[:-1]]["cost"]
        }, comp_data))
        comp_champs = deepcopy(all_champions)
        for champion in comp_data:
            comp_champs[champion["name"]] = max(comp_champs[champion["name"]],champion["total_cost"])

        out_json.append([list(comp_champs.values()),comp_key])

    with open("../winner_comps.json", "w") as fp:
        json.dump(out_json,fp)