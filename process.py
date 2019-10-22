import requests

import cloudflare
import config
import ifttt
import ipaddr


if __name__ == '__main__':
    config.LOGGER.info('Beginning public IP address check...')
    ipaddr = ipaddr.get_current_ipaddr()
    config.LOGGER.info(f'Got current address: {ipaddr}')
    if '.' not in ipaddr or not ipaddr:
        config.LOGGER.warn(f'IP address appears invalid. Exiting...')
    elif config.IPADDR != ipaddr:
        config.LOGGER.info('Storing current IP address into ipaddr.yaml...')
        config.store_ipaddr(ipaddr)
        config.LOGGER.info('Attempting to update DNS records on Cloudflare...')
        cf = cloudflare.Cloudflare()
        cf.update_all_subdomains(ipaddr)
        config.LOGGER.info('Attempting to send IFTTT webhook...')
        try:
            IFTTT = ifttt.IFTTT()
            IFTTT.send_alert(ipaddr)
        except config.InvalidConfigError:
            config.LOGGER.info('Could not send IFTTT webhook.')
        config.LOGGER.info('Completed. Exiting...')
    else:
        config.LOGGER.info('No changes. Exiting...')
