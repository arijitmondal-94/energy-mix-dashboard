from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field


class FuelType(BaseModel):
    fuel: str
    perc: float


class GenerationMixDTO(BaseModel):
    from_: str = Field(..., alias='from')
    to: str
    generationmix: List[FuelType]
