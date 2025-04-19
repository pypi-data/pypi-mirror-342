from typing import Literal

from pydantic import BaseModel


class OrderRequest(BaseModel):
    itemId: str
    tokenId: str
    currencyId: str
    side: Literal["0", "1"]  # 0 покупка, 1 продажа
    quantity: str
    amount: str
    curPrice: str
    flag: str
    version: str
    securityRiskToken: str = ""
