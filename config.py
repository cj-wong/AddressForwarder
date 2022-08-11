import json
import logging
import logging.handlers
import sys


# Logger related

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

# Configuration file reading and validating

_CONFIG_LOAD_ERRORS = (
    FileNotFoundError,
    KeyError,
    TypeError,
    ValueError,
    json.decoder.JSONDecodeError,
    )

EXIT_CONFIG_INVALID = 1
EXIT_CONFIG_DEFAULT = 2
# Other exit codes continue here.

try:
    with open('config.json') as f:
        CONF = json.load(f)
except _CONFIG_LOAD_ERRORS as e:
    LOGGER.error("config.json doesn't exist or is malformed.")
    LOGGER.error(f'More information: {e}')
    sys.exit(EXIT_CONFIG_INVALID)

with open('config.json.example') as f:
    _DEFAULTS = json.load(f)

if _DEFAULTS == CONF:
    LOGGER.error(
        "config.json has default values. Modify them with your own.")
    sys.exit(EXIT_CONFIG_DEFAULT)
# Other configuration validation continues here.

try:
    CF = CONF['cloudflare']
    if CF['token'] and not CF['email']:
        AUTH = [CF['token']]
    elif CF['email'] and CF['key']:
        AUTH = [CF['email'], CF['key']]
    else:
        LOGGER.warn('Pick either token OR email and key.')
        sys.exit(EXIT_CONFIG_INVALID)
    ZONE = CF['zone']
    DOMAIN = CF['domain']
    SUBDOMAINS = CF['subdomains']
except KeyError:
    LOGGER.warn('Cloudflare configuration is missing or incomplete.')
    sys.exit(EXIT_CONFIG_INVALID)

try:
    WEBHOOKS = CONF['webhooks']
except KeyError:
    LOGGER.warn("No webhooks were defined.")

try:
    with open('ipaddr.yaml', 'r') as f:
        IPADDR = json.load(f)['ipaddr']
except (FileNotFoundError, KeyError, TypeError, ValueError):
    """ipaddr.yaml may not exist. Ignore if it doesn't."""
    IPADDR = None
    LOGGER.info('ipaddr.yaml does not exist. Using defaults...')

# Other configuration


def store_ipaddr(ipaddr: str) -> None:
    """Store the new IP address into file.

    Args:
        ipaddr (str): e.g. '0.0.0.0'

    """
    with open('ipaddr.json', 'w') as f:
        json.dump({'ipaddr': ipaddr}, f)


def write_config() -> None:
    """Write the config back to file.

    `get_subdomain_identifier` in `cloudflare.Cloudflare` uses this.

    """
    with open('config.json', 'w') as f:
        json.dump(CONF, f)
