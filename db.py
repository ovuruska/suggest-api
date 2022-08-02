from random import randint
import numpy as np
import pandas as pd
import json

import utils

augments_data = pd.read_csv("augments.csv")
items_data = pd.read_csv("items.csv")
champions_data = pd.read_csv("champions.csv")


with open("winner_comps.json") as fp:
    winner_comps = json.load(fp)


MAX_COMP_DISTANCE = lambda length:(12-length)*10



def get_points(placement):
    return randint((-placement + 4) * 7, (placement + 4) * 9)

champion_filter_list = [
    "TFT7_TrainerDragon",
]

filter_list = [
    "B.F. Sword",
    "Recurve Bow",
    "Needlessly Large Rod",
    "Tear of the Goddess",
    "Chain Vest",
    "Negatron Cloak",
    "Giant's Belt",
    "Spatula",
    "Sparring Gloves",
    "TFT_Item_MadredsBloodrazor"
]

def get_best_augments(request):
    augments = request.augments
    comp_array = utils.get_comp_array(request.comp)
    comp_size = len(request.comp)
    filtered_augments = augments_data[
        augments_data["comp"].apply(lambda x: sum([abs(i - j) for i, j in zip(json.loads(x), comp_array)])) < MAX_COMP_DISTANCE(comp_size)]

    analysis_results = {}
    for row in filtered_augments.itertuples():

        comp_worth = get_points(row.placement)
        name = row.name
        if name in augments:
            continue
        analysis_results[name] = analysis_results.get(name, 0) + comp_worth

    analysis_results = sorted(analysis_results.items(), key=lambda x: x[1], reverse=True)
    analysis_results  = [x[0] for x in analysis_results[:11]]
    return analysis_results

def get_best_items(request):
    items = request.items
    comp_array = utils.get_comp_array(request.comp)
    comp_size = len(request.comp)
    filtered_items = items_data[
        items_data["comp"].apply(lambda x: sum([abs(i - j) for i, j in zip(json.loads(x), comp_array)])) < MAX_COMP_DISTANCE(comp_size)]

    analysis_results = {}
    for row in filtered_items.itertuples():
        comp_worth = get_points(row.placement)
        champion = row.champion
        name = row.name
        if name in filter_list:
            continue
        key = json.dumps({
            "champion": champion,
            "name": name,
        }, sort_keys=True)

        analysis_results[key] = analysis_results.get(key, 0) + comp_worth

    for item in items:
        champion = item.champion
        name = item.name
        if name in filter_list:
            continue
        key = json.dumps({
            "champion": champion,
            "name": name,
        }, sort_keys=True)
        try:
            del analysis_results[key]
        except KeyError:
            continue

    analysis_results = sorted(analysis_results.items(), key=lambda x: x[1], reverse=True)
    analysis_results = [json.loads(x[0]) for x in analysis_results[:5]]

    return analysis_results

def get_best_champions(request):
    comp = request.comp

    comp_array = utils.get_comp_array(request.comp)
    comp_size = len(request.comp)
    filtered_champions = champions_data[
        champions_data["comp"].apply(lambda x: sum([abs(i - j) for i, j in zip(json.loads(x), comp_array)])) < MAX_COMP_DISTANCE(len(comp))]

    out_champions = dict()

    for row in filtered_champions.itertuples():
        comp_worth = get_points(row.placement)
        champion_name = row.name
        if champion_name in champion_filter_list:
            continue

        out_champions[champion_name] = out_champions.get(champion_name, 0) + comp_worth

    comp_champions = [champion.name for champion in comp]

    for champion in comp_champions:
        if champion in filter_list:
            continue
        try:
            del out_champions[champion]
        except KeyError:
            continue

    out_champions = sorted(out_champions.items(), key=lambda x: x[1], reverse=True)[:3]
    out_champions = list(map(lambda x:x[0],out_champions))
    return out_champions
