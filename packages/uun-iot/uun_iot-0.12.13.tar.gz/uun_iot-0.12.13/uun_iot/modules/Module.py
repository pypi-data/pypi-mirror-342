import itertools
import logging
import typing as t
from enum import Enum, auto
from typing import Any, Callable, List, Optional, Union

from uun_iot.events import (EvConfUpdate, EventType,
                            extract_event_handlers_from_object)
from uun_iot.utils import (Storage, _get_dict_path, canonical_id_from_str,
                           instance_ids)

logger = logging.getLogger(__name__)


class ConfigScopeEnum(Enum):
    """Enumeration for configuration scopes."""

    #: Use the root ``gateway`` key for the module configuration.
    GATEWAY = auto()

    #: Use the ``gateway.moduleId`` key for the module configuration.
    MODULE = auto()

    #: Use custom base for the configuration manager.
    BASED = auto()


class Module:
    """Provides utility functions for modules.

    Class :class:`Module` implements interface :class:`uun_iot.typing.IModule`
    for derived classes automatically. The :attr:`id` attribute is derived from
    the class name using :func:`uun_iot.utils.module_id_from_str`. If the class
    already has the :attr:`id` attribute, keep it.

    The derived classes must call the :class:`Module`'s init function using :func:`super`. Example:

    .. code-block:: python

        from uun_iot import Module
        class TestModule(Module):
            def __init__(self, config, uucmd):
                super().__init__(config=config, uucmd=uucmd)
                self.attribute1 = "value1"

    The utility functions include:

        - configuration management
        - storage management
        - backup and restore of storage to filesystem (useful for power failures)
        - automation for sending storage to uuApp
        - handling of failed send storage actions (useful for unstable internet connection)

    Configuration management:

        Access configuration in easy way as ``self._c("key/subkey/subsubkey")``
        instead of cumbersome ``self._config["key"]["subkey"]["subsubkey"]`` and more.
        See configuration manager :meth:`._config_manager` or its alias :meth:`._c`.

    Storage management:

        An instanced thread-safe :class:`~uun_iot.utils.Storage` is available as
        :attr:`._storage`. The class provides backup and restore to
        JSON files and limiting the storage in number of its entries. If
        enabled, oldest entries will be removed for the sake of newer ones.

    If the derived class does not have the ``_config`` attribute, set it to the
    constructor argument ``config``.

    Args:
        uucmd: function(storage)->failed_send_data to send data to uuApp server
        config: gateway configuration
    """

    #: is set in :meth:`__init__` dynamically according to derived class
    id: str

    #: optional uuCmd function for data sending
    _uucmd: Optional[Callable[..., List]]
    #: gateway configuration
    _config: dict

    #: custom base key for accessing config via config manager
    _config_manager_base: t.Optional[str]

    #: storage facility
    _storage: t.Optional[Storage]

    def __init__(
        self,
        config: t.Optional[dict] = None,
        *,
        uucmd: t.Optional[Callable[[Any], List]] = None,
        storage: t.Union[t.Optional[Storage], bool] = True,
    ):

        self._uucmd = uucmd

        canon_id, real_id = instance_ids(self)
        self.id = real_id

        if config is None:
            config = {}
        self._config = config
        self._config_manager_base = None

        # load backup file with previous data
        # if module is supposed to be backed up
        self._storage = None
        if storage is True:
            self._storage = self._init_storage()
        elif storage:
            self._storage = storage

        # register config update handler if not already specified by user
        extracted = extract_event_handlers_from_object(self)
        registered = any(
            einfo.event_type == EventType.CONF_UPDATE for _, einfo in extracted
        )
        if not registered:
            logger.info(
                "registering default configuration update handler for module '%s'",
                self.id,
            )
            self._on_config = EvConfUpdate.subscribe(self._update_config).extract()  # type: ignore

    def _init_storage(self) -> Storage:
        """Initialize storage.

        Look into configuration and initialize storage. If specified, apply backup and
        storage limiting.
        """
        if (
            "moduleBackupStorage" in self._config
            and self.id in self._config["moduleBackupStorage"]
        ):
            try:
                backup_path = self._config["moduleBackupStorage"][self.id]["path"]
                storage_limit = self._config["moduleBackupStorage"][self.id]["limit"]
                if not isinstance(storage_limit, int):
                    logger.warning(
                        "Configuration for `%s`: "
                        "limit of 'gateway.moduleBackupStorage' must be an integer.",
                        self.id,
                    )
                    raise TypeError
            except (KeyError, TypeError):
                backup_path = self._config["moduleBackupStorage"][self.id]
                storage_limit = 0
        else:
            backup_path = None
            storage_limit = 0

        return Storage(self.id, backup_path, storage_limit)

    # dynamic @EvConfUpdate.subscribe
    def _update_config(self, new_config: dict):
        """Update configuration.

        Default handler to update configuration stored in ``._config``. Handler is not
        active if user specifies their own handler.

        This is dynamically registered by EvConfUpdate if no user handler is detected.

        Warning:

            Changing storage characteristics (such as backup and storage limit) throught
            configuration update is not supported at the moment. Restart the app to
            apply config changes.

        Args:
            new_config: received gateway configuration from server
        """
        self._config = new_config

    def _set_config_manager_base(self, base: t.Optional[str]):
        """Does not check for validity of :attr:`base`.

        Set to None to reset to default, module-centric base."
        """
        self._config_manager_base = base

    def _config_manager(
        self,
        key: Optional[str] = None,
        scope: ConfigScopeEnum = ConfigScopeEnum.BASED,
        must_exist: bool = True,
    ) -> Any:
        """Return configuration key based on scope.

        When a custom base is specified via call to
        :meth:`Module._set_config_manager_base(new_base)`, config manager now operates
        with :attr:`key` relative to this :attr:`new_base` When the base is not set, it
        acts like MODULE e.g. when ``mySubkey/NextSubkey`` is set as a base and config
        manager is called with ``key="myValue"``, it returns value from configuration
        located at ``mySubkey/NextSubkey/myValue``

        See arguments for more information.

        Examples:

            Following example JSON configuration file with Python outputs:

            .. code-block:: json

                {
                    "gateway": {
                        "testModule1": {
                            "option1": "value1",
                            "structure": {
                                "field1": 1,
                                "field2": {
                                    "nested": 2
                                }
                            }
                        },

                        "testModule2": {
                            "option2": "value2"
                        }
                    }

            .. code-block:: python

                from uun_iot import ConfigScopeEnum

                # inside of a method of class TestModule1 derived from Module
                print(self._c("option1"))
                >>> value1

                print(self._c("structure/field1/nested"))
                >>> 2

                self._set_config_manager_base("testModule1/structure")
                print(self._c("field1/nested"))
                >>> 2

                print(self._c("option1", scope=ConfigScopeEnum.MODULE))
                >>> value1

                print(self._c("testModule1/option1", scope=ConfigScopeEnum.GATEWAY))
                >>> value1

                print(self._c("testModule2/option2", scope=ConfigScopeEnum.GATEWAY))
                >>> value2

        Warning:

            This cannot be used to address config keys which have '/' inside the actual
            key. Also, refrain of using :attr:`self.id` containing the slash as this
            config lookup will not behave properly.

        Args:
            key: specify value of configuration key to read. Set to ``None`` to
                return whole dictionary of corresponding configuration given by
                ``scope``. delimit subdictionaries with ``/`` symbol, ie.
                ``self._c("color/bright/red")`` is the same as
                ``self._c("color")["bright"]["red"]``

            scope: the root of configuration ``scope`` can be any of
                :class:`ConfigScopeEnum`.
                When :attr:`ConfigScopeEnum.MODULE`, ie.
                ``key`` is taken as a subkey of ``gateway.<moduleId>``.
                Alternatively, specify :attr:`ConfigScopeEnum.GATEWAY` to take ``key``
                as subkey of ``gateway`` key.
                See description for more.

            must_exist: if the given key does not exist in configuration given by
                arguments above, the function will throw error when `must_exist=True`
                (default). Otherwise, it returns None.

        Returns:
            Any: the configuration entry

        Raises:
            KeyError: when a given key does not exist inside the configuration
        """

        if scope == ConfigScopeEnum.BASED:
            set_base = self._config_manager_base
            base_idx = set_base if set_base is not None else self.id
        elif scope == ConfigScopeEnum.MODULE:
            base_idx = self.id
        elif scope == ConfigScopeEnum.GATEWAY:
            base_idx = None
        else:
            if must_exist:
                raise ValueError(f"Invalid scope `{scope}`.")
            else:
                return None

        return _get_dict_path(
            self._config, key_pieces=[base_idx, key], must_exist=must_exist
        )

    def _send_data(
        self, data: Union[List, Any], usecase: t.Optional[t.Callable] = None
    ):
        """Logging wrapper for sending ``data`` with ``usecase`` function.

        Log a message with INFO level with information about the data, then send the data.

        Args:
            data: data to be sent by usecase as ``usecase(data)``
            usecase: if ``None``, use stored :attr:`._uucmd`

        Raises:
            TypeError: if ``usecase`` is not specified and ``self._uucmd`` is also not specified
        """
        if usecase is None:
            usecase = self._uucmd
        if usecase is None:
            raise TypeError(
                f"No usecase was specified and the module `{self.id}` "
                "has no stored uucmd."
            )

        try:
            length = len(data)
            logger.info(
                "Sending data object for `%s` with [%i] entries", self.id, length
            )
        except TypeError:
            logger.info("Sending data object for `%s`", self.id)

        usecase(data)

    def _send_storage(self, usecase: Optional[Callable[[List], List]] = None):
        """Sends entire storage of module to uuApp via ``usecase`` or stored :attr:`uucmd`.

        The ``usecase`` takes data and outputs items which failed to be sent.
        This method saves these failed attempts to file and retries again
        together with new data on next envocation. Only failed entries will be
        saved to the backup file. This functionality is independent on the
        backup functionality.

        Args:
            usecase: function ``List->List`` with one argument taking the data
            to be sent and outputting list with items which were not sent. If
            ``None``, use ``self._uucmd``

        Raises:
            TypeError: if ``usecase`` is not specified and ``self._uucmd`` is also not specified
        """

        if self._storage.is_empty():
            # no data to send
            return

        if usecase is None:
            usecase = self._uucmd
        if usecase is None:
            raise TypeError(
                f"No usecase was specified and the module `{self.id}` "
                "has no stored uucmd."
            )

        # prevent situation, where data are sent, another thread writes data to
        # storage, and (as a consequence of sending data) storage is emptied
        # thus discarding the latest unsent data
        with self._storage.write_lock:
            length = len(self._storage)
            logger.info("Sending storage of `%s` with [%i] entries", self.id, length)

            failed_entries = usecase(self._storage.data)
            self._storage.empty()

        if not self._storage.has_backup:
            # do not backup
            return

        if len(failed_entries) == 0:
            # everything was sent
            logger.info("Whole storage of `%s` sent successfully", self.id)
        else:
            # merge the two objects (chronologically) to prevent discarding
            # entries added to ._storage while previus ones were being
            # processed/sent

            # extend the storage with entries of the failed_entries list
            self._storage.merge(failed_entries, new_data=False)
            logger.warning(
                "Could not send %i entries from storage of `%s`",
                len(failed_entries),
                self.id,
            )

    _c = _config_manager
