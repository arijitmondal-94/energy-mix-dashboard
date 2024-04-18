from typing import Any, List, Optional

from pydantic import BaseModel


class Metadata(BaseModel):
    datasets: List[str]

class IndicativeImbalanceSettlement(BaseModel):
    settlementDate: str
    settlementPeriod: int
    startTime: str
    createdDateTime: str
    systemSellPrice: float
    systemBuyPrice: float
    bsadDefaulted: bool
    priceDerivationCode: str
    reserveScarcityPrice: int
    netImbalanceVolume: float
    sellPriceAdjustment: int
    buyPriceAdjustment: int
    replacementPrice: Any
    replacementPriceReferenceVolume: Any
    totalAcceptedOfferVolume: float
    totalAcceptedBidVolume: float
    totalAdjustmentSellVolume: float
    totalAdjustmentBuyVolume: float
    totalSystemTaggedAcceptedOfferVolume: float
    totalSystemTaggedAcceptedBidVolume: float
    totalSystemTaggedAdjustmentSellVolume: Any
    totalSystemTaggedAdjustmentBuyVolume: Any

