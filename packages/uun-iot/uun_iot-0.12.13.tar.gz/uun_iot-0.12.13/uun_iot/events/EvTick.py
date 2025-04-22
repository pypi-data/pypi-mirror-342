import contextlib
import logging
import threading
import typing as t
from collections import defaultdict

from ..exceptions import EventCannotRegisterHandler
from ..typing import ModuleId
from ..utils import RepeatTimer, classproperty
from .Event import Event, EventType, HandlerInfo, Register

logger = logging.getLogger(__name__)
SelfM = t.Any

CONFIG_TIMER_KEY = "moduleTimers"
GATEWAY_KEY = "gateway"

HandlerTickT = t.Callable[[SelfM], None]


class EvTick(Event, contextlib.AbstractContextManager):
    """
    Event that fires periodically when a timer expires.

    Periods are loaded from configuration file and are updated on configuration update.

    Pass full configuration.

    Examples:

        - ``timer`` event without ID

            - configuration:

                .. code-block:: json

                    {
                        "gateway": {
                            "moduleTimers": {
                                "timerModule": 1
                            }
                        }
                    }

            .. code-block:: python


                from uun_iot import EvTick
                class TimerModule:
                    id = "timerModule" # optional
                    @EvTick.subscribe
                    def periodical(self):
                        print("Tick tock every 1 s.")

        - ``timer`` event with ID

            - configuration

                .. code-block:: json

                    {
                        "gateway": {
                            "moduleTimers": {
                                "sendReceive": {
                                    "send": 2,
                                    "get": 1
                                }
                            }
                        }
                    }

            .. code-block:: python

                class SendReceive:
                    @EvTick.subscribe_timer("get")
                    def retrieve(self):
                        print(f"Retrieving data...")

                    @EvTick.subscribe_timer("send")
                    def send(self):
                        print(f"Sending data...")
    """

    event_type = EventType.TICK

    _fire_on_start: bool

    startev: threading.Event
    _handlers: t.DefaultDict[
        ModuleId, t.DefaultDict[t.Optional[str], t.List[t.Callable]]
    ]
    _timers: t.Collection[t.Tuple[RepeatTimer, t.Tuple[ModuleId, t.Optional[str]]]]

    def __init__(self, config=None, fire_on_start: bool = True):
        """
        Args:
            config: dictionary with configuration
            fire_on_start: if the timers should execute right when :meth:`.start` is run
                if True, run on start and then each period,
                if False, do not run on start but after that run each period
        """
        self.startev = threading.Event()
        self._handlers = defaultdict(lambda: defaultdict(list))  # handlers[x][y]=[...]
        self._timers = []
        self._fire_on_start = fire_on_start
        super().__init__(config=config, requires_config=True)

    @classproperty
    def subscribe(cls):
        """Decorate a method to register it as a EvTick handler

        The handler corresponds to the timer found in config under
            ``"moduleTimers: { "moduleId": <period in seconds [float]>}``
        """
        return cls._register(Register[HandlerTickT], None)

    @classmethod
    def subscribe_timer(cls, timer_id: str):
        """Decorate a method to register it as a EvTick handler

        The handler corresponds to the timer found in config under
            ``"moduleTimers: { "moduleId": { "timerId": <period in seconds [float]>}}``

        Args:
            timer_id: timer id corresponding to configuration entry and current class
        """
        if not isinstance(timer_id, str):
            raise EventCannotRegisterHandler("Only string timer IDs are supported.")
        return cls._register(Register[HandlerTickT], timer_id)

    def add_handlers(
        self,
        handler_list: t.Iterable[t.Tuple[t.Callable, HandlerInfo]],
    ):
        if self.startev.is_set():
            raise EventCannotRegisterHandler(
                "Stop the EvTick before adding new handlers."
            )

        handlers = self._handlers
        # populate and check validity of handlers
        for fn, info in handler_list:
            mid = info.owner_id
            timer_id = info.args[0]
            handlers[mid][timer_id].append(fn)
            if None in handlers[mid] and len(set(handlers[mid].keys())) > 1:
                # multiple None handlers are valid - different instances
                # of same class might register None handler each
                raise EventCannotRegisterHandler(
                    "You cannot mix @EvTick.subscribe and @EvTick.subscribe_timer"
                    f" in module '{mid}'"
                )

        assert self._handlers == handlers
        # default dict no longer needed for reading, convert to dict to prevent accidental bugs
        self._timers = self._init_timers(
            dict(handlers),
        )

    def _init_timers(
        self,
        handlers: t.Dict[ModuleId, t.Dict[t.Optional[str], t.List[t.Callable]]],
    ):
        """Initialize timers for handlers from configuration."""
        assert self._config is not None
        timers = []
        for mid in handlers:
            try:
                interval_base = self._config[GATEWAY_KEY][CONFIG_TIMER_KEY][mid]
                assert interval_base != {}
            except (KeyError, AssertionError):
                # user has registered tick handler but no timer entry in config
                logger.warning(
                    "You defined handler for EvTick but did not specify"
                    f" timer period for module '%s'.",
                    mid,
                )
                continue

            interval_dict: t.Dict[t.Optional[str], float]
            if not isinstance(interval_base, dict):
                interval_dict = {None: interval_base}
            else:
                interval_dict = interval_base

            set_handlers = set(handlers[mid].keys())
            set_config = set(interval_dict.keys())
            if set_handlers != set_config:
                logger.error(
                    "Mismatch between defined EvTick handlers and timers in"
                    " configuration '.moduleTimers'."
                    " In configuration, there are '%s' and you defined handlers '%s'.",
                    set_config,
                    set_handlers,
                )
                raise EventCannotRegisterHandler()
            for timer_id, fns in handlers[mid].items():
                period = interval_dict[timer_id]
                timers.extend(
                    (
                        RepeatTimer(period, fn, runonstart=self._fire_on_start),
                        (mid, timer_id),
                    )
                    for fn in fns
                )
        return timers

    def number_of_handlers(self):
        """Get number of registered EvTick handlers.

        Warning: See :meth:`.number_of_timers` for an actual number of functional timers.
        """
        s = 0
        for mid, subev in self._handlers.items():
            for timer_id, fns in subev.items():
                s += len(fns)
        return s

    def number_of_timers(self):
        """Get number of created timers, as specified in configuration.

        Note that :meth:`.number_of_handlers` always returns number greater than or equal to
        :meth:`.number_of_timers`

        Some handlers might not have a timer entry in configuration and the
        corresponding timer is thus not created. Still, the handler is stored and a
        future configuration update might add the timer for the handler.
        """
        return len(self._timers)

    def start(self):
        logger.debug("EvTick has these handlers registered: %s", repr(self._handlers))
        logger.debug("EvTick has these timers registered: %s", repr(self._timers))
        for timer, (mid, tid) in self._timers:
            timer.start()
            logger.debug("Timer `%s:%s` started.", mid, tid)

    def stop(self):
        for timer, (mid, tid) in self._timers:
            timer.stop()
            logger.debug("Timer `%s:%s` stopped.", mid, tid)

    def update(self, new_config: dict):
        """Update timers from config. Compare new periods to existing and
        restart timer if neccesarry.

        The possible timer restart stops the timer, sets new period and then run the
        timer with new period, skipping the initial fire on start.

        Side effect: should the EvTick event be stopped and started again,
        updated timers will have runonstart=False.
        """
        self._config = new_config

        for timer, (mid, tid) in self._timers:
            try:
                new_period = self._config[GATEWAY_KEY][CONFIG_TIMER_KEY][mid]
                if tid is not None:
                    new_period = self._config[GATEWAY_KEY][CONFIG_TIMER_KEY][mid][tid]
            except KeyError:
                logging.warning(
                    "Configuration update removed timer entry for timer '%s.%s'.",
                    mid,
                    tid,
                )
                continue

            if not isinstance(new_period, (int, float)):
                logger.warning(
                    "Received invalid period in new configuration %s.%s: '%s'",
                    mid,
                    tid,
                    timer,
                )
                continue

            if new_period != timer.period:
                timer.stop()
                timer.runonstart = False
                timer.period = new_period
                timer.start()
                logger.info("Updated `%s.%s`'s timer to {new_period} s", mid, tid)
