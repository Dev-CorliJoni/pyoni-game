from pyonigame.events import RequestType
from pyonigame.events import Request, Event
from pyonigame.models import DictObject


def _event_match(event, comparing_event) -> bool:
    return event & comparing_event == comparing_event


class EventController:
    FOCUS_ORDER_NUMBER = 0
    EVENT_SUBSCRIPTIONS = {}
    REQUESTS = {}
    UPCOMING_EVENTS = []

    FOCUSED_OBJECT = None
    KEY_MAPPING = {}

    @staticmethod
    def process_inputs(inputs: list[DictObject]) -> None:
        if Event.FOCUS in EventController.EVENT_SUBSCRIPTIONS:
            # sort focus for tab focus switch
            EventController.EVENT_SUBSCRIPTIONS[Event.FOCUS] = dict(sorted(EventController.EVENT_SUBSCRIPTIONS[Event.FOCUS].items(), key=lambda item: item[1].focus_order_number))

        # Todo HMI should send request_answer on requests(collision, font_shape_provider or executed
        # Todo commands(apply_settings -> new screen size, ...))
        for event in reversed(EventController.UPCOMING_EVENTS):
            if event.type == "dragging":
                event.pos = (2, 3)  # Todo change to current mouse coordinates
                event.value = "left"
            inputs.insert(0, event)

        EventController.UPCOMING_EVENTS.clear()

        for input_ in inputs:
            for e in Event:
                if e in EventController.EVENT_SUBSCRIPTIONS:
                    filtered_subscriptions = filter(lambda o: not hasattr(input_, "id") or input_.id == o.id, EventController.EVENT_SUBSCRIPTIONS[e].values())
                    sorted_subscriptions = sorted(filtered_subscriptions, key=lambda o: o.layer == "control")

                    for obj in sorted_subscriptions:
                        EventController._trigger(e, obj, input_)

    @staticmethod
    def generate_requests() -> list[DictObject]:
        # commands(quit->change game.running=False))
        for id_ in EventController.REQUESTS:
            _, command = EventController.REQUESTS[id_]
            yield command.request()

    @staticmethod
    def request(request: Request, requester=None):
        if request.type == RequestType.REFRESH_SETTINGS:
            # Todo Save settings in EventController
            request.data = request.data.view
        EventController.REQUESTS[request.id] = (requester, request)

    @staticmethod
    def change_theme(theme: str):
        EventController.UPCOMING_EVENTS.append(DictObject(type="change_theme", theme=theme))

    @staticmethod
    def change_language(language: str):
        EventController.UPCOMING_EVENTS.append(DictObject(type="change_language", language=language))

    @staticmethod
    def set_event_subscriptions(obj, event: Event) -> None:
        for e in Event:
            # Creating defaults for the events
            if e not in EventController.EVENT_SUBSCRIPTIONS:
                EventController.EVENT_SUBSCRIPTIONS[e] = {}

            # Subscribe
            if obj.id not in EventController.EVENT_SUBSCRIPTIONS[e] and _event_match(event, e):
                if _event_match(event, Event.FOCUS):
                    obj.focus_order_number = EventController.FOCUS_ORDER_NUMBER
                    EventController.FOCUS_ORDER_NUMBER += 1

                EventController.EVENT_SUBSCRIPTIONS[e][obj.id] = obj
            # Unsubscribe
            elif obj.id in EventController.EVENT_SUBSCRIPTIONS[e] and not _event_match(event, e):
                if _event_match(event, Event.FOCUS):
                    obj.focus_order_number = None
                del EventController.EVENT_SUBSCRIPTIONS[e][obj.id]

    @staticmethod
    def trigger(event: Event, id_: int, event_arg: DictObject) -> None:
        for e in EventController.EVENT_SUBSCRIPTIONS:
            if _event_match(e, event):
                if id_ in EventController.EVENT_SUBSCRIPTIONS[e]:
                    obj = EventController._get_object(e, id_)
                    EventController._trigger(e, obj, event_arg)

    @staticmethod
    def _get_object(event: Event, id_: int):
        return EventController.EVENT_SUBSCRIPTIONS[event][id_]

    @staticmethod
    def _trigger(event: Event, obj, event_arg: DictObject) -> None:
        if _event_match(event, Event.THEME_CHANGED) and event_arg.type == "change_theme":
            obj.theme_changed(event_arg.theme)

        elif _event_match(event, Event.LANGUAGE_CHANGED) and event_arg.type == "change_language":
            obj.language_changed(event_arg.language)

        elif _event_match(event, Event.SCREEN_SIZE_CHANGED) and event_arg.type == "screen_size":
            obj.screen_size_changed(event_arg.width, event_arg.height)

        elif (any((_event_match(event, e) for e in (Event.MOUSE, Event.FOCUS, Event.DRAG_AND_DROP))) and
              event_arg.type in ("hover", "click", "click_end", "scroll", "dragging")):
            mouse_x, mouse_y = event_arg.pos
            EventController._mouse_events(event, obj, event_arg, mouse_x, mouse_y)

        elif (any((_event_match(event, e) for e in (Event.KEY, Event.FOCUS))) and
              event_arg.type in ("key", "key_end")):
            EventController._key_events(event, obj, event_arg)

    @staticmethod
    def _key_events(event: Event, obj, event_arg) -> None:
        type_, unicode, value = event_arg.type, event_arg.unicode, event_arg.value
        is_tab_used = event_arg.is_tab_used if hasattr(event_arg, "is_tab_used") else False

        second_value = None
        if value in EventController.KEY_MAPPING:
            second_value = EventController.KEY_MAPPING[value]

        if type_ == "key":
            if _event_match(event, Event.KEY):
                obj.key_press(unicode, value, second_value)

            elif _event_match(event, Event.FOCUS) and value == "tab" and not is_tab_used:
                EventController._tab_switch_focus(event, obj, event_arg)

        elif type_ == "key_end" and _event_match(event, Event.KEY):
            obj.key_release(unicode, value, second_value)

    @staticmethod
    def _mouse_events(event: Event, obj, event_arg: DictObject, mouse_x, mouse_y) -> None:
        type_ = event_arg.type
        if type_ != "hover":
            value = event_arg.value

            if type_ == "click":
                EventController._click(event, obj, value, mouse_x, mouse_y)
            elif type_ == "click_end":
                EventController._click_end(event, obj, value, mouse_x, mouse_y)

            elif type_ == "scroll" and _event_match(event, Event.MOUSE):
                if value == "up":
                    obj.scroll_up()
                elif value == "down":
                    obj.scroll_down()

            elif type_ == "dragging" and _event_match(event, Event.DRAG_AND_DROP):
                obj.dragging(mouse_x, mouse_y)
                EventController.UPCOMING_EVENTS.append(DictObject(type="dragging", id=obj.id))
        else:
            if _event_match(event, Event.MOUSE):
                obj.hover(mouse_x, mouse_y)

    @staticmethod
    def _click(event: Event, obj, value, mouse_x, mouse_y) -> None:
        if value == "left":
            if _event_match(event, Event.DRAG_AND_DROP):
                obj.drag_start(mouse_x, mouse_y)
                EventController.UPCOMING_EVENTS.append(DictObject(type="dragging", id=obj.id))

    @staticmethod
    def _click_end(event: Event, obj, value, mouse_x, mouse_y) -> None:
        if value == "left":
            if _event_match(event, Event.DRAG_AND_DROP):
                obj.drop(mouse_x, mouse_y)
                EventController.UPCOMING_EVENTS = [
                    event for event in EventController.UPCOMING_EVENTS
                    if not (event.type == "dragging" and event.id == obj.id)
                ]
            elif _event_match(event, Event.MOUSE):
                obj.left_click(mouse_x, mouse_y)

            EventController._focus_events(event, obj, mouse_x, mouse_y)

        elif value == "middle" and _event_match(event, Event.MOUSE):
            obj.middle_click(mouse_x, mouse_y)

        elif value == "right" and _event_match(event, Event.MOUSE):
            obj.right_click(mouse_x, mouse_y)

    @staticmethod
    def _tab_switch_focus(event: Event, obj, event_arg) -> None:
        if EventController.FOCUSED_OBJECT == obj:
            keys = list(EventController.EVENT_SUBSCRIPTIONS[event].keys())

            index = keys.index(obj.id)
            new_index = (index + 1) % len(keys)
            new_key = keys[new_index]

            new_focused_object = EventController.EVENT_SUBSCRIPTIONS[event][new_key]
            EventController._focus_events(event, new_focused_object, -1, -1)
            event_arg.is_tab_used = True

    @staticmethod
    def _focus_events(event: Event, obj, mouse_x, mouse_y) -> None:

        if _event_match(event, Event.FOCUS):
            if EventController.FOCUSED_OBJECT is not None:
                # If another clickable object is clicked
                EventController.FOCUSED_OBJECT.lost_focus()

            obj.focus(mouse_x, mouse_y)
            EventController.FOCUSED_OBJECT = obj
