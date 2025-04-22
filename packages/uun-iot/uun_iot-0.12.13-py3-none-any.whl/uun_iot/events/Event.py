import logging
import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum, auto

from ..exceptions import EventException, InvalidModuleId
from ..typing import ModuleId
from ..utils import class_ids, instance_ids

logger = logging.getLogger(__name__)


EVENT_KEY = "_uuniot"


class EventType(IntEnum):
    START = auto()
    STOP = auto()
    CONF_UPDATE = auto()
    TICK = auto()
    EXTERNAL = auto()


# TODO: save _HandlerInfoInternal along with method
# turn it to HandlerInfo on extraction
# this would simplify the saving logic (as it does not have to use __set__name__ class
# handler)
@dataclass
class _HandlerInfoInternal:
    event_type: EventType
    args: t.Tuple
    kwargs: t.Dict


@dataclass
class HandlerInfo:
    event_type: EventType
    args: t.Tuple
    kwargs: t.Dict
    owner_id: ModuleId


F = t.TypeVar("F", bound=t.Callable)
FT = t.TypeVar("FT", bound=t.Callable)
V = t.TypeVar("V")


# no idea why this works (with regard to typing) and the simpler function approach does not
class Register(t.Generic[F]):
    """
    Workaround till Python 3.12 which offers parametric functions Descriptor
    cannot be parametrized as it is outside of scope and passing t.Callable as
    argument of type Type[T] does not work in typecheckers
    """

    # @staticmethod
    # def dynamic_register(subscription, owner, name: str):
    #    """Dynamically register event handler.

    #        owner: owner class
    #        name: attribute name to save
    #    """
    #    subscription.stamp_function()
    #    setattr(owner, name, subscription)
    #    # explicitly call __set_name__ as it is not called automatically in this case
    #    getattr(owner, name).__set_name__(owner, name)

    @classmethod
    def register(cls, event_type: EventType, *args, **kwargs):
        """Decorator to register class methods as event handlers.

        The decorator marks the function as event handler by assigning an attribute
        with event details directly to the method.

        Events are supposed to provide correct signature of event handlers and use this internally.
        """

        class FunctionWrapper:
            """
            Used exclusively for dynamic handler registering and in order to stop
            side-effects. We need to assign event attribute to the handler and this
            approach does not modify attributes of the original.
            """

            def __init__(self, function_or_method):
                self.fn = function_or_method

            def __call__(self, *args, **kwargs):
                return self.fn(*args, **kwargs)

        class Descriptor(t.Generic[FT]):
            """
            Class-type decorator based on descriptors (__set_name__)
            """

            def __init__(self, fn: FT):
                self.fn = fn
                self.__doc__ = fn.__doc__

            # def link(self) -> None:
            #    """Used to dynamically register handlers.

            #    Warning:

            #        Dangerous side effects! Use with care. This method cannot be used to
            #        dynamically register only some instances of a class - the underlying
            #        technique directly modifies the class method and it changes it for
            #        ALL instances.

            #    Make the method into a handler.
            #    """
            #    self._add_event_attribute(self.fn)

            def extract(self) -> FT:
                """Returns the function with additional event handler data.

                Might be used to conditionally register a handler.

                Warning:
                    In order for this method to have no side effects (such as modifing
                    the original function), it needs to wrap the function in another
                    call layer. If that might be a problem (if performance of some very
                    frequently called function is in stake), do not use dynamic
                    registering or rather use the :meth:`.link` technique.

                Example:

                    This short example shows a (trivial) usage. It can be applied similarly to
                    any other event.

                    .. code-block:: python

                        # this example shows
                        from uun_iot import EvStart
                        from uun_iot.events import Register
                        ENABLE_EVENT = True

                        class MyModule:
                            def __init__(self):
                                if ENABLE_EVENT:
                                    self.handler = EvStart.subscribe(self._handler).extract()

                            def _handler(self):
                                print("ticking")

                Args:
                    descriptor: the classical subscription without decorator, eg.
                        `EvTick.subscribe(my_handler)`
                """
                wrapper = FunctionWrapper(self.fn)
                self._add_event_attribute(wrapper)
                return wrapper  # type: ignore

            def _add_event_attribute(self, callable_obj) -> None:
                logger.debug(
                    "producing dynamic stand-alone handler for '%s' using function '%s'",
                    event_type,
                    callable_obj,
                )

                # include information in attribute of the decorated function
                # this works on function but not 'methods', i.e. bound functions. On
                # these, it throws error: 'method' object has no attribute '_uuniot'.
                # bound methods override getattr and setattr in order to lookup the
                # parameters in the wrapped function (.__func__).
                setattr(
                    (
                        callable_obj.__func__
                        if hasattr(callable_obj, "__func__")
                        else callable_obj
                    ),
                    EVENT_KEY,
                    _HandlerInfoInternal(event_type, args, kwargs),
                )

            def __set_name__(self, owner, name: str):
                """Called after assigning decorated method as an attribute to the class.

                Args:
                    owner: owner class
                    name: name of the attribute
                """
                # owner -- owner class of the decorated method
                _, owner_id = class_ids(owner)
                logger.debug(f"decorating {self.fn} of {owner_id}")

                if len(args) > 0:
                    normalized_args = args
                elif args == ():
                    normalized_args = []
                elif args is None:
                    normalized_args = []
                else:
                    normalized_args = list(args)
                doc_list_args = [
                    ",".join([f'"{arg}"' for arg in normalized_args]),
                    ",".join(
                        (f'{key}="{val}"' for key, val in kwargs.items())
                        if kwargs is not None
                        else []
                    ),
                ]
                doc_arguments = ",".join(filter(lambda x: x != "", doc_list_args))
                doc_arguments = f"({doc_arguments})" if doc_arguments != "" else ""
                self.fn.__doc__ = (
                    f"Registered to handle event ``@Ev{event_type.name}.subscribe{doc_arguments}.``\n\n"
                    + self.fn.__doc__
                    if self.fn.__doc__ is not None
                    else ""
                )

                setattr(
                    self.fn,
                    EVENT_KEY,
                    _HandlerInfoInternal(event_type, args, kwargs),
                )

                # then replace ourself (Descriptor) with the original method
                setattr(owner, name, self.fn)

            def __call__(self, *args, **kwargs):
                """
                Type checkers do not know descriptor protocol, hence this is not used during runtime used.

                (In case the method is assigned dynamically (e.g. in __init__),
                __set_name__ is not called. Then, the Descriptor class itself is stored
                as the method and it needs to have __call__ defined.
                """
                return self.fn(*args, **kwargs)

        return Descriptor[F]


