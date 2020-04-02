from contextlib import nullcontext

import pytest
from pydantic import ValidationError

from currencyetl.models import ConversionRates
from currencyetl.models import Rates


valid_rates = {
    "HKD": 7.7532858708,
    "ISK": 142.0226359985,
    "PHP": 50.9903249361,
    "DKK": 6.8158086893,
    "HUF": 328.6053304126,
    "CZK": 24.9288061336,
    "GBP": 0.8090817817,
    "RON": 4.4069916028,
    "SEK": 10.0961117196,
    "IDR": 16310.0036509675,
    "INR": 75.6649324571,
    "BRL": 5.2027199708,
    "RUB": 78.4488864549,
    "HRK": 6.96011318,
    "JPY": 108.5250091274,
    "THB": 32.7902519168,
    "CHF": 0.9661372764,
    "EUR": 0.9127418766,
    "MYR": 4.3200073019,
    "BGN": 1.7851405622,
    "TRY": 6.5774917853,
    "CNY": 7.0996714129,
    "NOK": 10.5056589996,
    "NZD": 1.6809967141,
    "ZAR": 17.8984118291,
    "USD": 1.0,
    "MXN": 23.8930266521,
    "SGD": 1.4268893757,
    "AUD": 1.6399233297,
    "ILS": 3.5613362541,
    "KRW": 1224.0142387733,
    "PLN": 4.1535231836,
}

invalid_rates = {
    "HKD": 7.7532858708,
    "ISK": 142.0226359985,
    "PHP": "Test",
    "DKK": 6.8158086893,
    "HUF": 328.6053304126,
    "CZK": 24.9288061336,
    "GBP": 0.8090817817,
    "RON": 4.4069916028,
    "SEK": 10.0961117196,
    "IDR": 16310.0036509675,
    "INR": 75.6649324571,
    "BRL": 5.2027199708,
    "RUB": 78.4488864549,
    "HRK": 6.96011318,
    "JPY": 108.5250091274,
    "THB": 32.7902519168,
    "CHF": 0.9661372764,
    "EUR": -0.9127418766,
    "MYR": 4.3200073019,
    "BGN": 1.7851405622,
    "TRY": 6.5774917853,
    "CNY": 7.0996714129,
    "NOK": 10.5056589996,
    "NZD": 1.6809967141,
    "ZAR": "Test",
    "USD": 1.0,
    "MXN": 23.8930266521,
    "SGD": 1.4268893757,
    "AUD": 1.6399233297,
    "ILS": 3.5613362541,
    "KRW": 1224.0142387733,
    "PLN": 4.1535231836,
}


@pytest.mark.parametrize(
    "data, expectation",
    [
        pytest.param(valid_rates, nullcontext(), id="valid_input"),
        pytest.param(invalid_rates, pytest.raises(ValidationError), id="invalid_input"),
    ],
)
def test_rates_model(data, expectation):
    with expectation:
        currency_rates = Rates(**data)


@pytest.mark.parametrize(
    "data, expectation",
    [
        pytest.param(
            {"rates": valid_rates, "base": "USD", "date": "2019-03-31"},
            nullcontext(),
            id="valid_response",
        ),
        pytest.param(
            {"rates": valid_rates, "base": 1, "date": "2019-03-31"},
            pytest.raises(ValidationError),
            id="invalid_response1",
        ),
        pytest.param(
            {"rates": valid_rates, "base": "USD", "date": 1},
            pytest.raises(ValidationError),
            id="invalid_response2",
        ),
    ],
)
def test_conversion_rate_model(data, expectation):
    with expectation:
        response = ConversionRates(**data)
