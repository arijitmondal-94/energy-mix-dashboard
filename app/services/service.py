from app.api_requests.dto import FuelType, GenerationMixDTO
from app.api_requests.carbon_intensity_requests import GenerationMixAPI
import pandas as pd
from dateutil.relativedelta import relativedelta
from logging import getLogger
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
            to_ = pd.Timestamp(current_date - relativedelta(days=current_date.day - 1))
            from_ = to_ - relativedelta(days=to_.daysinmonth + 1)
            logger.debug(f'Getting Generation Mix Data between {from_} - {to_}')
        isp_generation_mix = cls.gen_mix_api.get_generation_mix_between_period(from_, to_)
        months_generation_mix = cls._aggregate_months_generation_mix(isp_generation_mix)
        return months_generation_mix
        