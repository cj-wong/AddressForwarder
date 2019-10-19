import requests

import config
import ifttt
import ipaddr


def print_info(message: str) -> None:
    """Prints and logs to INFO.

    Args:
        message (str): the message to print and log

    """
    print(message)
    config.LOGGER.info(message)


if __name__ == '__main__':
    print_info('Beginning public IP address check...')
    ipaddr = ipaddr.get_current_ipaddr()
    print_info(f'Got current address: {ipaddr}')
    if config.IPADDR['ipaddr'] != ipaddr:
        config.IPADDR['ipaddr'] = ipaddr
        print_info('Storing current IP address into ipaddr.yaml...')
        config.store_ipaddr(IPADDR)
        print_info('Attempting to send IFTTT webhook...')
        IFTTT = ifttt.IFTTT()
        IFTTT.send_alert(ipaddr)
        print_info('Completed. Exiting...')
    else:
        print_info('No changes. Exiting...')
