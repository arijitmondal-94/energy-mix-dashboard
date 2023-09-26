from app.api_requests.dto import GenerationMixDTO
from app.api_requests.carbon_intensity_requests import GenerationMixAPI
import pandas as pd
from dateutil.relativedelta import relativedelta
from logging import getLogger
from typing import List

logger = getLogger(__name__)

class GenerationMixService(object):
    gen_mix_api = GenerationMixAPI()
    
    @classmethod
    def aggregate_months_generation_mix(cls, generation_mix_list: List[GenerationMixDTO]) -> GenerationMixDTO:
        for mix in generation_mix_list:
            mix.generationmix
    
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
        months_generation_mix = cls.aggregate_months_generation_mix(isp_generation_mix)
        return months_generation_mix
        