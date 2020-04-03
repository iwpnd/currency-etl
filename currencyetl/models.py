import datetime

from pydantic import BaseModel
from pydantic import confloat
from pydantic import StrictStr
from pydantic import validator


class Rates(BaseModel):
    """ Pydantic model to store conversion rates in
    """

    HKD: confloat(gt=0) = None
    ISK: confloat(gt=0) = None
    PHP: confloat(gt=0) = None
    DKK: confloat(gt=0) = None
    HUF: confloat(gt=0) = None
    CZK: confloat(gt=0) = None
    GBP: confloat(gt=0) = None
    RON: confloat(gt=0) = None
    SEK: confloat(gt=0) = None
    IDR: confloat(gt=0) = None
    INR: confloat(gt=0) = None
    BRL: confloat(gt=0) = None
    RUB: confloat(gt=0) = None
    HRK: confloat(gt=0) = None
    JPY: confloat(gt=0) = None
    THB: confloat(gt=0) = None
    CHF: confloat(gt=0) = None
    EUR: confloat(gt=0) = None
    MYR: confloat(gt=0) = None
    BGN: confloat(gt=0) = None
    TRY: confloat(gt=0) = None
    CNY: confloat(gt=0) = None
    NOK: confloat(gt=0) = None
    NZD: confloat(gt=0) = None
    ZAR: confloat(gt=0) = None
    USD: confloat(gt=0) = None
    MXN: confloat(gt=0) = None
    SGD: confloat(gt=0) = None
    AUD: confloat(gt=0) = None
    ILS: confloat(gt=0) = None
    KRW: confloat(gt=0) = None
    PLN: confloat(gt=0) = None


class ConversionRates(BaseModel):
    """ Pydantic model to store conversion rates
    """

    rates: Rates
    base: StrictStr = None
    date: StrictStr = None
    utc_created_at: StrictStr = None

    @validator("utc_created_at", pre=True, always=True)
    def set_utc_now(cls, v):
        return str(datetime.datetime.utcnow())
