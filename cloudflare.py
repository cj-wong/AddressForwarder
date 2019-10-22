from typing import Dict, Union

import requests

import config


class Cloudflare:
    """Cloudflare handler class."""

    def __init__(self) -> None:
        """Initialize from config."""
        self.url = (
            'https://api.cloudflare.com/client/v4/zones/'
            f'{config.ZONE}/dns_records'
            )
        self.subdomains = config.SUBDOMAINS
        if len(config.AUTH) == 1:
            token, = config.AUTH
            self.headers = {'Authorization': f'Bearer {token}'}
        else:
            email, key = config.AUTH
            self.headers = {
                'X-Auth-Email': email,
                'X-Auth-Key': key
                }
        self.headers['Content-Type'] = 'application/json'

    def update_subdomain(
        self, subdomain: Dict[str, Dict[str, Union[bool, str]]], ipaddr: str
        ) -> None:
        """Update a specific `subdomain`.

        Args:
            subdomain (dict): contains a label (str) and params (dict)
            ipaddr (str): the current IP address, e.g. 0.0.0.0

        """
        for label, params in subdomain.items():
            if label:
                url = f"{label}.{config['domain']}"
            else:
                url = config['domain']

            update = {
                'type': 'A',
                'name': url,
                'content': ipaddr,
                'ttl': 120,
                'proxied': params['proxied']
                }

            response = requests.put(
                f"{self.url}/{params['identifier']}",
                data=update,
                headers=self.headers
                )

            config.LOGGER.info(f'Response: {response}')

    def update_all_subdomains(self, ipaddr: str) -> None:
        """Update all subdomains. Calls `update_subdomain`.

        Args:
            ipaddr (str): the current IP address, e.g. 0.0.0.0

        """
        for subdomain in self.subdomains:
            self.update_subdomain(subdomain)
