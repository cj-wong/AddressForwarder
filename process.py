import requests

import config
import ifttt
import ipaddr


if __name__ == '__main__':
    config.LOGGER.info('Beginning public IP address check...')
    ipaddr = ipaddr.get_current_ipaddr()
    config.LOGGER.info(f'Got current address: {ipaddr}')
    if config.IPADDR != ipaddr:
        config.LOGGER.info('Storing current IP address into ipaddr.yaml...')
        config.store_ipaddr(ipaddr)
        config.LOGGER.info('Attempting to send IFTTT webhook...')
        IFTTT = ifttt.IFTTT()
        IFTTT.send_alert(ipaddr)
        config.LOGGER.info('Completed. Exiting...')
    else:
        config.LOGGER.info('No changes. Exiting...')
