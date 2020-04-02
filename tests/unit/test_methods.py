import csv
from os import path

import pytest
import requests_mock
from pydantic import ValidationError

from currencyetl import settings
from currencyetl.methods import create_fieldnames
from currencyetl.methods import create_outputfile
from currencyetl.methods import output_file_exists
from currencyetl.methods import request_conversion_rates
from currencyetl.methods import write_conversion_rates_to_csv
from currencyetl.models import ConversionRates


def test_request_conversion_rates(mock_request_data_valid):
    with requests_mock.Mocker() as m:
        m.register_uri("GET", settings.API_URL, json=mock_request_data_valid)

        response = request_conversion_rates()

        assert all(
            [x in response.dict() for x in ["base", "rates", "date", "utc_created_at"]]
        )
        assert isinstance(response, ConversionRates)


def test_request_conversion_rates_fails(mock_request_data_invalid):
    with pytest.raises(ValidationError):
        with requests_mock.Mocker() as m:
            m.register_uri("GET", settings.API_URL, json=mock_request_data_invalid)
            response = request_conversion_rates()


def test_output_file_exists_true(monkeypatch):
    def mock_path_exists(filename: str):
        return True

    monkeypatch.setattr(path, "exists", mock_path_exists)

    assert output_file_exists("test.csv") is True


def test_output_file_exists_false(monkeypatch):
    def mock_path_exists(filename: str):
        return False

    monkeypatch.setattr(path, "exists", mock_path_exists)

    assert output_file_exists("test.csv") is False


def test_create_fieldnames(mock_request_data_valid):
    conversion_rates = ConversionRates(**mock_request_data_valid)

    fieldnames = create_fieldnames(conversion_rates=conversion_rates)

    assert isinstance(fieldnames, list)
    assert all([field in fieldnames for field in conversion_rates.rates.dict().keys()])
    assert all([field in fieldnames for field in ["utc_created_at", "base", "date"]])


def test_create_outputfile(tmpdir, mock_conversion_rates):
    file = tmpdir.join("output.csv")
    create_outputfile(filename=file, conversion_rates=mock_conversion_rates)

    assert path.exists(file.strpath)
    assert (
        file.read()
        == ",".join(create_fieldnames(conversion_rates=mock_conversion_rates)) + "\n"
    )  # check if header is created properly


def test_write_conversion_rates_to_csv(tmpdir, mock_conversion_rates):
    file = tmpdir.join("output.csv")
    write_conversion_rates_to_csv(
        conversion_rates=mock_conversion_rates, output_file=file
    )

    csv_file = open(file)
    reader = csv.reader(csv_file)

    assert path.exists(file)
    assert len(list(reader)) == 2


def test_write_conversion_rates_to_csv_append(tmpdir, mock_request_data_valid):
    file = tmpdir.join("output.csv")
    rates1 = ConversionRates(**mock_request_data_valid)
    write_conversion_rates_to_csv(conversion_rates=rates1, output_file=file)
    rates2 = ConversionRates(**mock_request_data_valid)
    write_conversion_rates_to_csv(conversion_rates=rates2, output_file=file)

    csv_file = open(file)
    reader = csv.reader(csv_file)

    assert path.exists(file)
    assert len(list(reader)) == 3
