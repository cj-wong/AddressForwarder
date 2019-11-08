import re

import requests


IPADDR = re.compile('([0-9]+\.){3}[0-9]+')


def get_current_ipaddr() -> str:
    """Retrieves the current public IP address using ipify.

    Returns:
        str: the IP address

    Raises:
        APIResponseError: if an invalid response was detected

    """
    response = requests.get('https://api.ipify.org').text
    if IPADDR.match(response):
        return response
    else:
        raise APIResponseError(response)


class Error(Exception):
    """Base error class for ipaddr.py"""
    pass


class APIResponseError(Error):
    """The *ipify* API did not return a valid IP address."""
    def __init__(self, response):
        super().__init__(
            'The *ipify* API did not return a valid IP address. '
            f'Response: {response}'
            )
