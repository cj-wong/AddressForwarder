import logging

import yaml


LOGGER = logging.getLogger('public_ipaddr_check')
LOGGER.setLevel(logging.DEBUG)

FH = logging.FileHandler('ipaddr.log')
FH.setLevel(logging.DEBUG)

CH = logging.StreamHandler()
CH.setLevel(logging.INFO)

FH.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
CH.setFormatter(
    logging.Formatter(
        '%(levelname)s - %(message)s'
        )
    )

LOGGER.addHandler(FH)
LOGGER.addHandler(CH)


try:
    with open('ipaddr.yaml', 'r') as f:
        IPADDR = yaml.safe_load(f)['ipaddr']
except (FileNotFoundError, KeyError, TypeError, ValueError):
    """ipaddr.yaml may not exist. Ignore if it doesn't."""
    IPADDR = None
    LOGGER.info('ipaddr.yaml does not exist. Using defaults...')

try:
    with open('config.yaml') as f:
        CONF = yaml.safe_load(f)
    CF = CONF['cloudflare']
    if CF['token'] and not CF['email']:
        AUTH = [CF['token']]
    elif CF['email'] and CF['key']:
        AUTH = [CF['email'], CF['key']]
    else:
        LOGGER.error('Pick either token OR email and key.')
        raise InvalidConfigError
    ZONE = CF['zone']
    DOMAIN = CF['domain']
    SUBDOMAINS = CF['subdomains']
except FileNotFoundError as e:
    print('Encountered a fatal error:', e)
    LOGGER.error(e)
    raise InvalidConfigError
except KeyError:
    LOGGER.error('Cloudflare configuration is missing')
    raise InvalidConfigError


class Error(Exception):
    """Base exception for config"""
    pass


class InvalidConfigError(Error):
    """An invalid configuration was detected.

    - FileNotFoundError
    - ValueError
    - TypeError
    - KeyError
    """
    def __init__(self):
        super().__init__('An invalid configuration was detected. Exiting...')


def store_ipaddr(ipaddr: str) -> None:
    """Store the new IP address into file.

    Args:
        ipaddr (str): e.g. '0.0.0.0'

    """
    with open('ipaddr.yaml', 'w') as f:
        yaml.safe_dump({'ipaddr': ipaddr}, stream=f)
