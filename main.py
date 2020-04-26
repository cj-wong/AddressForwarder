import requests

import config
import ifttt
import ipaddr


def main() -> None:
    """This function runs everything: gets the current IP address,
    checks whether it's a valid IP address string, compares against the
    last known IP address, stores the new one if so, and sends the
    alert via IFTTT.
    
    """
    config.LOGGER.info('Beginning public IP address check...')
    ipaddr = ipaddr.get_current_ipaddr()
    config.LOGGER.info(f'Got current address: {ipaddr}')
    if '.' not in ipaddr or not ipaddr:
        config.LOGGER.warn(f'IP address appears invalid. Exiting...')
    elif config.IPADDR != ipaddr:
        config.LOGGER.info('Storing current IP address into ipaddr.yaml...')
        config.store_ipaddr(ipaddr)
        config.LOGGER.info('Attempting to send IFTTT webhook...')
        IFTTT = ifttt.IFTTT()
        IFTTT.send_alert(ipaddr)
        config.LOGGER.info('Completed. Exiting...')
    else:
        config.LOGGER.info('No changes. Exiting...')


if __name__ == '__main__':
    main()
