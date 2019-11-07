import requests

import config


class IFTTT:
    """IFTTT handlder."""
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
            config.LOGGER.warn('Could not initialize IFTTT configuration.')
            raise config.InvalidConfigError

    def send_alert(self, ipaddr: str) -> None:
        """Sends an alert via IFTTT if the public IP address is different.

        Args:
            ipaddr (str): the current public IP address

        """

        response = requests.post(
           f"https://maker.ifttt.com/trigger/{self.event}/with/key/{self.url}",
           headers={'Content-Type': 'application/json'},
           json={'value1': ipaddr}
           )
        config.LOGGER.info(f'Response: {response}')
