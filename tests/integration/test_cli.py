import csv
import time
from os import path

import requests_mock
import schedule
from click.testing import CliRunner

from currencyetl import cli
from currencyetl import settings


def test_start(monkeypatch, mock_request_data_valid):
    class MockEvery(object):
        def __init__(self, num: int):
            self.minutes = MockMinutes()

    class MockMinutes(object):
        def __init__(self):
            pass

        def do(self, func, *args, **kwargs) -> bool:
            return True

    def mock_every(num: int):
        return MockEvery(num)

    def mock_run_pending():
        cli.main(timeout=settings.REQUEST_TIMEOUT, output_file=settings.OUTPUT_FILE)

    def mock_time_sleep(num: int) -> None:
        exit()

    monkeypatch.setattr(schedule, "run_pending", mock_run_pending)
    monkeypatch.setattr(schedule, "every", mock_every)
    monkeypatch.setattr(time, "sleep", mock_time_sleep)

    runner = CliRunner()

    # mock requests to return mock_request_data_valid
    with requests_mock.Mocker() as m:
        m.register_uri("GET", settings.API_URL, json=mock_request_data_valid)

        with runner.isolated_filesystem():

            # invoke cli and check if output and exit code are ok
            result = runner.invoke(cli.cli, ["start", "--logfile"])
            assert "Initializing cronjob" in result.output
            assert result.exit_code == 0

            # check if output exists
            assert path.exists(settings.OUTPUT_FILE)
            assert path.exists("file.log")

            # read output and check its length
            csv_file = open(settings.OUTPUT_FILE)
            reader = csv.reader(csv_file)
            assert len(list(reader)) == 2

            # invoke again to check if properly appending results
            result = runner.invoke(cli.cli, ["start", "--logfile"])
            csv_file = open(settings.OUTPUT_FILE)
            reader = csv.reader(csv_file)

            assert len(list(reader)) == 3
