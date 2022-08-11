import config
from AddressForwarder import cloudflare
from AddressForwarder import ipaddr
from AddressForwarder import webhook


def main() -> None:
    """Check address and update if necessary."""
    config.LOGGER.info('Beginning public IP address check...')
    ip_addr = ipaddr.get_current_ipaddr()
    config.LOGGER.info(f'Got current address: {ip_addr}')
    if '.' not in ip_addr or not ip_addr:
        config.LOGGER.warn(f'IP address appears invalid. Exiting...')
    elif config.IPADDR != ip_addr:
        config.LOGGER.info("A new IP address was detected.")
        config.LOGGER.info('Attempting to update DNS records on Cloudflare...')
        cf = cloudflare.Cloudflare()
        cf.update_all_subdomains(ip_addr)
        config.LOGGER.info('Attempting to send webhook...')
        webhook.send_webhooks({"ipaddr": ip_addr})
        config.LOGGER.info('Storing current IP address into ipaddr.yaml...')
        config.store_ipaddr(ip_addr)
        config.LOGGER.info('Completed. Exiting...')
    else:
        config.LOGGER.info('No changes. Exiting...')


if __name__ == '__main__':
    main()
