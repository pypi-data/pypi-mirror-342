"""
Library events are defined in this module. Below is an overview of existing
events and general information regarding subscriptions to events.

================= =======================================================================
    event                   description
================= =======================================================================
 ``EvTick``        timer has ticked (timer configured in JSON config)
 ``EvStart``       app has started (via :meth:`~Gateway.start`)
 ``EvStop``        app is stopping, please end module's action as soon as possible
 ``EvExternal``    a registered command was issued using socket IPC
 ``EvConfUpdate``  gateway's configuration was updated
================= =======================================================================

Event subscriptions:

    Event handlers in classes (user modules) are registered by storing
    additional information together with the class's method, using
    corresponding `@<event>.subscribe`. This information includes event type
    and possibly additional information needed to identify the handler.

    This information is then collected from all passed instances using
    :func:`attach_handlers` and events with registered handlers are returned.
    There, appropriate events are created and the corresponding handlers are
    registered to corresponding events.

Advanced handler extraction:

    Alternatively, the :func:`attach_handlers` can register handlers to already
    existing events. You can even define your own events! See
    :func:`attach_handlers` for technical details.

Custom events:

    If you want to define your own events independently from this library, the
    only requirement is to subclass from the :class:`Event` class in order to
    be consistend with existing event handling logic. Have a look at existing
    events.

    When defining ways to store event information along with the handler in
    your custom event, you need to implement logic to resolve
    :attr:`HandlerInfo.event_type` to your custom event, while preserving
    existing resolver given in :func:`get_event_class`. For example, define
    :attr:`Event.event_type` to a unique (among all possible subclasses of
    Event) value and use the existing infrastructure

        .. code-block:: python

            import typing as t
            from uun_iot.events import Event, Register, get_event_class, attach_handlers
            from uun_iot.utils import classproperty

            # you can specify details to provide type-checking for handlers
            HandlerSignature = t.Callable[..., None]

            class MyEvent(Event):
                event_type = "myev"
                def __init__(self, config):
                    self._handlers = []
                    super().__init__(config)

                @classproperty
                def subscribe(cls):
                    return cls._register(Register[HandlerSignature])

                def add_handlers(self, handler_list):
                    self._handlers = [fn for fn, info in handler_list]

                def start(self):
                    pass
                def stop(self):
                    pass

            def get_extended_event_class(ev_type):
                if ev_type == "myev":
                    return MyEvent
                else:
                    return get_event_class(ev_type)

            class TestClass:
                @MyEvent.subscribe
                def method(self):
                    pass

            # then, you can attach handlers such as:
            evs = attach_handlers({}, [TestClass()], get_ev_class=get_extended_event_class)
            print(evs)

Note:

    Note about standard Python behaviour. When a class's instance is
    created, the method is bound such that its first argument is the
    instance (the `self` argument). When invoking the instance's
    method, the augmented function is called instead.

Warning:

    Registering handlers not belong to any class (ie. handlers which are not
    methods) is currently not supported. Future versions might allow for
    registering "bare" handler functions.
"""

import itertools
import typing as t

from ..utils import groupby_unsorted, maybe_get_instance
from .EvConfUpdate import EvConfUpdate
from .Event import (Event, EventType, HandlerInfo, Register,
                    extract_event_handlers_from_object,
                    registered_event_submodule)
from .EvExternal import EvExternal
from .EvStart import EvStart
from .EvStop import EvStop
from .EvTick import EvTick

# __all__ = [
#    "EvConfUpdate",
#    "EvExternal",
#    "EvStart",
#    "EvStop",
#    "EvTick",
#    "Event",
#    "EventType",
#    "HandlerInfo",
#    "Register",
#    "extract_event_handlers_from_object",
#    "registered_event_submodule",
# ]


def get_event_class(event_type: EventType):
    """Event factory

    Function matching event type identifier in :class:`HandlerInfo` struct to
    particular event constructor.

    Args:
        event_type: event ID (:class:`EventType`)

    Raises:
        ValueError: When the given :attr:`event_type` is not recognized
    """
    # match event_type:
    #    case EventType.START:
    #        return EvStart
    #    case EventType.STOP:
    #        return EvStop
    #    case EventType.CONF_UPDATE:
    #        return EvConfUpdate
    #    case EventType.TICK:
    #        return EvTick
    #    case EventType.EXTERNAL:
    #        return EvExternal
    #    case _:
    #        raise ValueError("Event type does not exists.")

    if event_type == EventType.START:
        return EvStart
    elif event_type == EventType.STOP:
        return EvStop
    elif event_type == EventType.CONF_UPDATE:
        return EvConfUpdate
    elif event_type == EventType.TICK:
        return EvTick
    elif event_type == EventType.EXTERNAL:
        return EvExternal
    else:
        raise ValueError("Event type does not exists.")


def merge_events(old: t.Iterable[Event], new: t.Iterable[Event]) -> t.Iterable[Event]:
    """Take events from old and new iterables and merge them so that the
    result contains at most one kind of each event, events from new taking precedence.

    iterators are consumed and new ones are returned
    """
    tmp_dict = {ev.event_type: ev for ev in old}
    tmp_dict_new = {ev.event_type: ev for ev in new}
    tmp_dict.update(tmp_dict_new)
    return list(tmp_dict.values())


def attach_handlers(
    config: t.Optional[t.Dict],
    object_list: t.Iterable[t.Any],
    events: t.Optional[t.Iterable[Event]] = None,
    get_ev_class: t.Optional[t.Callable[[EventType], t.Type[Event]]] = None,
) -> t.Collection[Event]:
    """Attach event handlers to :class:`Event` instances.

    Args:
        config: gateway config
        object_list: list of (instantiated) modules with handlers (defined via
            @Event decorator). Alternatively, you can pass the class itself if the
            handlers were already registered locally.
        events: optionally, pass a list of already instantiated events and
            handlers will be added to these events
        get_ev_class: if you define custom events, supply your own map of event
            ID to Event subclass (and preferably pass the event instance in
            :attr:`events`) inherited from :class:`EventType`

    Returns:
        a list where each Event instance is present
          (at most once for each subclass of Event) if it had handlers defined
    """
    if events is None:
        events = []
    if get_ev_class is None:
        get_ev_class = get_event_class

    def get_evtype(item: t.Tuple[t.Callable, HandlerInfo]) -> EventType:
        _, ev_data = item
        return ev_data.event_type

    def ev_with_handlers(config, ev_type, handlers):
        ev_subclass = get_ev_class(ev_type)

        ev = maybe_get_instance(ev_subclass, events)
        if ev is None:
            ev = ev_subclass(config)
        ev.add_handlers(handlers)
        return ev

    # use unsorted groupby as event_types might not be comparable when extended by user
    return [
        ev_with_handlers(config, ev_type, grouped_handler_data)
        for ev_type, grouped_handler_data in groupby_unsorted(
            list(
                itertools.chain.from_iterable(  # flatten
                    map(extract_event_handlers_from_object, object_list)
                )
            ),
            key=get_evtype,
        )
    ]
