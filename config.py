import logging
import logging.handlers

import yaml


class InvalidConfigError(RuntimeError):
    """An invalid configuration was detected.

    - FileNotFoundError
    - ValueError
    - TypeError
    - KeyError

    """

    def __init__(self) -> None:
        """Initialize the error with a message."""
        super().__init__('An invalid configuration was detected. Exiting...')


_LOGGER_NAME = 'public_ipaddr_check'

LOGGER = logging.getLogger(_LOGGER_NAME)
LOGGER.setLevel(logging.DEBUG)

_FH = logging.handlers.RotatingFileHandler(
    f'{_LOGGER_NAME}.log',
    maxBytes=40960,
    backupCount=5,
    )
_FH.setLevel(logging.DEBUG)

_CH = logging.StreamHandler()
_CH.setLevel(logging.WARNING)

_FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
_FH.setFormatter(_FORMATTER)
_CH.setFormatter(_FORMATTER)

LOGGER.addHandler(_FH)
LOGGER.addHandler(_CH)


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
except FileNotFoundError as e:
    LOGGER.error(e)
    raise InvalidConfigError

try:
    CF = CONF['cloudflare']
    if CF['token'] and not CF['email']:
        AUTH = [CF['token']]
    elif CF['email'] and CF['key']:
        AUTH = [CF['email'], CF['key']]
    else:
        LOGGER.warn('Pick either token OR email and key.')
        CF_ENABLED = False
    ZONE = CF['zone']
    DOMAIN = CF['domain']
    SUBDOMAINS = CF['subdomains']
    CF_ENABLED = True
except KeyError:
    LOGGER.warn('Cloudflare configuration is missing')
    CF_ENABLED = False


def store_ipaddr(ipaddr: str) -> None:
    """Store the new IP address into file.

    Args:
        ipaddr (str): e.g. '0.0.0.0'

    """
    with open('ipaddr.yaml', 'w') as f:
        yaml.safe_dump({'ipaddr': ipaddr}, stream=f)


def write_config() -> None:
    """Write the config back to file.

    `get_subdomain_identifier` in `cloudflare.Cloudflare` uses this.

    """
    with open('config.yaml', 'w') as f:
        yaml.safe_dump(CONF, stream=f)
