import logging
import logging.handlers

import yaml


LOGGER = logging.getLogger('public_ipaddr_check')
LOGGER.setLevel(logging.DEBUG)

FH = logging.handlers.RotatingFileHandler(
    'ipaddr.log',
    maxBytes=4096,
    backupCount=5,
    )
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
    with open('config.yaml', 'r') as f:
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
    LOGGER.error(e)
    raise InvalidConfigError
except KeyError:
    LOGGER.error('Cloudflare configuration is missing')
    raise InvalidConfigError


class InvalidConfigError(RuntimeError):
    """An invalid configuration was detected.

    - FileNotFoundError
    - ValueError
    - TypeError
    - KeyError
    """
    def __init__(self) -> None:
        super().__init__('An invalid configuration was detected. Exiting...')


def store_ipaddr(ipaddr: str) -> None:
    """Store the new IP address into file.

    Args:
        ipaddr (str): e.g. '0.0.0.0'

    """
    with open('ipaddr.yaml', 'w') as f:
        yaml.safe_dump({'ipaddr': ipaddr}, stream=f)


def write_config() -> None:
    """Write the config back to file. `get_subdomain_identifier` in
    `cloudflare.Cloudflare` uses this.

    """
    with open('config.yaml', 'w') as f:
        yaml.safe_dump(CONF, stream=f)
