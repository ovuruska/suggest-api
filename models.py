from typing import List
from pydantic import BaseModel


class Champion(BaseModel):
    tier: int
    name: str


class ItemOwnership(BaseModel):
    name: str
    champion: str


class SuggestRequest(BaseModel):
    comp: List[Champion]
    items: List[ItemOwnership]
    augments: List[str]


class SuggestResponse(BaseModel):
    comp_key: str
    champions: List[Champion]
