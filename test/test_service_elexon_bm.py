import pytest
from services.analytics import ElexonBMPricesService

bm_prices = ElexonBMPricesService()

@pytest.skip("This is to check the service data flow")
def test_elexon_bm_current_day() -> None:
    data = bm_prices.settlement_prices_current_day()
    data