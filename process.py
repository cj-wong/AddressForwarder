import sys

import requests
import yaml


try:
    with open('ipaddr.yaml', 'r') as f:
        IPADDR = yaml.safe_load(f)
except (FileNotFoundError, KeyError):
    IPADDR = {'ipaddr': None}


def get_current_ipaddr() -> str:
    """Retrieves the current public IP address using ipify.

    Returns:
        str: the IP address

    """
    return requests.get('https://api.ipify.org').text


def store_ipaddr(IPADDR: dict) -> None:
    """Store the new IP address into file.

    Args:
        IPADDR (dict): {'ipaddr': 0.0.0.0}

    """
    with open('ipaddr.yaml', 'w') as f:
        yaml.safe_dump(IPADDR, stream=f)


def send_alert(ipaddr: str) -> None:
    """Sends an alert via IFTTT if the public IP address is different.

    Args:
        ipaddr (str): the current public IP address

    """
    try:
        with open('config.yaml') as f:
            ifttt = yaml.safe_load(f)['ifttt']
            url = ifttt['url']
            event = ifttt['event']
    except (ValueError, TypeError, KeyError) as e:
        print('Encountered a fatal error:', e)
        print('Exiting...')
        sys.exit(1)

    response = requests.post(
       f"https://maker.ifttt.com/trigger/{event}/with/key/{url}",
       headers={'Content-Type': 'application/json'},
       json={'value1': ipaddr}
       )
    print('Response:', response)

if __name__ == '__main__':
    print('Beginning public IP address check...')
    ipaddr = get_current_ipaddr()
    print('Got current address:', ipaddr)
    if IPADDR['ipaddr'] != ipaddr:
        IPADDR['ipaddr'] = ipaddr
        print('Storing current IP address into ipaddr.yaml...')
        store_ipaddr(IPADDR)
        print('Attempting to send IFTTT webhook...')
        send_alert(ipaddr)
        print('Completed. Exiting...')
    else:
        print('No changes. Exiting...')
