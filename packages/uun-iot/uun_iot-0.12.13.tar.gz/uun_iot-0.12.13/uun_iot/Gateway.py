"""
Main Gateway class which manages all user modules.
"""

import contextlib
import json
import logging
import signal
import sys
import threading
import typing as t
from collections.abc import Iterable

from .events import Event, attach_handlers, merge_events
from .modules import init_library_module_events
from .UuAppClient import UuAppClient

UserModule = t.Any

logger = logging.getLogger(__name__)
loggerc = logging.getLogger(__name__ + ".Config")


class Gateway(contextlib.AbstractContextManager):
    """Main application entrypoint.

    Gateway is responsible for initializing all events (and all modules) by providing
    them configuration and app start/stop information.

    This class is a `ContextManager`. On enter, the :meth:`.start` method is called,
    on leave, the :meth:`.stop` method is called.

    Warning:
        When an exception is thrown inside the ``module_init`` or ``event_init`` function
        (usually calling class constructors), it is not supressed and leads to
        classical exception behaviour (ie. program termination).

        When an exception is thrown inside an event handler, the exception is typically
        catched and printed via logging. Consult corresponding event for more information.

    Examples:

        .. code-block:: python

            from uun_iot import Gateway:
            config_file="config.json"
            with Gateway(config_file) as g:
                while True:
                    g.stopev.wait()

        In this example, the :class:`Gateway` is initialized using the
        configuration file in a `with` block. Upon entering, the gateway is
        started. When an exeption occurs, the gateway is gracefully stopped
        using its :meth:`.stop` method -- this allows the `Gateway` to do
        cleanup and inform user modules (here are none) that they should exit,
        too.

    Configuration:

        The preffered styling of the JSON keys is ``camelCase``, ie. first letter
        lowercase, letters after spaces uppercase and finally, the spaces removed.

        The JSON configuration file has the following example structure:

        .. code-block:: json
            :force:

            {
                "gateway": {

                    "moduleTimers": {
                        "customModule1": {
                            "receive": 120,
                            "send": 400
                        },
                        "customModule2": 60
                    },

                    "moduleBackupStorage": {
                        "customModule1": "backup/customModule1.json",
                        "customModule2": {
                            "path": "backup/customModule2.json",
                            "limit": 50
                        }
                    },

                    "customModule2": {
                        "option1": "value1"
                    }
                },

                "uuApp": { ... },
                "uuThing": { ... },
                "oidcGrantToken": { ... }
            }

        On the other hand, a **minimal** configuration file is an empty JSON file:

        .. code-block:: json

            {}

        Meaningful keys and subkeys are:

            - ``gateway``: `optional`. Main configuration for this IoT application

                - ``moduleTimers``: `optional`. Core functionality, dictionary with
                  periods (in seconds) for ``@on("tick")`` events for corresponding
                  modules. The module IDs are keys, the periods are values.

                    - Multiple timers can be
                      specified by introducing a subobject with the timer ID and the
                      timer period. The timer ID corresponds to the event defined in
                      Python code as ``@on("tick", "timerId")``.

                - ``moduleBackupStorage``: `optional`. Applies to modules based on
                  :class:`~uun_iot.modules.Module.Module`. The format is module ID
                  as key and file path as value. This key is used to specify
                  location to which should unsent data from the module be saved,
                  see :class:`~uun_iot.modules.Module.Module` for more information.

                    - You can specify additional information, such that the storage
                      should be limited in size. For this, specify the size of the
                      storage in number of entries in ``limit`` and add the
                      original file path in the ``path`` key.

                - ``<moduleId>``: `optional`. A default place for the configuration specific to
                  the module with ID ``moduleId``. The structure is arbitrary and
                  depends on your needs.

            - keys for :class:`uun_iot.UuAppClient`. `Optional`. See documentation there for
              more information. If you want to use secure communication with uuApp,
              specify the details in keys

                - ``uuApp``
                - ``uuThing``
                - ``oidcGrantToken``


    Args:
        config_file: path to configuration JSON file. See :class:`Config` for
            information about format of the file.
        module_init: a function instantiating modules and returning the
            instances with registered handlers which are to be registered to events
            defined in this library
        event_init: a function with different signature for advanced use cases. Takes
            a config file path, config dictionary and UuAppClient and returns instantiated
            events with registered handlers (using :func:`attach_handlers`).
            Beware that if you want to use library modules (ConfifUpdater, SocketServer, Heartbeat),
            you need to incorporate :func:`uun_iot.modules.init_library_modules` into the function.
            It can be used to define custom
            events (as long as they derive :class:`Event`) or create event-module strong
            coupling if needed (see :class:`ConfigUpdater` or :class:`SocketServer`).
            For defining custom events, see documentation in :mod:`events` module.
    """

    _events: t.Iterable[Event]

    #: event set when the gateway is running
    runev: threading.Event
    stopev: threading.Event

    def __init__(
        self,
        config_file: t.Optional[str],
        module_init: t.Optional[
            t.Union[
                t.Callable[[t.Dict, UuAppClient], UserModule],
                t.Callable[[t.Dict, UuAppClient], t.Iterable[UserModule]],
            ]
        ],
        event_init: t.Optional[
            t.Callable[[t.Optional[str], t.Dict, UuAppClient], t.Iterable[Event]]
        ] = None,
    ):

        logger.debug("Starting gateway module system.")

        if not module_init and not event_init:
            raise ValueError("Both init methods cannot be empty")

        if module_init and event_init:
            raise ValueError("Specify only one init method")

        if config_file is None:
            config = {}
        else:
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError("Could not decode JSON config") from e
            except FileNotFoundError as e:
                raise ValueError(
                    "Provided config file '%s' does not exist", config_file
                ) from e

        if "gateway" not in config:
            config["gateway"] = {}

        uuapp_client = UuAppClient(config)

        if module_init:
            logger.debug("using basic module init")
            base_events = init_library_module_events(config_file, config, uuapp_client)
            user_modules = module_init(config, uuapp_client)
            if not isinstance(user_modules, Iterable):
                user_modules = [user_modules]
            user_events = attach_handlers(config, user_modules, base_events)
            # do not discard events needed for library modules even when user modules do
            # not need these events
            events = merge_events(base_events, user_events)
        elif event_init:
            logger.debug("using advanced event init")
            # trust that event_init properly calls and merges with library events
            # init_base_events
            # and registers handlers on its own using :func:`events.attach_handlers`
            events = event_init(config_file, config, uuapp_client)
        else:
            assert False

        logger.debug("Registered following events: %s", repr(events))
        if not events:
            raise ValueError("Nothing to do, no defined handlers/events.")
        self._events = events

        self.runev = threading.Event()
        self.stopev = threading.Event()
        self.stopev.set()
        logger.debug("module system initilized")

    def __enter__(self):
        """Call :meth:`.start`."""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Call :meth:`.stop`."""
        self.stop()

    def start(self):
        """Start Gateway and all its associated events.

        Set self.runev, clear self.stopev, invoke all ``@on("start")`` start
        all timers  and wait for all of them to finish.

        This is no-op when the gateway is already started.
        """
        if not self.runev.is_set():
            for ev in self._events:
                ev.start()
            self.runev.set()
            self.stopev.clear()

    def stop(self):
        """Stop Gateway and all its associated events.

        Peacefully stop (wait to finish) all timers and associated
        ``@on("tick")`` handlers, invoke all ``@on("stop")`` handlers and wait
        for all of them to finish.

        This is no-op when the gateway is not running.
        """

        # this also stops on_start function (oneshots) polling for the event
        if self.runev.is_set():
            for ev in self._events:
                ev.stop()
            self.runev.clear()
            self.stopev.set()

    def signal_handler(
        self,
        sig: int,
        frame,
        additional_cleanup: t.Optional[t.Callable[["Gateway"], None]] = None,
    ):
        """Handler for predefined signals.

        The following signals are supported:

        =================   ===========
        functionality no.   description
        =================   ===========
        1                   :meth:`.stop` Gateway, ``del`` ete all modules, run ``additional_cleanup`` and exit
        =================   ===========

        =========== =============
        signal      functionality
        =========== =============
        ``SIGINT``  1
        ``SIGTERM`` 1
        ``SIGUSR1`` 1 and exit with error code ``1``
        ``SIGUSR2`` 1
        =========== =============

        The signals need to be explicitly registered with this method being the
        associated handler. Register signals as:

        .. code-block:: python

            import signal
            from uun_iot import Gateway
            with Gateway(...) as g:
                signal.signal(signal.SIGTERM, g.signal_handler)
                ...

        If you want to specify ``additional_cleanup``, define a partial
        function from this method with first two arguments left empty.

        Args:
            sig: caught signal
            frame: exception frame
            additional_cleanup: optional function to be run to cleanup the
                `Gateway`. The function takes the `Gateway` instance as an
                argument.
        """
        logger.debug("Received signal `%s`", signal.Signals(sig).name)
        if sig in [signal.SIGINT, signal.SIGTERM, signal.SIGUSR1, signal.SIGUSR2]:
            # systemd issues SIGTERM to stop a program
            # user defined signal SIGUSR1 -- is issued from some Module to stop gateway and exit
            self.stop()

            # explicitly delete an event before exiting to give it a chance to execute its __del__
            # and the same for user modules bound to events via handlers
            for ev in self._events:
                del ev

            if additional_cleanup is not None:
                additional_cleanup(self)

            ec = sig in [signal.SIGUSR1]
            # SIGUSR1 -- exit with error
            # SIGUSR2 -- exit without error
            sys.exit(int(ec))


# def old_config_on_tick(self):
#    """
#    Gets new configuration from the uuApp, validates it, restarts timers
#    (if needed based on the new configuration) and saves the new
#    configuration locally. It also notifies modules (via their
#    ``@on("update")``) about configuration update.
#    It is triggered by a tick event.
#    """
#
#    new_config = self._uucmd()
#
#    if not new_config:
#        # did not get a valid configuration
#        return
#
#    if new_config != self.config["gateway"]:
#
#        loggerc.debug("Received new configuration from server: %s", new_config)
#
#        # for loop: restart timers if needed
#        for id, mt in self.g._timers.items():
#            if id not in new_config["moduleTimers"]:
#                continue
#
#            # new timer values are presented
#            if (
#                self.config["gateway"]["moduleTimers"][id]
#                != new_config["moduleTimers"][id]
#            ):
#
#                # if id == "config":
#                #    # TODO: needs testing if utils.Timer correctly handles setting period without stopping first
#                #    mt.timer.period = new_config["moduleTimers"][id]
#                #    loggerc.info(f"experimentally updated `{id}`'s timer to {new_config['moduleTimers'][id]} s")
#                #    continue
#
#                if mt.multi:
#                    # multiple timers for one module
#                    if (
#                        self.config["gateway"]["moduleTimers"][id].keys()
#                        != new_config["moduleTimers"][id].keys()
#                    ):
#                        loggerc.error(
#                            "Update cannot introduce new timer_id for a module, only update timer values."
#                        )
#                        continue
#
#                    for timer_id, new_interval in new_config["moduleTimers"][
#                        id
#                    ].items():
#                        if (
#                            new_interval
#                            != self.config["gateway"]["moduleTimers"][id][timer_id]
#                        ):
#                            mt.timer[timer_id].stop()
#                            mt.timer[timer_id].period = new_config["moduleTimers"][id][
#                                timer_id
#                            ]
#                            mt.timer[timer_id].runonstart = False
#                            mt.timer[timer_id].start()
#                            loggerc.info(
#                                f"updated `{id}:{timer_id}` timer to {new_config['moduleTimers'][id][timer_id]} s"
#                            )
#                else:
#                    # single timer
#                    mt.timer.stop()
#                    mt.timer.period = new_config["moduleTimers"][id]
#                    mt.timer.runonstart = False
#                    mt.timer.start()
#                    loggerc.info(
#                        f"updated `{id}`'s timer to {new_config['moduleTimers'][id]} s"
#                    )
#
#        # update config, only gateway key, rest is unchanged
#
#        # PASSIVE CONFIGURATION UPDATE
#        # propagated passively to each module
#        # modules contain _config in form of config["gateway"] assigned at module's init
#        #   (other keys are not needed and only cause more typing)
#
#        # DOES NOT WORK:
#        # cannot do `self.config["gateway"] = new_config` as it would not change the config["gateway"] dict present in each module:
#        # self.config["gateway"]           --> { 'module_1' --> module_1_data_old, ... }
#        # self.config["gateway"] --(update)--> { 'module_1' --> module_1_data_new, ... }
#        # (some_module)._config            --> { 'module_1' --> module_1_data_old, ... } as
#        #   it was never reassigned inside the module
#
#        # DOES WORK:
#        # update every key(pointer) in config["gateway"] separately; module's _config still points to the same config["gateway"]
#        #   but every key inside config["gateway"] is correctly updated
#        # self.config["gateway"] --> { 'module_1'           --> module_1_data_old, ... }
#        # self.config["gateway"] --> { 'module_1' --(update)--> module_1_data_new, ... }
#        # (some_module)._config  --> { 'module_1'           --> module_1_data_new, ... } as
#        #   the module's config and self.config["gateway"] point to the same (updated object)
#
#        # new update cannot introduce new keys to ["gateway"] (which is to be expected -- cannot create objects at run-time without any defining code)
#        updated_values = False
#        for key in self.config["gateway"]:
#
#            if key not in new_config:
#                loggerc.warning(
#                    "Update does not contain a configuration key `%s`. Update is not deleting this key from current configuration but it will be deleted on next run of application.",
#                    key,
#                )
#                continue
#
#            if self.config["gateway"][key] != new_config[key]:
#                updated_values = True
#                loggerc.debug(
#                    "changed key `%s` from %s to %s",
#                    key,
#                    self.config["gateway"][key],
#                    new_config[key],
#                )
#                self.config["gateway"][key] = new_config[key]
#
#        if not updated_values:
#            loggerc.debug(
#                "New configuration introduced only new keys not present on old config, discarding update."
#            )
#            return
#
#        # allow module callbacks to alter the configuration before saving to disk
#        self._invoke_update_callback()
#
#        # save updated config to file in case of power outage/app restart
#        with open(self._config_file, "w") as f:
#            f.write(
#                json.dumps(self.config, indent=4)
#            )  # pretty print in case of manual editing
#
#        loggerc.info("Updated configuration.")
