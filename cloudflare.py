import sys
from typing import Dict, Union

import requests

import config


PARAMS = Dict[str, Union[bool, str]]
SUBDOMAINS = Dict[str, PARAMS]

URL = 'https://api.cloudflare.com/client/v4/zones'


class SubdomainIDAlreadySet(ValueError):
    """A value already exists in the subdomain attribute."""

    def __init__(self, subdomain: str) -> None:
        """Initialize the error with a message.

        Args:
            subdomain (str): subdomain of the domain

        """
        super().__init__(
            f'The ID field for {subdomain} already has a value. '
            'Delete the value if you want to re-run the function.'
            )


class NoRecords(ValueError):
    """No DNS records were found given a subdomain."""

    def __init__(self, subdomain: str) -> None:
        """Initialize the error with a message.

        Args:
            subdomain (str): subdomain of the domain

        """
        super().__init__(f'No subdomains were found matching {subdomain}.')


class TooManyRecords(ValueError):
    """Too many DNS records were found given a subdomain."""

    def __init__(self, subdomain: str) -> None:
        """Initialize the error with a message.

        Args:
            subdomain (str): subdomain of the domain

        """
        super().__init__(f'Too many DNS records were found for {subdomain}.')


def normalize_subdomain(subdomain: str) -> str:
    """Normalize a subdomain to a full domain.

    Args:
        subdomain (str): subdomain of a domain; may be empty to represent the
            base domain

    Returns:
        str: the normalized full subdomain

    """
    return config.DOMAIN if not subdomain else f'{subdomain}.{config.DOMAIN}'


class Cloudflare:
    """Cloudflare handler class.

    Currently, you can only update domains and subdomains.

    Attributes:
        headers (Dict[str, str]): headers to pass via `requests.put`;
            these are also used for authentication
        subdomains (SUBDOMAINS): a dictionary containing
            subdomains (keys) and their respective values, identifier
            (str) and proxied (bool)
        url (str): the URL for a user's domain

    """

    def __init__(self) -> None:
        """Initialize from config."""
        self.url = (f'{URL}/{config.ZONE}/dns_records')
        self.subdomains = config.SUBDOMAINS

        if len(config.AUTH) == 2:
            email, key = config.AUTH
            self.headers = {
                'X-Auth-Email': email,
                'X-Auth-Key': key
                }
        elif config.AUTH:
            token, = config.AUTH
            self.headers = {'Authorization': f'Bearer {token}'}

        self.headers['Content-Type'] = 'application/json'

    def get_subdomain_identifier(self, subdomain: str) -> None:
        """Get a subdomain identifier to use in the configuration file.

        Args:
            subdomain (str): the name of the DNS record to check;
                can be empty string ('') to represent only the domain

        """
        if not subdomain: # '' for only domain, no subdomain
            subdomain = ''

        url = normalize_subdomain(subdomain)

        for subd in config.SUBDOMAINS:
            if subd['subdomain'] == subdomain:
                params: PARAMS = subd
                append = False
                break
        else:
            params = {'subdomain': subdomain}
            append = True

        if 'identifier' in params:
            raise SubdomainIDAlreadySet(subdomain)

        if 'proxied' not in params:
            # By default, set proxied to True.
            # Users may change this to False if necessary.
            params['proxied'] = True

        response = requests.get(
            f'{self.url}?type=A&name={url}',
            headers=self.headers
            )
        result = response.json()['result']
        if len(result) > 1:
            raise TooManyRecords(subdomain)

        try:
            params['identifier'] = result[0]['id']
        except IndexError:
            raise NoRecords(subdomain)

        if append:
            config.SUBDOMAINS.append(params)
        else:
            for subd in config.SUBDOMAINS:
                if subd['subdomain'] == subdomain:
                    subd = params

        config.write_config()
        config.LOGGER.info(f'Wrote config for {url}!')

    def update_subdomain(self, ipaddr: str, params: PARAMS) -> None:
        """Update a specific subdomain.

        Args:
            ipaddr (str): the current IP address, e.g. 0.0.0.0
            params (PARAMS): a dictionary of the subdomain attributes,
                subdomain name (str), identifier (str), proxied (bool)

        """
        subdomain = str(params['subdomain'])
        url = normalize_subdomain(subdomain)

        update = {
            'type': 'A',
            'name': url,
            'content': ipaddr,
            'ttl': 120,
            'proxied': params['proxied']
            }

        response = requests.put(
            f"{self.url}/{params['identifier']}",
            json=update,
            headers=self.headers
            )

        config.LOGGER.info(f'Response: {response}')

    def update_all_subdomains(self, ipaddr: str) -> None:
        """Update all subdomains. Call `update_subdomain()` in batch.

        Args:
            ipaddr (str): the current IP address, e.g. 0.0.0.0

        """
        for params in self.subdomains:
            self.update_subdomain(ipaddr, params)


if __name__ == '__main__':
    cf = Cloudflare()
    if len(sys.argv) == 1:
        config.LOGGER.info('get_subdomain_identifier interactive mode')
        subdomain = input('Enter your subdomain: ')
        cf.get_subdomain_identifier(subdomain)
    else:
        config.LOGGER.info('get_subdomain_identifier batch mode')
        for arg in sys.argv[1:]:
            cf.get_subdomain_identifier(arg)
