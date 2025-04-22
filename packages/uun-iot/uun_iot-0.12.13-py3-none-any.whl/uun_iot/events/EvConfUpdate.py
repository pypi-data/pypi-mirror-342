import itertools
import logging
import threading
import typing as t
from dataclasses import dataclass

from ..utils import classproperty
from .Event import Event, EventType, Register

logger = logging.getLogger(__name__)

SelfM = t.Any


class EvConfUpdate(Event):
    """
    Event fired when new gateway configuration is available.

    This event is fired using :class:`uun_iot.modules.ConfigUpdater.ConfigUpdater`
    """

    event_type = EventType.CONF_UPDATE
    _handlers: t.List[t.Callable]

    def __init__(self, config=None):
        self._handlers = []
        super().__init__(config=None)

    @classproperty
    def subscribe(cls):
        """Register config update event.

        Register a handler to obtain the new configuration - it is passed in a single
        positional argument to the handler.

        If you are using the utility class Module, it is already registered for you. If
        you plan to register your own handler for some reason, consult documentation in
        Module.
        """
        return cls._register(Register[t.Callable[[SelfM, t.Dict], None]])

    def add_handlers(self, handler_list):
        self._handlers += [fn for fn, info in handler_list]

    def start(self):
        """Noop."""
        logger.debug(
            "EvConfUpdate has these handlers registered: %s", repr(self._handlers)
        )

    def stop(self):
        """Noop"""

    def fire_handlers(self, new_config: dict, block: bool = True):
        """Execute all stored handlers with new configuration.

        They are each executed in new thread.

        Args:
            new_config ([TODO:type]): [TODO:description]
            block: block till all of the executed handlers finish. Default is True.
        """
        threads = []
        for fn in self._handlers:
            logger.debug("Calling EvConfUpdate handler, function `%s`", fn)
            t = threading.Thread(target=fn, args=(new_config,))
            t.start()
            threads.append(t)

        if block:
            for t in threads:
                t.join()
