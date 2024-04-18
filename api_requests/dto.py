from typing import List
from pydantic import BaseModel, Field


class FuelType(BaseModel):
    fuel: str
    perc: float


class GenerationMixDTO(BaseModel):
    from_: str = Field(..., alias='from')
    to: str
    generationmix: List[FuelType]

class CO2Intensity(BaseModel):
    forecast: int
    index: str
    
class CO2Regions(BaseModel):
    regionid: int
    dnoregion: str
    shortname: str
    intensity: CO2Intensity
    generationmix: List[FuelType]
    

class CO2IntensityDTO(BaseModel):
    from_: str = Field(..., alias='from')
    to: str
    regions: List[CO2Regions]