import requests


def get_current_ipaddr() -> str:
    """Retrieves the current public IP address using ipify.

    Returns:
        str: the IP address

    """
    return requests.get('https://api.ipify.org').text
