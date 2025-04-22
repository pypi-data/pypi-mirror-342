"""Initialize modules."""

import json
import logging
import typing as t

from uun_iot.UuAppClient import UuAppClient

from ..events import (EvConfUpdate, Event, EvExternal, EvTick, attach_handlers,
                      merge_events)
from ..utils import maybe_get_instance
# from .BaseHealthCheck import register_basehealthcheck
from .ConfigUpdater import ConfigUpdater
from .Heartbeat import Heartbeat
from .SocketServer import SocketServer

logger = logging.getLogger(__name__)
loggerc = logging.getLogger(__name__ + "ConfigUpdaterUucmd")


def init_library_module_events(
    config_path: t.Optional[str],
    config: t.Dict,
    uuclient: UuAppClient,
    events: t.Optional[t.Iterable[Event]] = None,
) -> t.Iterable[Event]:
    full_config = config
    config = config["gateway"] if "gateway" in config else config
    modules = []

    ev_confupdate = maybe_get_instance(EvConfUpdate, events) or EvConfUpdate(
        full_config
    )
    ev_tick = maybe_get_instance(EvTick, events) or EvTick(full_config)
    ev_external = maybe_get_instance(EvExternal, events) or EvExternal(full_config)
    evs = [ev_confupdate, ev_tick, ev_external]

    ### ConfigUpdater
    endpoint_uucmd_config = (
        full_config.get("uuApp", {})
        .get("uuCmdList", {})
        .get("gatewayGetConfiguration", None)
    )
    if endpoint_uucmd_config:

        def uucmd_config_update():
            # create uucmd function, separate from other cmd due to nature of Config
            r, exc = uuclient.get(endpoint_uucmd_config, log_level=logging.DEBUG)
            if r is None or exc is not None:
                return None

            try:
                new_config = r.json()
                # this is not an actual configuration key, only a remnant of server communication
                if "uuAppErrorMap" in new_config:
                    del new_config["uuAppErrorMap"]
                if not new_config:
                    loggerc.debug(
                        "Received empty JSON configuration from server, ignoring."
                    )
                    return None
            except json.decoder.JSONDecodeError:
                loggerc.warning("Received invalid configuration JSON from server")
                loggerc.debug("Invalid response: %s", r.text)
                return None

            return new_config

        def save_config_to_file(config):  # -> bool:
            if config_path is None:
                return  # False
            try:
                with open(config_path, "w") as f:
                    f.write(json.dumps(config, indent=4))
                    return  # True
            except:
                return  # False

        def update_callback(new_config):
            ev_tick.update(new_config)
            ev_confupdate.fire_handlers(new_config, block=False)

        modules.append(
            ConfigUpdater(
                full_config, uucmd_config_update, save_config_to_file, update_callback
            )
        )

    ### SocketServer
    try:
        modules.append(SocketServer(config, ev_external))
        logger.info("socket server successfuly initialized")
    except ValueError as er:
        logger.info("socket server was not initialized: %s", str(er))

    ### Heartbeat
    endpoint_uucmd_heartbeat = (
        full_config.get("uuApp", {}).get("uuCmdList", {}).get("gatewayHeartbeat", None)
    )
    if endpoint_uucmd_heartbeat:

        def uucmd_heartbeat(dto_in):
            resp, exc = uuclient.post(
                endpoint_uucmd_heartbeat, dto_in, log_level=logging.DEBUG
            )
            if exc is None:
                return resp
            return None

        modules.append(Heartbeat(uucmd_heartbeat))

    all_evs = attach_handlers(full_config, modules, evs)
    # all_evs does not containg EvExternal as none of the base modules directly
    # subscribe to it - attach_handlers does not find it in the passed modules.
    # Instead, the SocketServer indirectly uses it so we need to
    # forcefully include it in returned events so that user modules subscribing to
    # EvExternal get the same instance of the event which was registered with SocketServer
    return merge_events(all_evs, evs)
