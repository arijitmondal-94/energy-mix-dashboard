import json
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from api_requests.carbon_intensity_requests import GenerationMixAPI
from api_requests.dto import GenerationMixDTO

TEST_FILE_PATH = "test/data/generation_mix.json"


def get_test_data():
    f = open(TEST_FILE_PATH)
    return json.load(f)['data']


@pytest.mark.skip(reason="no way of currently testing this")    
def test_current_generation_mix():
    expected = GenerationMixDTO.model_validate(get_test_data())
    generation_mix = GenerationMixAPI()
    observed = generation_mix.get_generation_mix_current()
    assert observed == expected
    
def test_generation_mix_between_period():
    from_ = datetime(2023, 9, 17, 10, tzinfo=ZoneInfo('Europe/London'))
    to_ = datetime(2023, 9, 17, 12, tzinfo=ZoneInfo('Europe/London'))
    expected = [GenerationMixDTO.model_validate(mix) for mix in get_test_data()]
    generation_mix = GenerationMixAPI()
    observed = generation_mix.get_generation_mix_between_period(from_, to_)
    assert observed == expected