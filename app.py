import json
import os
from typing import List

import numpy as np
from fastapi import UploadFile, File, FastAPI, Form
from pydantic import BaseModel
import utils

app = FastAPI(dependencies=[], debug=True)

class Champion(BaseModel):
    level:int
    name:str


class SuggestRequest(BaseModel):
    comp : List[Champion]

with open("winner_comps.json") as fp:
    winner_comps = json.load(fp)

all_winner_comps = np.array([comp_array for comp_array,_ in winner_comps])


class SuggestResponse(BaseModel):
    comp_key : str
    items: List[str]


@app.post("/suggest")
async def get_suggest(suggest_request : SuggestRequest):

    comp = suggest_request.comp
    comp_array = utils.get_comp_array(comp)
    arr = np.array(comp_array)

    argmax = np.abs(all_winner_comps-arr).sum(axis=1).argmin()
    comp_key = winner_comps[argmax][1]