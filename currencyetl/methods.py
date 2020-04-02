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
            api_url (str): API url eg. https://exchangeratesapi.io/ defaults to settings.API_URL
            timeout (int): request timeout in seconds, defaults to 1

        Returns:
            Response
    """

    response = requests.get(api_url, timeout=timeout)
    conversion_rates = ConversionRates(**response.json())

    return conversion_rates
