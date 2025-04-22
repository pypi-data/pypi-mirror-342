import collections
import itertools
import json
import logging
import os
import threading
import time
import typing as t
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .typing import ModuleId

T = t.TypeVar("T")
V = t.TypeVar("V")


def canonical_id_from_str(module_name: str) -> str:
    """Create module ID from module name string.

    The format is: first letter lowercase.

    Examples:
        - `Hearbeat` -> ``heartbeat``
        - `WeatherConditions` -> ``weatherConditions``

    Args:
        module_name: module name

    Returns:
        str: formatted module ID
    """
    return module_name[0].lower() + module_name[1:]


def class_ids(cls) -> Tuple[ModuleId, ModuleId]:
    """Return canonical and real IDs of a class.

    Canonical ID is created using :func:`canonical_id_from_str` on class name
    and real ID is class's :attr:`id` attribute if defined, otherwise canonical id.

    Args:
        cls: class or instance of a class

    Returns:
        str: cls ID is created from ``cls.__name__`` attribute
    """
    canon_id = canonical_id_from_str(cls.__name__)
    real_id = cls.id if hasattr(cls, "id") else None
    if not isinstance(real_id, str):
        real_id = canon_id
    return canon_id, real_id


def instance_ids(instance) -> Tuple[ModuleId, ModuleId]:
    """Same as :func:`class_ids` except this operates on instantiated class objects,
    ie. instance = Class()"""
    canon_id = canonical_id_from_str(instance.__class__.__name__)
    real_id = instance.id if hasattr(instance, "id") else None
    if not isinstance(real_id, str):
        real_id = canon_id
    return canon_id, real_id


def groupby_unsorted(
    seq: t.Sequence[T], key: t.Callable[[T], V] = lambda x: x
) -> t.Iterable[t.Tuple[V, t.Iterable[T]]]:
    """Group sequence elements by the same key."""
    # https://code.activestate.com/recipes/580800-groupby-for-unsorted-input/
    indexes = collections.defaultdict(list)
    for i, elem in enumerate(seq):
        indexes[key(elem)].append(i)
    for k, idxs in indexes.items():
        yield k, (seq[i] for i in idxs)


def groupby_unsorted_tup(
    seq: t.Sequence[t.Tuple[V, T]],
) -> t.Iterable[t.Tuple[V, t.Iterable[T]]]:
    """Group sequence of tuples (key, value) into groups of values by key."""
    for key, items in groupby_unsorted(seq, key=lambda x: x[0]):
        yield key, [tup[1] for tup in items]


def maybe_get_instance(
    clas: t.Type[T], iterable: t.Optional[t.Iterable]
) -> t.Optional[T]:
    """Get first occurence of instance of :attr:`clas` in :attr:`iterable`.

    If not present, return None.

    Args:
        clas: class to filter in iterable
        iterable: the iterable
    """
    if iterable is None:
        return None
    return next(filter(lambda inst: isinstance(inst, clas), iterable), None)


def file_save(path: str, data: Union[List, Dict]) -> bool:
    """Save data to file in JSON.

    Args:
        path: file path
        data: dictionary or list with data

    Returns:
        bool: `True` if saved, `False` if file already contains the same data as passed
    """

    # prevent writing to file if not neccesarry (if power wents out at exact
    # moment, file might be empty)
    if os.path.isfile(path) and os.stat(path).st_size > 0:  # not empty file
        with open(path, "r") as f:
            file_json = json.load(f)
            if json.loads(json.dumps(data)) == file_json:  # force serialization on data
                return False  # do nothing, file contains the same (currently retrying)

    # save new data
    with open(path, "w") as json_data_file:
        json_data_file.write(json.dumps(data))

    return True


