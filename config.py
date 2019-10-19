import logging
from typing import Dict

import yaml


LOGGER = logging.getLogger('public_ipaddr_check')
LOGGER.setLevel(logging.DEBUG)

FH = logging.FileHandler('ipaddr.log')
FH.setLevel(logging.DEBUG)

CH = logging.StreamHandler()
CH.setLevel(logging.WARNING)

FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
FH.setFormatter(FORMATTER)
CH.setFormatter(FORMATTER)

LOGGER.addHandler(FH)
LOGGER.addHandler(CH)


try:
    with open('ipaddr.yaml', 'r') as f:
        IPADDR = yaml.safe_load(f)
except FileNotFoundError:
    """ipaddr.yaml may not exist. Ignore if it doesn't."""
    IPADDR = {'ipaddr': None}
    LOGGER.info('ipaddr.yaml does not exist. Using defaults...')

try:
    with open('config.yaml') as f:
        CONF = yaml.safe_load(f)
except FileNotFoundError as e:
    print('Encountered a fatal error:', e)
    LOGGER.error(e)
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


def store_ipaddr(ipaddr: Dict[str, str]) -> None:
    """Store the new IP address into file.

    Args:
        ipaddr (dict): {'ipaddr': '0.0.0.0'}

    """
    with open('ipaddr.yaml', 'w') as f:
        yaml.safe_dump(ipaddr, stream=f)
