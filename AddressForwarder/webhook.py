from typing import Dict

import requests

import config


HEADERS = {'Content-Type': 'application/json'}


def send_webhooks(params: Dict[str, str]) -> None:
    """Send webhooks with configured message.

    Args:
        params (Dict[str, str]): parameters that can format a message;
            parameters: "ipaddr"

    """
    try:
        for webhook in config.WEBHOOKS:
            url = webhook['url']
            message = webhook['message'].format(**params)
            if type(message) is dict:
                response = requests.post(url, headers=HEADERS, json=message)
            else:
                response = requests.post(url, headers=HEADERS, data=message)
            config.LOGGER.info(f"Response: {response}")
    except AttributeError:
        pass
