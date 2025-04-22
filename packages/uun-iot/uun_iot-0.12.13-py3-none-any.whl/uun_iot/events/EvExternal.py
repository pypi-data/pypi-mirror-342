import itertools
import logging
import typing as t
from dataclasses import dataclass

from ..exceptions import EventCannotRegisterHandler
from ..utils import classproperty
from .Event import Event, EventType, Register

logger = logging.getLogger(__name__)

SelfM = t.Any
F = t.TypeVar("F")


class DuplicateKeyError(ValueError):
    pass


K = t.TypeVar("K")
V = t.TypeVar("V")


@dataclass
class DuplicateKeyErrStruct(t.Generic[K, V]):
    key: K
    current: V
    new: V


def dict_throw_on_duplicate_keys(
    it: t.Iterable[t.Tuple[K, V]],
    init_dict: t.Optional[t.Dict[K, V]] = None,
) -> t.Dict[K, V]:
    if init_dict is None:
        d = {}
    else:
        d = init_dict

    for k, v in it:
        if k in d:
            raise DuplicateKeyError(DuplicateKeyErrStruct(k, d[k], v))
        d[k] = v
    return d


def populate_handlers(
    it: t.Iterable[t.Tuple[K, V]],
    init_dict: t.Optional[t.Dict[K, V]] = None,
    format_err: t.Callable[[DuplicateKeyErrStruct], str] = lambda x: x,
) -> t.Dict[K, V]:
    try:
        return dict_throw_on_duplicate_keys(it, init_dict=init_dict)
    except DuplicateKeyError as e:
        einfo = e.args[0]
        raise ValueError(format_err(einfo)) from e


class EvExternal(Event):
    """
    Event for mediating socket commands. This class acts as an intermediary between the
    socket server and handlers. See :class:`uun_iot.modules.ConfUpdater` for more
    details.

    Examples:

        - configuration:

            .. code-block:: json

                {
                    "gateway": {
                        "socket": {
                            "path-to-socket-file.socket"
                        }
                    }
                }

        .. code-block:: python

            from uun_iot import EvExternal

            class ExternallyControlledModule:
                @EvExternal.subscribe_command("action1")
                def handle_cmd(self, msg):
                    cmd, msg = msg
                    assert(cmd == "action1")
                    print(msg)

            >>> echo "action1 This message was created outside of the main Python app." | nc -U path/to/unix/socket.sock
            >>> # handle_cmd is called and prints
            >>> 'This message was created outside of the main Python app.'
    """

    event_type = EventType.EXTERNAL
    _handlers: t.Dict[str, t.Callable]

    def __init__(self, config=None):
        self._handlers = {}
        super().__init__(config=None)

    @classmethod
    def subscribe_command(cls, action_id: str, *subactions: str):
        """Subscribe to socket command.

        The handler is passed positional argument ``msg`` as a tuple ``(cmd, rest_msg)``,
        where cmd is the issued command and ``rest_msg`` is the rest of the
        message received by socket IPC

        Specifying subactions is functionally equivalent to naming the action as ``action_id[subaction1,subaction2,...]``

        Args:
            action_id: string identifier of action
            subactions: optionally specify sub-commands
        """
        if not isinstance(action_id, str):
            raise EventCannotRegisterHandler("Only string action IDs are supported.")
        sub = f"[{','.join(subactions)}]" if subactions else ""
        return cls._register(
            Register[
                t.Callable[[SelfM, t.Tuple[str, t.Optional[str]]], t.Optional[str]]
            ],
            action_id + sub,
        )

    def add_handlers(self, handler_list):
        self._handlers = populate_handlers(
            ((info.args[0], fn) for fn, info in handler_list),
            init_dict=self._handlers,
            format_err=lambda einfo: f"Encountered duplicate entry for @EvExternal.subscribe_command, id '{einfo.key}'",
        )

    def get_handler(
        self, action_id: str
    ) -> t.Optional[t.Callable[[t.Tuple[str, t.Optional[str]]], t.Optional[str]]]:
        """Get handler with action_id, if exists.

        Args:
            action_id: identifier of handler
        """
        return self._handlers.get(action_id)

    def start(self):
        """Noop"""
        logger.debug(
            "EvExternal has these handlers registered: %s", repr(self._handlers)
        )

    def stop(self):
        """Noop"""
        pass
