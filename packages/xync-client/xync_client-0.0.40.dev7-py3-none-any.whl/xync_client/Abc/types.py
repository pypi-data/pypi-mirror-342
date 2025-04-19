from pydantic import BaseModel, model_validator
from x_model.types import BaseUpd
from xync_schema.enums import PmType
from xync_schema.models import Country, Pm, Ex
from xync_schema.types import PmexBank

from xync_client.pm_unifier import PmUni


class PmTrait:
    typ: PmType | None = None
    logo: str | None = None
    banks: list[PmexBank] | None = None


class PmEx(BaseModel, PmTrait):
    exid: int | str
    name: str


class PmIn(BaseUpd, PmUni, PmTrait):
    _unq = "norm", "country"
    country: Country | None = None

    class Config:
        arbitrary_types_allowed = True


class PmExIn(BaseModel):
    pm: Pm
    ex: Ex
    exid: int | str
    name: str

    class Config:
        arbitrary_types_allowed = True


class CredExOut(BaseModel):
    id: int


class BaseOrderReq(BaseModel):
    ad_id: int | str
    is_sell: bool
    asset_amount: float | None = None
    fiat_amount: float | None = None
    cred_id: int
    # todo: if is not sell, it can be just pmcur_id

    @model_validator(mode="after")
    def check_a_or_b(self):
        if not self.asset_amount and not self.fiat_amount:
            raise ValueError("either fiat_amount or asset_amount is required")
        return self


class BaseAdUpdate(BaseModel):
    id: int | str
