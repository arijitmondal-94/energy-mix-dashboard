import pandas as pd
import json
from datetime import datetime
import requests
from typing import Optional
from logging import getLogger
from app.api_requests.dto import GenerationMixDTO


logger = getLogger('__name__')

class CarbonIntensity(object):
    """
    Base CarbonIntensity API Class with Base URL
    """
    def __init__(self) -> None:
        self.headers = {
              'Accept': 'application/json'
        }
        self.base_url: str = "https://api.carbonintensity.org.uk/"

class GenerationMix(CarbonIntensity):
    """
    Implements Generation Mix APIs from Carbon Intensity 
    """
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = self.base_url + 'generation/'
        
    def _get_request(self, url: Optional[str] = None, payload: Optional[dict] = None) -> dict:
        r = requests.get(url or self.endpoint, params=payload, headers=self.headers)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise ValueError(f"Resrponse Code: {r.status_code}. Could not retrieve data for url {self.endpoint}.")
    
    
    def get_generation_mix_current(self) -> GenerationMixDTO:
        try:
            current_generation_mix = GenerationMixDTO.model_validate(self._get_request())
            logger.debug(current_generation_mix)
        except ValueError as e:
            logger.error(f'Unable to get current egenration mix. {current_generation_mix}')
            
        return current_generation_mix
    
    def get_generation_mix_between_period(self, from_datetime: datetime, to_datetime: datetime) -> list[GenerationMixDTO]:
        url = self.endpoint + from_datetime.strftime("%Y-%m-%dT%H:%MZ") + '/' + to_datetime.strftime("%Y-%m-%dT%H:%MZ")
        try:
            return [GenerationMixDTO.model_validate(mix) for mix in self._get_request(url)]
        except ValueError as e:
            logger.error(f"{e}")