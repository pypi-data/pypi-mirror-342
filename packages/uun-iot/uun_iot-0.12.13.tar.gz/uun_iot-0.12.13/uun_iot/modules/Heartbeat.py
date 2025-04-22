import logging
from datetime import datetime
from typing import Callable, Dict, Optional

import requests
from uun_iot import EvTick
from uun_iot.utils import get_iso_timestamp

logger = logging.getLogger(__name__)


class Heartbeat:
    online: bool

    """
    Ping server in short periods to let server know if the gateway is online and
    send a little info about the gateway.

    Args:
        uucmd: function ``(dto_in) -> requests.Response``, the function takes
            an argument with data to be sent to the heartbeat uuCmd endpoint. It
            returns the reponse formed using :class:`requests.Response`.
    """

    id = "heartbeat"

    def __init__(self, uucmd: Callable[[Dict], Optional[requests.Response]]):
        self.online = False
        self._uucmd = uucmd

    @EvTick.subscribe
    def beat(self):
        """Determine online status and send a little information about gateway to uuApp.

        The online status is determined using ``self._uucmd`` uuCmd. The information sent includes

            - boot timestamp (in ISO timestamp)
            - CPU usage in percent
            - RAM usage in percent

        Executed on each timer tick.
        """

        try:
            # in docker, psutil is not installed
            import psutil

            boot_timestamp = get_iso_timestamp(
                datetime.fromtimestamp(psutil.boot_time())
            )
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
        except ImportError:
            boot_timestamp = cpu = ram = None

        dto_in = {
            "bootTimestamp": boot_timestamp,
            "cpuUsage": cpu,
            "ramUsage": ram,
        }

        response = self._uucmd(dto_in)
        if response:
            if response.status_code >= 200 and response.status_code < 300:
                if not self.online:
                    logger.info("online")
                    self.online = True
            else:
                if self.online:
                    logger.warning("uuApp server error")
                    self.online = False
        else:
            if self.online:
                logger.warning("network offline")
                self.online = False