# typing does not work for some reason, class properties are not supported well
# https://github.com/python/mypy/issues/2563
# class Register(t.Generic[F]):
#    """
#    Workaround till Python 3.12 which offers parametric functions Descriptor
#    cannot be parametrized as it is outside of scope and passing t.Callable as
#    argument of type Type[T] does not work in typecheckers
#    """
#
#    @classmethod
#    def register(cls, event_type: EventType, *args, **kwargs):
#        """Decorator to register class methods as event handlers.
#
#        The decorator marks the function as event handler by assigning an attribute
#        with event details directly to the method.
#
#        Events are supposed to provide correct signature of event handlers and use this internally.
#        """
#
#        def descriptor(fn: F) -> F:
#            logger.debug("decorating '%s'", fn)
#
#            # include information in attribute of the decorated function
#            setattr(
#                fn,
#                EVENT_KEY,
#                _HandlerInfoInternal(event_type, args, kwargs),
#            )
#            return fn
#
#        return descriptor


class Event(ABC):
    """
    Pass whole config along with "gateway" key.

    It provides a default implementation of ContextManager - i.e. it can be used in
    `with` statements. Default implementation is to call :meth:`.start` on enter and
    :meth:`.stop` on exit.
    """

    event_type: t.ClassVar[EventType]
    _handlers: t.Any
    _config: t.Optional[t.Dict]

    # @classmethod
    # @property
    # @abstractmethod
    # def event_type(cls) -> EventType:
    #    pass

    def __init__(
        self,
        config: t.Optional[t.Dict] = None,
        *,
        requires_config=False,
    ):

        if not hasattr(self, "event_type"):
            raise AttributeError("Event must define its `.event_type`!")

        if requires_config:
            if config is None:
                config = {"gateway": {}}
            if "gateway" not in config:
                raise ValueError(
                    "Pass full configuration to events, not only the gateway subdictionary."
                )
        self._config = config

    @classmethod
    def _register(cls, reg_t_: t.Optional[t.Type[Register[F]]] = None, *args, **kwargs):
        """Register a handler with signature and

        Use as `self._register(Register[typing.Callable[<signature>]],
        additional_data_to_be_stored_for_event_handler)` to enable handler
        signature type checking via :attr:`typing.Callable` signature. To
        typecheck for methods, you need to include first auxilary "self"
        argument in the signature.

        This saves handler information (event type) directly as an attribute to
        the method in :class:`HandlerInfo` structure along with specified
        `*args` and `**kwargs`.

        Args:
            reg_t_: Register class used for type-checking handler signatures
        """
        if reg_t_ is None:
            return Register[t.Callable].register(cls.event_type, *args, **kwargs)
        else:
            return reg_t_.register(cls.event_type, *args, **kwargs)

    @abstractmethod
    def add_handlers(
        self, handler_list: t.Iterable[t.Tuple[t.Callable, HandlerInfo]]
    ) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc_info):
        self.stop()

    def number_of_handlers(self) -> int:
        return len(self._handlers)