def get_iso_timestamp(dt: datetime) -> str:
    """Create ISO timetamp from given datetime object. If not timezone info is
    specified, treat as UTC.

    Args:
        dt: :class:`datetime.datetime` object

    Returns:
        str: corresponding ISO timestamp
    """
    if dt.tzinfo is None:
        # if no timezone specified, assume it is UTC
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    else:
        # convert to UTC first
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def get_datetime_from_iso_timestamp(iso_timestamp: str) -> datetime:
    """Create datetime object from given ISO timetamp .

    Args:
        iso_timestamp: ISO timestamp

    Returns:
        datetime: corresponding :class:`datetime.datetime` object
    """
    return datetime.strptime(iso_timestamp, "%a, %d %b %Y %H:%M:%S %Z")


# class classproperty:
#    def __init__(self, func):
#        self.fn = func
#    def __get__(self, instance, owner):
#        return self.fn(owner)

PropReturn = t.TypeVar("PropReturn")

if t.TYPE_CHECKING:

    def classproperty(meth: t.Callable[..., PropReturn]) -> PropReturn:
        """Access a @classmethod like a @property."""
        # mypy doesn't understand class properties yet: https://github.com/python/mypy/issues/2563
        return classmethod(property(meth))  # type: ignore
        # return meth # type: ignore

else:
    # class classproperty:
    #    def __init__(self, func):
    #        self.fn = func

    #    def __get__(self, instance, owner):
    #        return self.fn(owner)

    class classproperty(property):
        def __get__(self, obj, objtype=None):
            return super().__get__(objtype)


class LoggingSystemdHandler(logging.StreamHandler):
    """Severity information for stdout&stderr logging. See SD-DAEMON(3)"""

    PREFIX = {
        # EMERG <0>
        # ALERT <1>
        logging.CRITICAL: "<2>",
        logging.ERROR: "<3>",
        logging.WARNING: "<4>",
        # NOTICE <5>
        logging.INFO: "<6>",
        logging.DEBUG: "<7>",
        logging.NOTSET: "<7>",
    }

    def emit(self, record):
        try:
            msg = self.PREFIX[record.levelno] + self.format(record)
            msg = msg.replace("\n", "\\n")  # Tracebacks on single line
            self.stream.write(msg + "\n")
            self.stream.flush()
        except Exception:
            self.handleError(record)


logger_rt = logging.getLogger(__name__ + ".RepeatTimer")


class RepeatTimer:
    """Periodically run function with unlimited repetition.

    Start the timer by executing :meth:`.start`. The timer can be interrupted
    at any time by issuing :meth:`.stop`.

    It is possible to :meth:`.stop` the timer, directly set different :attr:`period` or
    :attr:`runonstart` and :meth:`.start` again. But be sure to STOP before changing
    these values. Any exceptions raised in :attr:`f` will be logged with ERROR log
    level using `logging` library together with stacktrace. This will NOT stop
    the timer.

    Warning:
        Any exception occuring in the function :attr:`f` is catched and logged,
        ie. exceptions occuring in the function will not stop the timer.

    Args:
        period: period between timer ticks, in seconds
        f: function to be executed
        args: positional arguments to be passed to ``f``
        kwargs: keyword arguments to be passed to ``f``
        runonstart: default to `True` -- make the first execution of ``f`` right after
            calling :meth:`.start` (without waiting first for ``period``)
    """

    _period: float
    _runonstart: bool
    _f: Callable
    _args: List
    _kwargs: Dict
    _stopev: threading.Event

    def __init__(
        self,
        period: float,
        f: Callable,
        args: List = [],
        kwargs: Dict = {},
        runonstart: bool = True,
    ):
        self._period = period
        self._runonstart = runonstart

        self._f = f
        self._args = args
        self._kwargs = kwargs

        # stop event to abort wait (would be time.sleep) in while loop
        self._stopev = threading.Event()
        self._stopev.set()

    @property
    def period(self) -> float:
        return self._period

    @period.setter
    def period(self, new) -> None:
        if not self._stopev.is_set():
            raise RuntimeError("Stop the timer before setting `period`.")
        self._period = new

    @property
    def runonstart(self) -> bool:
        return self._runonstart

    @runonstart.setter
    def runonstart(self, new) -> None:
        if not self._stopev.is_set():
            raise RuntimeError("Stop the timer before setting `runonstart`.")
        self._runonstart = new

    def start(self):
        """Start the timer."""
        # make timer possible to restart again
        self._stopev.clear()
        self._t = threading.Thread(target=self._do_every)
        self._t.start()

    def stop(self, block: bool = True):
        """Stop the timer.

        Can be set to block until current execution of :attr:`.f` is finished.

        Args:
            block: If ``block`` is `True`, block until currently executed
                function is finished. Default to `True`.
        """
        self._stopev.set()
        # race conditions
        if block and self._t.is_alive():
            self._t.join()

    def _do_every(self):
        def sleep_sequence():
            t = time.time()
            while True:
                t += self._period
                yield max(t - time.time(), 0)

        s = sleep_sequence()

        # first wait
        if not self._runonstart:
            self._stopev.wait(next(s))

        # while stop was not called
        while not self._stopev.is_set():
            try:
                self._f(*self._args, **self._kwargs)
            except Exception as e:
                logger_rt.exception(
                    "Function [%s] thrown an error: [%s]. See stacktrace. ",
                    self._f,
                    str(e),
                )

            # wait for stopevent for next(s) seconds
            self._stopev.wait(next(s))


