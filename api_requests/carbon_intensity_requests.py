import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import requests
from typing import Optional
from logging import getLogger
from api_requests.dto import GenerationMixDTO, CO2IntensityDTO


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
        self.regions = self.__load_regions_config(
            Path("data/gb_regions.json"))

    def __load_regions_config(self, path: Path) -> dict:
        if path.exists():
            logger.debug(f'{path} exists. Loading Regions data')
            with open(path, 'r') as f:
                data = json.load(f)
            return data
        else:
            logger.error(f"Unable to load Region data. {path} Invalid")
            return None


class CO2IntensityRegionalAPI(CarbonIntensity):

    def __init__(self) -> None:
        super().__init__()
        self.endpoint = f"{self.base_url}regional/intensity"

    def __get_request(self, url: Optional[str] = None, payload: Optional[dict] = None) -> dict:
        r = requests.get(url or self.endpoint,
                         params=payload, headers=self.headers)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise ValueError(
                f"Resrponse Code: {r.status_code}. Could not retrieve data for url {url}.")

    def get_regions(self):
        return self.regions

    def get_regional_co2_intensity_pt24h(self, region_id: dict, from_datetime: datetime) -> CO2IntensityDTO:
        url = f"{self.endpoint}/{from_datetime.strftime('%Y-%m-%dT%H:%MZ')}/pt24h/regionid/{region_id}"
        try:
            return CO2IntensityDTO.model_validate(self.__get_request(url))

        except ValueError as e:
            logger.error(f"{e}")

    def get_all_regional_co2_intensity_pt24h(self, from_datetime: datetime):
        pass

    def get_regional_co2_intensity_current_hh(self) -> CO2IntensityDTO:
        url = self.endpoint.removesuffix('intensity')
        try:
            return CO2IntensityDTO.model_validate(self.__get_request(url)[0])
        except ValueError as e:
            logger.error(f"{e}")

    def get_co2_intensity_pt24h(self, from_datetime: datetime):
        """_summary_

        Args:
            from_datetime (datetime): _description_

        Returns:
            _type_: _description_
        """
        url = f"{self.endpoint}/{from_datetime.strftime('%Y-%m-%dT%H:%MZ')}/pt24h"
        try:
            return self.__get_request(url)
        except ValueError as e:
            logger.error(f"{e}")


class GenerationMixAPI(CarbonIntensity):
    """
    Implements Generation Mix APIs from Carbon Intensity 
    """

    def __init__(self) -> None:
        super().__init__()
        self.endpoint = self.base_url + 'generation/'

    def __get_request(self, url: Optional[str] = None, payload: Optional[dict] = None) -> dict:
        r = requests.get(url or self.endpoint,
                         params=payload, headers=self.headers)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise ValueError(
                f"Resrponse Code: {r.status_code}. Could not retrieve data for url {self.endpoint}.")

    def get_generation_mix_current(self) -> GenerationMixDTO:
        try:
            current_generation_mix = GenerationMixDTO.model_validate(
                self.__get_request())
            logger.debug(current_generation_mix)
        except ValueError as e:
            logger.error(
                f'Unable to get current genration mix')

        return current_generation_mix

    def get_generation_for_date(self, index_date: datetime) -> GenerationMixDTO:
        url = f'{self.endpoint}{index_date.strftime("%Y-%m-%dT%H:%MZ")}/pt24h'

        try:
            obj = self.__get_request(url)
            logger.debug(obj)
        except ValueError as e:
            logger.error(
                f'Unable to get current genration mix. {e} {url}')

        return [GenerationMixDTO.model_validate(mix) for mix in obj]

    def get_generation_mix_between_period(self, from_datetime: datetime, to_datetime: datetime) -> list[GenerationMixDTO]:
        url = self.endpoint + \
            from_datetime.strftime("%Y-%m-%dT%H:%MZ") + \
            '/' + to_datetime.strftime("%Y-%m-%dT%H:%MZ")
        try:
            return [GenerationMixDTO.model_validate(mix) for mix in self.__get_request(url)]
        except ValueError as e:
            logger.error(f"{e}")
