import pytest
import requests_mock
from pydantic import ValidationError

from currencyetl import settings
from currencyetl.methods import request_conversion_rates
from currencyetl.models import ConversionRates


def test_request_conversion_rates(mock_request_data_valid):
    with requests_mock.Mocker() as m:
        m.register_uri("GET", settings.API_URL, json=mock_request_data_valid)

        response = request_conversion_rates()

        assert all(
            [x in response.dict() for x in ["base", "rates", "date", "utc_created_at"]]
        )
        assert response.json() == ConversionRates(**mock_request_data_valid).json()


def test_request_conversion_rates_fails(mock_request_data_invalid):
    with pytest.raises(ValidationError):
        with requests_mock.Mocker() as m:
            m.register_uri("GET", settings.API_URL, json=mock_request_data_invalid)
            response = request_conversion_rates()