def _get_dict_path(
    dic: dict, key_pieces: t.Sequence[t.Optional[str]], must_exist: bool
):
    """See get_dict_path for high-level usage."""
    current_key = []
    path_parts = itertools.chain.from_iterable(
        map(
            lambda path: path.split("/"),
            filter(None, key_pieces),
        )
    )
    for subkey in path_parts:
        current_key.append(subkey)
        try:
            dic = dic[subkey]
        except KeyError as e:
            if must_exist:
                raise KeyError(
                    f"key `{'/'.join(current_key)}` is not present in configuration"
                ) from e
            else:
                return None
    return dic


def get_dict_path(dic: t.Dict[str, t.Any], key: str, must_exist: bool = True) -> t.Any:
    """
    Navigate nested dictionary, every slash '/' in key denotes nesting.
    Dict must have string keys not containing '/'.
    When must_exist is True (default), KeyError is raised for non-existent keys.

    Example:

        .. code-block:: python

            get_dict_path("hello/there/you", { "hello": {"something": 0, "there": {"you": 42}} })
            >>> 42
            get_dict_path("hello/there", { "hello": {"something": 0, "there": {"you": 42}} })
            >>> {"you": 42}
    """
    return _get_dict_path(dic, key_pieces=key.split("/"), must_exist=must_exist)


logger_st = logging.getLogger(__name__ + ".Storage")


