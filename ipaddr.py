import re

import requests


IP_ADDR = re.compile(r'^([0-9]+\.){3}[0-9]+$')

URL = 'https://api.ipify.org'


def get_current_ipaddr() -> str:
    """Retrieves the current public IP address using ipify.

    Returns:
        str: the IP address

    Raises:
        APIResponseError: if an invalid response was detected

    """
    response = requests.get(URL).text
    if IP_ADDR.match(response):
        return response
    else:
        raise APIResponseError(response)


class APIResponseError(ValueError):
    """The *ipify* API did not return a valid IP address."""
    def __init__(self, response) -> None:
        super().__init__(
            f'{URL} did not return a valid IP address. '
            f'Response: {response}'
            )
