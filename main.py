import sys

import config
from AddressForwarder import cloudflare
from AddressForwarder import ipaddr
from AddressForwarder import webhook


def main() -> None:
    """Check address and update if necessary."""
    config.LOGGER.info('Beginning public IP address check...')
    ipv4, ipv6 = ipaddr.get_ip_addresses()
    config.LOGGER.info(f'Got current address: {ipv4} (IPv4), {ipv6} (IPv6)')
    if config.IPV4 == ipv4 and config.IPV6 == ipv6:
        config.LOGGER.info('No changes. Exiting...')
        sys.exit(0)
    if '.' in ipv4 and config.IPV4 != ipv4:
        config.LOGGER.info("A new IPv4 address was detected.")
        config.LOGGER.info('Attempting to update DNS records on Cloudflare...')
        cf = cloudflare.Cloudflare()
        cf.update_all_subdomains(ipv4)
    # Because IPv6 is not mandatory, ipv6 can be an empty string. Only apply
    # changes if it's true.
    if ipv6 and ':' in ipv6 and config.IPV6 != ipv6:
        config.LOGGER.info("A new IPv6 address was detected.")
        config.LOGGER.info('Attempting to update DNS records on Cloudflare...')
        cf = cloudflare.Cloudflare()
        cf.update_all_subdomains(ipv6)
    config.LOGGER.info('Attempting to send webhook...')
    webhook.send_webhooks({"ipaddr": ipv4})
    config.LOGGER.info('Storing current IP address into ipaddr.json...')
    config.store_ipaddr(ipv4, ipv6)
    config.LOGGER.info('Completed. Exiting...')


if __name__ == '__main__':
    main()
