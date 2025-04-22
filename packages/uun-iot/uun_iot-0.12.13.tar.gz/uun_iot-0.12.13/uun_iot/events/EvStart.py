import logging
import threading
import typing as t
from dataclasses import dataclass

from ..exceptions import EventCannotRegisterHandler
from ..typing import ModuleId
from ..utils import classproperty
from .Event import Event, EventType, Register

logger = logging.getLogger(__name__)

SelfM = t.Any
HandlerStartT = t.Callable[[SelfM, t.Tuple[threading.Event, threading.Event]], None]


class EvStart(Event):
    """Event for registering handlers to run on start of app.

    It is possible to register both blocking and non-blocking handlers.

    Warning:

        Ordering of handler execution is not given and cannot be relied upon.

    Examples:

        - configuration:

            .. code-block:: json

                {}

        .. code-block:: python

            from uun_iot import EvStart
            class AdvancedDataMeasurement(Module):
                @EvStart.subscribe
                def oneshot(self, evs):
                    # polling for data
                    runev, stopev = evs
                    while runev.is_set():
                        print("Polling for voltage reading from voltmeter...")
                        data = 53.8
                        if data > 50:
                            time.sleep(1)
                        else:
                            time.sleep(1.5)
                            print(data)

    """

    event_type = EventType.START
    _handlers: t.List[t.Tuple[t.Callable, bool]]
    _threads: t.Iterable[t.Tuple[threading.Thread, bool]]
    runev: threading.Event
    stopev: threading.Event

    def __init__(self, config=None):
        self.runev = threading.Event()
        self.stopev = threading.Event()
        self.stopev.set()
        self._handlers = []
        super().__init__(config=None)

    @classproperty
    def subscribe(cls):
        """Subscribe to Start event.

        The handler is run in a separate thread. The `.stop` method blocks until the
        thread returns.
        """
        return cls._register(Register[HandlerStartT], block=False)

    @classproperty
    def subscribe_blocking(cls):
        """This is a blocking handler variant.

        The handler is run in a separate thread and the `.start` method waits until the
        handler returns.
        """
        return cls._register(Register[HandlerStartT], block=True)

    def add_handlers(self, handler_list):
        self._handlers += [(fn, info.kwargs["block"]) for fn, info in handler_list]

    def start(self):
        """Invoke handlers in separate threads.

        Blocks until those registered in `@EvStart.subscribe_blocking` finish.
        """
        logger.debug("EvStart has these handlers registered: %s", repr(self._handlers))
        if not self._handlers or self.runev.is_set():
            # if no handlers to run or was not stopped
            return

        self.runev.set()
        self.stopev.clear()

        threads = []
        for fn, block in self._handlers:
            # do not store the thread to kill it later, rely solely on the func
            #   to terminate itself when runev Event is unset
            logger.debug(
                "Calling %sEvStart handler, function `%s`",
                "(blocking) " if block else "",
                fn,
            )
            th = threading.Thread(
                target=fn, args=((self.runev, self.stopev),), name=repr(fn)
            )
            th.start()
            threads.append((th, block))

        for th, block in threads:
            if block:
                logger.info(
                    "Waiting for blocking handler thread '%s' to finish in EvStart.start",
                    th.name,
                )
                th.join()

        self._threads = threads

    def stop(self):
        """Block till handlers terminate.

        Set `runev`, unset `stopev` and wait for started threads to finish.
        """
        # do not kill thread, rely solely on the handler
        #   to terminate itself when runev Event is unset
        if not self.runev.is_set():
            return

        self.runev.clear()
        self.stopev.set()

        for th, _ in self._threads:
            logger.debug("stopping %s", th)
            th.join()
            logger.debug("stopped %s", th)

        self._threads = []
