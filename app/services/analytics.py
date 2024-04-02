from api_requests.dto import FuelType, GenerationMixDTO, CO2Regions
from api_requests.carbon_intensity_requests import GenerationMixAPI
from api_requests.carbon_intensity_requests import CO2IntensityRegionalAPI
import pandas as pd
from dateutil.relativedelta import relativedelta
from logging import getLogger
from datetime import datetime
from typing import List

logger = getLogger(__name__)


class GenerationMixService(object):
    gen_mix_api = GenerationMixAPI()

    @classmethod
    def _aggregate_months_generation_mix(cls, generation_mix_list: List[GenerationMixDTO]) -> GenerationMixDTO:
        biomass, coal, imports, gas, nuclear, other, hydro, solar, wind = (
            FuelType(fuel='biomass', perc=0),
            FuelType(fuel='coal', perc=0),
            FuelType(fuel='imports', perc=0),
            FuelType(fuel='gas', perc=0),
            FuelType(fuel='nuclear', perc=0),
            FuelType(fuel='other', perc=0),
            FuelType(fuel='hydro', perc=0),
            FuelType(fuel='solar', perc=0),
            FuelType(fuel='wind', perc=0)
        )
        aggreagte_from = generation_mix_list[0].from_
        no_of_isp = len(generation_mix_list)
        for mix in generation_mix_list:
            aggregate_to = mix.to
            for fuel in mix.generationmix:
                if fuel.fuel == 'biomass':
                    biomass.perc += fuel.perc
                elif fuel.fuel == 'coal':
                    coal.perc += fuel.perc
                elif fuel.fuel == 'imports':
                    imports.perc += fuel.perc
                elif fuel.fuel == 'gas':
                    gas.perc += fuel.perc
                elif fuel.fuel == 'nuclear':
                    nuclear.perc += fuel.perc
                elif fuel.fuel == 'other':
                    other.perc += fuel.perc
                elif fuel.fuel == 'hydro':
                    hydro.perc += fuel.perc
                elif fuel.fuel == 'solar':
                    solar.perc += fuel.perc
                elif fuel.fuel == 'wind':
                    wind.perc += fuel.perc
        for mix in [biomass, coal, imports, gas, nuclear, other, hydro, solar, wind]:
            mix.perc = mix.perc / no_of_isp
        return GenerationMixDTO.model_validate(
            {
                'from': aggreagte_from,
                'to': aggregate_to,
                'generationmix': [biomass, coal, imports, gas, nuclear, other, hydro, solar, wind]
            }
        )

    @classmethod
    def get_last_months_energy_mix(cls) -> GenerationMixDTO:
        """function determines last full month and gets the generation mix data from carbon intensity apis

        Returns:
            GenerationMixDTO: _description_
        """
        current_date = pd.Timestamp.now('Europe/London').normalize()
        if not current_date.is_month_end:
            to_ = pd.Timestamp(
                current_date - relativedelta(days=current_date.day - 1))
            from_ = to_ - relativedelta(days=to_.daysinmonth + 1)
            logger.debug(
                f'Getting Generation Mix Data between {from_} - {to_}')
        isp_generation_mix = cls.gen_mix_api.get_generation_mix_between_period(
            from_, to_)
        months_generation_mix = cls._aggregate_months_generation_mix(
            isp_generation_mix)
        return months_generation_mix

    @classmethod
    def get_generation_mix_selected_date(cls, index_date: datetime) -> GenerationMixDTO:
        """function determines last full month and gets the generation mix data from carbon intensity apis

        Returns:
            GenerationMixDTO: _description_
        """
        logger.debug(
            f'Getting Generation Mix Data for {index_date}')
        isp_generation_mix = cls.gen_mix_api.get_generation_for_date(
            index_date)
        aggragted_daily_mix = cls._aggregate_months_generation_mix(
            isp_generation_mix)
        return aggragted_daily_mix


class CO2IntensityServices(object):
    carbon_intensity_regional_api = CO2IntensityRegionalAPI()

    @classmethod
    def get_regions(cls) -> dict:
        return cls.carbon_intensity_regional_api.get_regions()['regions']

    @classmethod
    def get_daily_co2_intensity(cls, from_datetime: datetime):
        regional_co2_intensity = cls.carbon_intensity_regional_api.get_co2_intensity_pt24h(
            from_datetime)
        return regional_co2_intensity

    @classmethod
    def get_regional_co2_intensity(cls, from_datetime, region_id):
        regional_co2_intensity = cls.carbon_intensity_regional_api.get_regional_co2_intensity_pt24h(
            region_id['id'], from_datetime)
        return regional_co2_intensity

    @classmethod
    def get_current_regional_co2_intensity(cls) -> CO2Regions:
        co2_intensity = cls.carbon_intensity_regional_api.get_regional_co2_intensity_current_hh()
        return co2_intensity.regions
            
        
