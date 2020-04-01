import requests

from currencyetl import settings
from currencyetl.response import Response


def request_currency_rates(
    api_url: str = settings.API_URL, timeout: int = 1
) -> Response:
    """ Request currency rates from settings.API_URL

        Request currency rates from settings.API_URL and unpack
        the resulting response.json() into a Response() object
        for validation

        Arguments:
            api_url (str): API url eg. https://exchangeratesapi.io/ defaults to settings.API_URL
            timeout (int): request timeout in seconds, defaults to 1

        Returns:
            Response
    """

    response = requests.get(api_url, timeout=timeout)

    return Response(**response.json())
