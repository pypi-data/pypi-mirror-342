import logging
import threading
import typing as t

from ..utils import classproperty
from .Event import Event, EventType, Register

logger = logging.getLogger(__name__)

SelfM = t.Any


class EvStop(Event):
    """An Event which invokes handlers on app stop."""

    event_type = EventType.STOP
    _handlers: t.List[t.Callable]

    def __init__(self, config=None):
        self._handlers = []
        super().__init__(config=None)

    @classproperty
    def subscribe(cls):
        """Subscribe to Stop event.

        The handler is run on `.stop` and it blocks until the handler returns.
        """
        return cls._register(Register[t.Callable[[SelfM], None]])

    def add_handlers(self, handler_list):
        self._handlers += [fn for fn, info in handler_list]

    def start(self):
        """No-op."""
        logger.debug("EvStop has these handlers defined: %s", repr(self._handlers))
        pass

    def stop(self):
        """Invoke handlers and block till they finish.

        Each handler is started in a separate thread, then threads are
        collected.
        """
        if not self._handlers:
            return

        threads = []
        for fn in self._handlers:
            logger.debug("Calling EvStop handler, function `%s`", fn)
            th = threading.Thread(target=fn)
            th.start()
            threads.append(th)

        for th in threads:
            logger.debug("joining EvStop thread %s", th)
            th.join()
            logger.debug("joined EvStop thread %s", th)