class Storage:
    """Storage providing thread-safe utility functionality.

    This class provides:

        - basic thread-safe storage centered around Python's ``list``
        - backup and restore the storage to JSON files
        - limiting the storage to a number of entries. If enabled, the oldest
          entries are discarded. Newest entries are the ones stored at the end
          of the list.

            - as the limited storages are typically small in size (~100), no
              optimization is done for the sake of code simplicity. The
              ``list``'s removal from the left is ``O(n)`` where ``n`` is the
              size of the storage. If you need bigger limited storages,
              consider double ended queue ``deque``.

    Args:
        storage_id: identifier used only for logging purposes
        backup_path: location of backup JSON file. Pass ``None`` to turn off
            file backups. It will automatically create empty directories and
            create the backup file, if the path does not exist. If it exists,
            load data into storage from file.
        maxlen: maximum number of entries in the storage. Oldest entries are
            replaced by newer ones. Pass ``0`` to make the storage unlimited.
    """

    #: writing lock :class:`threading.Lock` can be used for more complex
    #: operations outside this class and is public
    write_lock: threading.Lock

    #: storage id, used for logging
    _sid: str
    #: max length of the storage
    _maxlen: int
    _data: List
    _backup_path: Optional[str]

    def __init__(self, storage_id: str, backup_path: Optional[str], maxlen: int = 0):
        self.write_lock = threading.Lock()

        self._sid = storage_id
        self._maxlen = maxlen

        self._data = []

        self._backup_path = backup_path
        if not self._backup_path:
            return

        os.makedirs(os.path.dirname(self._backup_path), exist_ok=True)
        if os.path.exists(self._backup_path):
            with open(self._backup_path, "r") as f:
                try:
                    data = json.load(f)
                except json.decoder.JSONDecodeError:
                    data = []
                    logger_st.warning(
                        "Backup file %s is not a valid JSON file.", self._backup_path
                    )
                    return

            if data:
                self._data = data
                logger_st.debug(
                    "Backup file `%s` for `%s` loaded successfully with [%i] entries",
                    self._backup_path,
                    self._sid,
                    len(data),
                )
            else:
                logger_st.debug(
                    "Nothing to load from backup file `%s` for `%s`",
                    self._backup_path,
                    self._sid,
                )

        else:
            with open(self._backup_path, "w") as f:
                f.write("[]")
            logger_st.debug("Created new backup file for `%s`", self._sid)

    def __len__(self):
        return len(self._data)

    @property
    def data(self) -> List:
        """The stored data list."""
        return self._data

    def has_backup(self) -> bool:
        """Is this storage backed up?"""
        return self._backup_path is not None

    def append(self, data: Any, backup: bool = False) -> None:
        """Append a piece of new data to the storage list. Thread-safe.

        There is an option to backup the storage directly after the append.
        Default is to not back up to file, because of the unnecessary IO
        overhead.

        Args:
            data: data to be appended using :meth:`self.data.append`
            backup: backup the storage to the file after appending. Defaults to ``False``.
        """
        with self.write_lock:
            self._data.append(data)
            self.trim()
            if backup:
                self._save_to_disk()

    def merge(self, data: List, new_data: bool = True, backup: bool = True) -> None:
        """Merge another list with the storage. Thread-safe.

        Chronologically merge data with storage. Defaults to file backup after
        the operation, if enabled in constructor.

        Args:
            data: another list to merge with the data.
            new_data: Value ``True`` means ``data`` are newer than whole
                content of the storage and are stored at the end of the storage.
                This is assumed by default. Value ``False`` merges the data at the
                beginning of the storage. This is important when storage limit is
                imposed, as the oldest entries will be deleted when the total number
                of entries is greater that the limit.
            backup: backup the storage to the file after appending. Defaults to ``True``.

        """
        with self.write_lock:
            if new_data:
                self._data = self._data + data
            else:
                self._data = data + self._data
            self.trim()
            if backup:
                self._save_to_disk()

    def is_empty(self) -> bool:
        """Is the storage an empty list ``[]``?"""
        return self._data == []

    def empty(self) -> None:
        """Empty the storage and empty the backup file."""
        logger_st.debug("Emptying storage `%s`.", self._sid)
        self._data = []
        self._save_to_disk()

    def trim(self) -> None:
        """Trim the storage size to the limit ``limit``.

        Only ``limit`` last entries of the storage are kept, rest is deleted.

        Do not trim if the ``limit`` is not set (is zero).
        """
        # equivalent even for edge cases in condition below
        # slen = len(self)
        # if self._limit > 0 and slen > self._limit:
        # del self._storage[:-self._limit]

        # keep last self._limit newest entries
        del self._data[: -self._maxlen]

    def _save_to_disk(self):
        """Save the storage to disk.

        Saves the storage to backup path, if specified. Otherwise, do nothing.
        """
        if self._backup_path:
            if file_save(self._backup_path, self._data):
                logger_st.debug("Saving storage of `%s` to backup file.", self._sid)
            else:
                logger_st.debug("Storage already saved, doing nothing.")
