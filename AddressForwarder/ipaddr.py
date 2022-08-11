import re
from collections import defaultdict
from operator import itemgetter
from typing import Dict, Tuple

import requests

import config


IPV4_ADDR = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
IPV6_ADDR = re.compile(r'^([0-9a-f]{0,4}:){5}[0-9a-f]{0,4}$', re.IGNORECASE)
TRACE_IPV4 = re.compile(r'ip=((\d{1,3}\.){3}\d{1,3})')
TRACE_IPV6 = re.compile(r'ip=(([0-9a-f]{0,4}:){5}[0-9a-f]{0,4})', re.I)

URLS = [
    'https://api.ipify.org',
    'https://ipapi.co/ip/',
    ]


def get_most_common_response(responses: Dict[str, int]) -> str:
    """Get the most common response.

    Unfortunately, if multiple responses are received, I don't know if the best
    way to go forward is to pick the consensus or just abort. For now, I pick
    the consensus.

    Args:
        responses (Dict[str, int]): responses from the APIs containing only the
            IP address

    Returns:
        str: the IP address

    """
    try:
        return sorted(responses.items(), key=itemgetter(1), reverse=True)[0][0]
    except (IndexError, TypeError):
        return ''


def get_ip_addresses() -> Tuple[str, str]:
    """Retrieve the current public IP address using multiple services.

    Returns:
        Tuple[str, str]: both IPv4 and IPv6

    """
    ipv4: Dict[str, int] = defaultdict(int)
    ipv6: Dict[str, int] = defaultdict(int)
    for url in URLS:
        response = requests.get(url).text
        if IPV4_ADDR.match(response):
            ipv4[response] += 1
        elif IPV6_ADDR.match(response):
            ipv6[response] += 1
        else:
            config.LOGGER.info(
                f"{url} did not return a valid response: {response}"
                )
    cf_trace = requests.get('https://www.cloudflare.com/cdn-cgi/trace').text
    cf_match = TRACE_IPV4.search(cf_trace)
    if cf_match:
        ipv4[cf_match.group(1)] += 1
    cf_match = TRACE_IPV6.search(cf_trace)
    if cf_match:
        ipv6[cf_match.group(1)] += 1

    if len(ipv4) != 1:
        config.LOGGER.warning("Multiple responses detected.")
        config.LOGGER.warning(ipv4)

    return (get_most_common_response(ipv4), get_most_common_response(ipv6))
