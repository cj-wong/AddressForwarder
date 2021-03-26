import requests

import config


URL = 'https://maker.ifttt.com/trigger'


class IFTTT:
    """IFTTT handler.

    Attributes:
        url (str): the personal IFTTT Maker/Webhooks URL
        event (str): the name of the event on IFTTT

    """

    def __init__(self) -> None:
        """Initialize IFTTT handler.

        Raises:
            config.InvalidConfigError: if the config could not be loaded

        """
        try:
            conf = config.CONF['ifttt']
            self.url = conf['url']
            self.event = conf['event']
        except (KeyError, TypeError, ValueError) as e:
            config.LOGGER.error(
                f'Could not initialize IFTTT configuration. {e}')
            raise config.InvalidConfigError

    def send_alert(self, ipaddr: str) -> None:
        """Send an alert via IFTTT if the public IP address is different.

        Args:
            ipaddr (str): the current public IP address

        """
        response = requests.post(
            f"{URL}/{self.event}/with/key/{self.url}",
            headers={'Content-Type': 'application/json'},
            json={'value1': ipaddr}
            )
        config.LOGGER.info(f'Response: {response}')
