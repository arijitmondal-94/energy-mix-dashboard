from datetime import datetime
from logging import getLogger
from pathlib import Path
from api_requests.elexon.bm_prices import BalancingPrice
from typing import List
import json


logger = getLogger(__name__)

TEST_DATA_PATH = "test/data/bm_prices.json"

bm_price = BalancingPrice()

def load_expected_data() -> List[dict]:
    expected_data_path = Path(TEST_DATA_PATH)
    if expected_data_path.exists():
        with open(expected_data_path, 'r') as fp:
            data = json.load(fp)
            return data["expected_data"]
    logger.error(f"Test data path: {expected_data_path} invalid")
    


def test_bm_prices_day_period() -> None:
    expected_data = load_expected_data()[11]
    dt = datetime(2024, 4, 10, 6, 0)
    observed_data = bm_price.settelement_prices_day_period(dt)
    assert observed_data.dict() == expected_data


def test_bm_prices_day() -> None:
    expected_data = load_expected_data()
    dt = datetime(2024, 4, 10)
    observed_data = bm_price.settelement_prices_day(dt)
    assert [ob.dict() for ob in observed_data] == expected_data
