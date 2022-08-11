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
            message = webhook['message']
            if type(message) is dict:
                new = {
                    k.format(**params): v.format(**params)
                    for k, v in message.items()
                    }
                response = requests.post(url, headers=HEADERS, json=new)
            else:
                message = message.format(**params)
                response = requests.post(url, headers=HEADERS, data=message)
            config.LOGGER.info(f"Response: {response}")
    except AttributeError:
        pass
