import pytest
import requests_mock
from pydantic import ValidationError

from currencyetl import settings
from currencyetl.download import request_currency_rates
from currencyetl.response import Response


def test_request_currency_rates(mock_request_data_valid):
    with requests_mock.Mocker() as m:
        m.register_uri("GET", settings.API_URL, json=mock_request_data_valid)

        response = request_currency_rates()

        assert response.json() == Response(**mock_request_data_valid).json()
        assert isinstance(response, Response)
        assert all(
            [x in response.dict() for x in ["base", "rates", "date", "utc_created_at"]]
        )


def test_request_currency_rates_fails(mock_request_data_invalid):
    with pytest.raises(ValidationError):
        with requests_mock.Mocker() as m:
            m.register_uri("GET", settings.API_URL, json=mock_request_data_invalid)
            response = request_currency_rates()
