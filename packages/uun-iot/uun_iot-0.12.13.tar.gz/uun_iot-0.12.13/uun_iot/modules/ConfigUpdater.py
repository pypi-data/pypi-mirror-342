import copy
import logging
import typing as t

from ..events import EvTick
from ..typing import ModuleId

logger = logging.getLogger(__name__)


class ConfigUpdater:
    """Configuration update module.

    Gets new configuration from the uuApp, validates it, calls supplied callbacks on config update, restarts timers
    (if needed based on the new configuration) and saves the new
    configuration locally. It also notifies modules (via their
    ``@EvUpdate``) about configuration update.
    It is triggered by a tick event.

    update config, only gateway key, rest is unchanged

    PASSIVE CONFIGURATION UPDATE
        propagated passively to each module
        modules contain _config in form of config["gateway"] assigned at module's init
          (other keys are not needed and only cause more typing)

    DOES NOT WORK:
        cannot do `self.config["gateway"] = new_config` as it would not change the gconfig=config["gateway"] dict present in each module:

        >>> config = {"gateway": {"key": 1}}
        >>> sub = config["gateway"]
        >>> id(config)
        136617035769600
        >>> id(config["gateway"])
        136617037635904
        >>> id(sub)
        136617037635904
        >>> config["gateway"] = {"new": 2} # new dictionary {new: 2} is created in memory and reference saved in config["gateway"]
        >>> id(config)
        136617035769600
        >>> id(config["gateway"])
        136617035590272
        >>> id(sub)
        136617037635904
        >>> sub
        {'key': 1}

        self.config["gateway"]           --> { 'module_1' --> module_1_data_old, ... }
        self.config["gateway"] --(update)--> { 'module_1' --> module_1_data_new, ... }
        (some_module)._config            --> { 'module_1' --> module_1_data_old, ... } as
          it was never reassigned inside the module

    DOES WORK:
        update every key(pointer) in config["gateway"] separately; module's _config still points to the same config["gateway"]
          but every key inside config["gateway"] is correctly updated
        self.config["gateway"] --> { 'module_1'           --> module_1_data_old, ... }
        self.config["gateway"] --> { 'module_1' --(update)--> module_1_data_new, ... }
        (some_module)._config  --> { 'module_1'           --> module_1_data_new, ... } as
          the module's config and self.config["gateway"] point to the same (updated object)

    Args:
        config: IMPORTANT: pass whole configuration, not just `gateway` key.
            This module saves new configuration to file.
        uucmd_update: [TODO:description]
        update_config_callback: new configuration (only the "gateway" subkey) will be
            passed to this function.
    """

    id: ModuleId = "config"

    def __init__(
        self,
        config: t.Dict,
        uucmd_update: t.Callable[[], t.Optional[t.Dict]],
        save_config: t.Callable[[t.Dict], None],
        update_config_callback: t.Callable[[t.Dict], None],
    ):
        if "gateway" not in config:
            raise ValueError(
                "ConfigUpdater operates on the whole configuration, do not pass only the 'gateway' key"
            )
        self._config = config
        self._save_config = save_config
        self._uucmd = uucmd_update
        self._update_callback = update_config_callback

    @EvTick.subscribe
    def update_config(self):
        fetched_config = self._uucmd()

        # if True, do not discard now non-existent keys in new config
        nondecremental_update = False
        if "nondecrementalUpdate" in self._config["gateway"] and self._config["gateway"]["nondecrementalUpdate"]:
            nondecremental_update = True

        # avoid mutating reference in existing configs
        dup_config = copy.deepcopy(self._config)
        if not fetched_config or fetched_config == dup_config["gateway"]:
            return

        if nondecremental_update:
            gconf: dict = dup_config["gateway"]
            gconf.update(fetched_config)
            dup_config["gateway"] = gconf
        else:
            dup_config["gateway"] = fetched_config

        #for key in dup_config["gateway"]:
        #    if key not in fetched_config:
        #        logger.warning(
        #            "Update does not contain a configuration key `%s`."
        #            " Update is not deleting this key from current configuration"
        #            " but it will be deleted on next run of application.",
        #            key,
        #        )
        #        continue

        #    if dup_config["gateway"][key] != fetched_config[key]:
        #        logger.debug(
        #            "changed key `%s` from %s to %s",
        #            key,
        #            dup_config["gateway"][key],
        #            fetched_config[key],
        #        )
        #        dup_config["gateway"][key] = fetched_config[key]

        # self._config["gateway"] = new_config # passive update
        # self._config = {"gateway": new_config} # decouple
        self._config = dup_config
        self._save_config(self._config)
        self._update_callback(self._config["gateway"])
