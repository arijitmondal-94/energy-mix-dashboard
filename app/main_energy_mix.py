from logging import getLogger
from app.api_requests.carbon_intensity_requests import GenerationMixAPI
from datetime import datetime
from zoneinfo import ZoneInfo
from services.plots import generate_donut
from pathlib import Path


logger = getLogger(__name__)

def main():
    from_ = datetime(2023, 9, 17, 10, tzinfo=ZoneInfo('Europe/London'))
    to_ = datetime(2023, 9, 17, 12, tzinfo=ZoneInfo('Europe/London'))
    generation_mix = GenerationMixAPI()
    mix = generation_mix.get_generation_mix_current()
    # mix = generation_mix.get_generation_mix_between_period(from_, to_)
    generate_donut(mix, Path('./images'), 'donut')

if __name__ == '__main__':
    main()