@dataclass
class _SubmoduleEv:
    """Internal object to distinguish event handlers and submodules"""

    allowed_events: t.Optional[t.List[EventType]]  # None means all allowed


def registered_event_submodule(
    submodule: V, allowed_events: t.Optional[t.List[t.Type[Event]]] = None
) -> V:
    """Register object as an event submodule.

    Assign the result of this funtion to main module to register the submodule's event handlers to main module.

    Modifies the passed submodule.

    Example:

        Configuration:

        .. code-block:: json

            {
                "gateway": {
                    "moduleTimers": {
                        "module": {
                            "timer1": 1,
                            "timer2": 2
                        }
                    }
                }
            }

        .. code-block:: python

            class Submodule:
                @EvTick.subscribe_timer("timer1")
                def ticktock(self):
                    print("Hello from submodule")

            class Module:
                def __init__(self):
                    self._submodule = registered_event_submodule(Submodule())

                @EvTick.subscribe_timer("timer2")
                def ticktock(self):
                    print("Hello from main module")

    """

    if allowed_events is not None:
        allowed = [ev.event_type for ev in allowed_events]
    else:
        allowed = None
    setattr(submodule, EVENT_KEY, _SubmoduleEv(allowed))
    return submodule


def extract_event_handlers_from_object(
    obj,
    is_class=False,
    owner_id: t.Optional[str] = None,
    rec: int = 0,
) -> t.Iterable[t.Tuple[t.Callable, HandlerInfo]]:
    """Find marked event handlers in an instance and output a dictionary with the handlers.

    If the object contains a registered submodule, behave as if its event handlers are
    handlers of the original object.

    All attributes of an object are visited and checked if the attribute contains an
    `_uuniot` subattribute with event handler information. Attributes starting with
    double underscore `__` are skipped.

    Args:
        obj: the instance in which to search for handlers
        is_class: whether the object is a class; ie. if it is instantiated
        owner_id: if specified, override the owner module's id which is passed to events
            e.g. the :class:`EvTick` event finds timer periods in configuration based on the
            owner_id
        rec: recursion depth, internal use

    Returns:
        an iterable with tuples of (function, handler_info)
    """
    handlers_and_info: t.List[t.Tuple[t.Callable, HandlerInfo]] = []
    if owner_id is None:
        _, owner_id = class_ids(obj) if is_class else instance_ids(obj)
    if owner_id is None:
        raise InvalidModuleId(
            f"Invalid or missing module id for module '{obj}'."
            " The library tries to get the id from the '.id' attribute or it deduces"
            " it from class name. If you see this, please provide snakeCased module id"
            " in the '.id' attribute of the module."
        )
    if rec > 5:
        raise EventException(
            "Recursion depth for handler extraction exceeded."
            " This probably means that you registered"
            " an event submodule which has a cyclic dependency with its parent."
            " Remove the cyclic dependency or the submodule"
        )

    for attr_name in dir(obj):
        # loop over all attributes of obj
        if attr_name.startswith("__"):
            continue
        meth = getattr(obj, attr_name, None)
        event_info = getattr(meth, EVENT_KEY, None)
        if event_info is None:
            # we are interested only in attributes which have been registered by us; it
            # must contain _uuniot attribute
            continue

        if callable(meth) and isinstance(event_info, _HandlerInfoInternal):
            # process event handler
            handler_info = HandlerInfo(
                event_info.event_type, event_info.args, event_info.kwargs, owner_id
            )
            # it is problematic to delete from instance method
            # proper way would be to delete from a class
            # but that would prevent other instances to ever be registered
            # delattr(fn, EVENT_KEY)
            handlers_and_info.append((meth, handler_info))

        elif isinstance(event_info, _SubmoduleEv):
            # attr_obj is an submodule; register its event handlers to the main original object
            submodule_ev_handlers = extract_event_handlers_from_object(
                obj=meth,
                is_class=is_class,
                owner_id=owner_id,
                rec=rec + 1,
            )
            allowed_events = event_info.allowed_events
            if allowed_events is not None:
                # filter only allowed_events
                submodule_ev_handlers = [
                    (fn, info)
                    for fn, info in submodule_ev_handlers
                    if info.event_type in allowed_events
                ]
            handlers_and_info.extend(submodule_ev_handlers)

    return handlers_and_info
