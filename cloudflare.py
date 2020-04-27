import sys
from typing import Dict, Union

import requests

import config


PARAMS = Dict[str, Union[bool, str]]
SUBDOMAINS = Dict[str, PARAMS]

URL = 'https://api.cloudflare.com/client/v4/zones'


class SubdomainValueAlreadySet(ValueError):
    """A value already exists in the subdomain attribute."""
    def __init__(self, subdomain: str, field: str) -> None:
        super().__init__(
            f'The {field} field for {subdomain} already has a value. '
            'Delete the value if you want to re-run the function.'
            )


class NoRecords(ValueError):
    """No DNS records were found given a subdomain."""
    def __init__(self, subdomain: str) -> None:
        super().__init__(f'No subdomains were found matching {subdomain}.')


class TooManyRecords(ValueError):
    """Too many DNS records were found given a subdomain."""
    def __init__(self, subdomain: str) -> None:
        super().__init__(f'Too many DNS records were found for {subdomain}.')



class Cloudflare:
    """Cloudflare handler class. Currently, you can only update domains
    and subdomains.

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

        try:
            email, key = config.AUTH
            self.headers = {
                'X-Auth-Email': email,
                'X-Auth-Key': key
                }
        except (TypeError, ValueError):
            token, = config.AUTH
            self.headers = {'Authorization': f'Bearer {token}'}

        self.headers['Content-Type'] = 'application/json'

    def get_subdomain_identifier(self, subdomain: str) -> str:
        """Get a subdomain identifier so that it may be used in the
        configuration file.

        Args:
            subdomain (str): the name of the DNS record to check;
                can be empty string ('') to represent only the domain

        """
        if not subdomain: # '' for only domain, no subdomain
            subdomain = ''
            url = config.DOMAIN
        else:
            url = f'{subdomain}.{config.DOMAIN}'

        if subdomain not in config.SUBDOMAINS:
            config.SUBDOMAINS[subdomain] = {}

        try:
            if config.SUBDOMAINS[subdomain]['identifier']:
                raise SubdomainValueAlreadySet(subdomain, 'id')
        except KeyError:
            pass

        try:
            proxied = config.SUBDOMAINS[subdomain]['proxied']
        except KeyError:
            # By default, set proxied to True.
            # Users may change this to False if necessary.
            proxied = True

        response = requests.get(
            f'{self.url}?type=A&name={url}',
            headers=self.headers
            )
        result = response.json()['result']
        if len(result) > 1:
            raise TooManyRecords(subdomain)

        try:
            subdomain_id = result[0]['id']
        except IndexError:
            raise NoRecords(subdomain)

        config.SUBDOMAINS[subdomain] = {
            'identifier': subdomain_id,
            'proxied': proxied,
            }

        config.write_config()

        config.LOGGER.info(f'Wrote config for {url}!')

        return subdomain_id

    def update_subdomain(self, subdomain: str, ipaddr: str, params: PARAMS
        ) -> None:
        """Update a specific `subdomain`.

        Args:
            subdomain (str): the name of the DNS record to check;
                can be empty string ('') to represent only the domain
            ipaddr (str): the current IP address, e.g. 0.0.0.0
            params (PARAMS): a dictionary of the subdomain attributes,
                identifier (str) and proxied (bool)

        """
        if subdomain:
            url = f"{subdomain}.{config.DOMAIN}"
        else:
            url = config.DOMAIN

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
        """Update all subdomains. Calls `update_subdomain`.

        Args:
            ipaddr (str): the current IP address, e.g. 0.0.0.0

        """
        for subdomain, params in self.subdomains.items():
            self.update_subdomain(subdomain, ipaddr, params)


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
