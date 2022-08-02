from fastapi import FastAPI
import pandas as pd

from db import get_best_augments, get_best_items, get_best_champions
from models import SuggestRequest

app = FastAPI(dependencies=[], debug=True)

augments_data = pd.read_csv("augments.csv")
items_data = pd.read_csv("items.csv")
champions_data = pd.read_csv("champions.csv")


@app.post("/champions")
async def get_champions(request: SuggestRequest):
    return {
        "champions": get_best_champions(request)
    }


@app.post("/items")
def get_items(request: SuggestRequest):
    return {
        "items": get_best_items(request)
    }


@app.post("/augments")
async def get_augments(request: SuggestRequest):
    return {
        "augments": get_best_augments(request)
    }


@app.post("/suggest")
async def get_suggest(request: SuggestRequest):
    return {
        "champions": get_best_champions(request),
        "items": get_best_items(request),
        "augments": get_best_augments(request)
    }
