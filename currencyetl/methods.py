import csv
from os import path

import requests

from currencyetl import settings
from currencyetl.models import ConversionRates


def request_conversion_rates(
    api_url: str = settings.API_URL, timeout: int = 1
) -> ConversionRates:
    """ Request currency rates from settings.API_URL

        Request currency rates from settings.API_URL and unpack
        the resulting response.json() into a ConversionRates() object
        for validation

        Arguments:
            api_url (str): API url eg. https://exchangeratesapi.io/
                defaults to settings.API_URL
            timeout (int): request timeout in seconds, defaults to 1

        Returns:
            Response
    """

    response = requests.get(api_url, timeout=timeout)
    conversion_rates = ConversionRates(**response.json())

    return conversion_rates


def output_file_exists(filename: str) -> bool:
    """Check if filename exists

        Argument:
                filename (str): filename to check
        Returns:
                bool
    """
    return path.exists(filename)


def create_fieldnames(conversion_rates: ConversionRates) -> list:
    """ Create a list of fieldnames for a csv header

        Arguments:
            conversion_rates (ConversionRates)

        Returns:
            list
    """
    fieldnames = [
        key for key in conversion_rates.dict().keys() if key != "rates"
    ] + list(conversion_rates.rates.dict().keys())

    return fieldnames


def create_outputfile(filename: str, conversion_rates: ConversionRates) -> None:
    """ Create an output file to store conversion rates in.

        Arguments:
            filename (str): name of the file
            conversion_rates (ConversionRates): requested conversion rates

        Returns:
            None
    """
    with open(filename, "w") as output:
        fieldnames = create_fieldnames(conversion_rates=conversion_rates)
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=",")
        writer.writeheader()


def write_conversion_rates_to_csv(
    conversion_rates: ConversionRates, output_file: str = "output.csv"
) -> None:

    """ Write conversion rates to file

        If file does not exist, calls create_outputfile() to create it.
        Then opens the output file as a contextmanager and appends
        most recent rates.

        Arguments:
            output_file (str): name of the csv file
            conversion_rates (ConversionRates): requested conversion rates

        Returns:
            None
    """

    if not output_file_exists(output_file):
        create_outputfile(conversion_rates=conversion_rates, filename=output_file)

    with open(output_file, "a") as output:
        fieldnames = create_fieldnames(conversion_rates=conversion_rates)
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=",")
        writer.writerow(
            {
                "utc_created_at": conversion_rates.utc_created_at,
                "base": conversion_rates.base,
                "date": conversion_rates.date,
                **conversion_rates.rates.dict(),
            }
        )
