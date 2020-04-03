import requests_mock
from click.testing import CliRunner

from currencyetl import cli
from currencyetl import settings


def test_cli_help():
    runner = CliRunner()

    result = runner.invoke(cli.cli, "--help")

    assert result.exit_code == 0


def test_start_help():
    runner = CliRunner()

    result = runner.invoke(cli.cli, "start --help")

    assert result.exit_code == 0


def test_main(tmpdir, monkeypatch, mock_request_data_valid):

    with requests_mock.Mocker() as m:
        m.register_uri("GET", settings.API_URL, json=mock_request_data_valid)

        file = tmpdir.join("output.csv")
        cli.main(timeout=1, output_file=file)
