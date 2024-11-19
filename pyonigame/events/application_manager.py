from pyonigame.models.settings import Settings
from pyonigame.events import RequestType
from pyonigame.events import Request, Event
from pyonigame.models import DictObject


def _event_match(event, comparing_event) -> bool:
    return event & comparing_event == comparing_event


class ApplicationManager:
    FOCUS_ORDER_NUMBER = 0
    EVENT_SUBSCRIPTIONS = {}
    REQUESTS = {}
    UPCOMING_EVENTS = []

    SETTINGS: Settings = None
    FOCUSED_OBJECT = None

    @staticmethod
    def process_inputs(inputs: list[DictObject]) -> None:
        if Event.FOCUS in ApplicationManager.EVENT_SUBSCRIPTIONS:
            # sort focus for tab focus switch
            ApplicationManager.EVENT_SUBSCRIPTIONS[Event.FOCUS] = dict(sorted(ApplicationManager.EVENT_SUBSCRIPTIONS[Event.FOCUS].items(), key=lambda item: item[1].focus_order_number))

        # Todo HMI should send request_answer on requests(collision, font_shape_provider or executed
        # Todo commands(apply_settings -> new screen size, ...))
        for event in reversed(ApplicationManager.UPCOMING_EVENTS):
            if event.type == "dragging":
                event.pos = (2, 3)  # Todo change to current mouse coordinates
                event.value = "left"
            inputs.insert(0, event)

        ApplicationManager.UPCOMING_EVENTS.clear()

        requests = list(ApplicationManager.REQUESTS.values())
        ApplicationManager.REQUESTS.clear()
        Request.COUNTER = 0

        for input_ in inputs:
            if input_.type == "quit":
                ApplicationManager.request(Request(RequestType.QUIT, DictObject()))
            elif input_.type == "request_answer":
                if input_.answer_type == "text_shape_resolver":
                    for requester, request in requests:
                        if request.type == RequestType.TEXT_SHAPE_RESOLVER:
                            requester.resolve_text_shape(input_.value)
            else:
                if input_.type == "screen_size":
                    ApplicationManager.SETTINGS.view.dimension.set_dimension(input_.width, input_.height)
                for e in Event:
                    if e in ApplicationManager.EVENT_SUBSCRIPTIONS:
                        filtered_subscriptions = filter(lambda o: not hasattr(input_, "id") or input_.id == o.id, ApplicationManager.EVENT_SUBSCRIPTIONS[e].values())
                        sorted_subscriptions = sorted(filtered_subscriptions, key=lambda o: o.layer == "control")

                        for obj in sorted_subscriptions:
                            ApplicationManager._trigger(e, obj, input_)

    @staticmethod
    def generate_requests() -> list[DictObject]:
        requested_text_shape_resolver = False
        ids = list(ApplicationManager.REQUESTS.keys())

        for id_ in ids:
            _, request = ApplicationManager.REQUESTS[id_]
            if request.type == RequestType.TEXT_SHAPE_RESOLVER and not requested_text_shape_resolver:
                requested_text_shape_resolver = True
                yield request.request()
            elif request.type != RequestType.TEXT_SHAPE_RESOLVER:
                del ApplicationManager.REQUESTS[id_]
                yield request.request()

    @staticmethod
    def request(request: Request, requester=None):
        settings = request.data
        if request.type == RequestType.REFRESH_SETTINGS:
            if ApplicationManager.SETTINGS.game.theme != settings.game.theme:
                ApplicationManager.UPCOMING_EVENTS.append(DictObject(type="change_theme", theme=settings.game.theme))
            if ApplicationManager.SETTINGS.game.language != settings.game.language:
                ApplicationManager.UPCOMING_EVENTS.append(DictObject(type="change_language", language=settings.game.language))

            ApplicationManager.SETTINGS = settings
            request.data = settings.view
        elif (request.type == RequestType.QUIT or request.type == RequestType.REFRESH) and any([request.type == r.type for _, r in ApplicationManager.REQUESTS.values()]):
            return
        ApplicationManager.REQUESTS[request.id] = (requester, request)

    @staticmethod
    def set_event_subscriptions(obj, event: Event) -> None:
        for e in Event:
            # Creating defaults for the events
            if e not in ApplicationManager.EVENT_SUBSCRIPTIONS:
                ApplicationManager.EVENT_SUBSCRIPTIONS[e] = {}

            # Subscribe
            if obj.id not in ApplicationManager.EVENT_SUBSCRIPTIONS[e] and _event_match(event, e):
                if _event_match(event, Event.FOCUS):
                    obj.focus_order_number = ApplicationManager.FOCUS_ORDER_NUMBER
                    ApplicationManager.FOCUS_ORDER_NUMBER += 1

                ApplicationManager.EVENT_SUBSCRIPTIONS[e][obj.id] = obj
            # Unsubscribe
            elif obj.id in ApplicationManager.EVENT_SUBSCRIPTIONS[e] and not _event_match(event, e):
                if _event_match(event, Event.FOCUS):
                    obj.focus_order_number = None
                del ApplicationManager.EVENT_SUBSCRIPTIONS[e][obj.id]

    @staticmethod
    def trigger(event: Event, id_: int, event_arg: DictObject) -> None:
        for e in ApplicationManager.EVENT_SUBSCRIPTIONS:
            if _event_match(e, event):
                if id_ in ApplicationManager.EVENT_SUBSCRIPTIONS[e]:
                    obj = ApplicationManager._get_object(e, id_)
                    ApplicationManager._trigger(e, obj, event_arg)

    @staticmethod
    def _get_object(event: Event, id_: int):
        return ApplicationManager.EVENT_SUBSCRIPTIONS[event][id_]

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
            ApplicationManager._mouse_events(event, obj, event_arg, mouse_x, mouse_y)

        elif (any((_event_match(event, e) for e in (Event.KEY, Event.FOCUS))) and
              event_arg.type in ("key", "key_end")):
            ApplicationManager._key_events(event, obj, event_arg)

    @staticmethod
    def _key_events(event: Event, obj, event_arg) -> None:
        type_, unicode, value = event_arg.type, event_arg.unicode, event_arg.value
        is_tab_used = event_arg.is_tab_used if hasattr(event_arg, "is_tab_used") else False

        second_value = None
        if value in ApplicationManager.SETTINGS.game.key_mapping:
            second_value = ApplicationManager.SETTINGS.game.key_mapping[value]

        if type_ == "key":
            if _event_match(event, Event.KEY):
                obj.key_press(unicode, value, second_value)

            elif _event_match(event, Event.FOCUS) and value == "tab" and not is_tab_used:
                ApplicationManager._tab_switch_focus(event, obj, event_arg)

        elif type_ == "key_end" and _event_match(event, Event.KEY):
            obj.key_release(unicode, value, second_value)

    @staticmethod
    def _mouse_events(event: Event, obj, event_arg: DictObject, mouse_x, mouse_y) -> None:
        type_ = event_arg.type
        if type_ != "hover":
            value = event_arg.value

            if type_ == "click":
                ApplicationManager._click(event, obj, value, mouse_x, mouse_y)
            elif type_ == "click_end":
                ApplicationManager._click_end(event, obj, value, mouse_x, mouse_y)

            elif type_ == "scroll" and _event_match(event, Event.MOUSE):
                if value == "up":
                    obj.scroll_up()
                elif value == "down":
                    obj.scroll_down()

            elif type_ == "dragging" and _event_match(event, Event.DRAG_AND_DROP):
                obj.dragging(mouse_x, mouse_y)
                ApplicationManager.UPCOMING_EVENTS.append(DictObject(type="dragging", id=obj.id))
        else:
            if _event_match(event, Event.MOUSE):
                obj.hover(mouse_x, mouse_y)

    @staticmethod
    def _click(event: Event, obj, value, mouse_x, mouse_y) -> None:
        if value == "left":
            if _event_match(event, Event.DRAG_AND_DROP):
                obj.drag_start(mouse_x, mouse_y)
                ApplicationManager.UPCOMING_EVENTS.append(DictObject(type="dragging", id=obj.id))

    @staticmethod
    def _click_end(event: Event, obj, value, mouse_x, mouse_y) -> None:
        if value == "left":
            if _event_match(event, Event.DRAG_AND_DROP):
                obj.drop(mouse_x, mouse_y)
                ApplicationManager.UPCOMING_EVENTS = [
                    event for event in ApplicationManager.UPCOMING_EVENTS
                    if not (event.type == "dragging" and event.id == obj.id)
                ]
            elif _event_match(event, Event.MOUSE):
                obj.left_click(mouse_x, mouse_y)

            ApplicationManager._focus_events(event, obj, mouse_x, mouse_y)

        elif value == "middle" and _event_match(event, Event.MOUSE):
            obj.middle_click(mouse_x, mouse_y)

        elif value == "right" and _event_match(event, Event.MOUSE):
            obj.right_click(mouse_x, mouse_y)

    @staticmethod
    def _tab_switch_focus(event: Event, obj, event_arg) -> None:
        if ApplicationManager.FOCUSED_OBJECT == obj:
            keys = list(ApplicationManager.EVENT_SUBSCRIPTIONS[event].keys())

            index = keys.index(obj.id)
            new_index = (index + 1) % len(keys)
            new_key = keys[new_index]

            new_focused_object = ApplicationManager.EVENT_SUBSCRIPTIONS[event][new_key]
            ApplicationManager._focus_events(event, new_focused_object, -1, -1)
            event_arg.is_tab_used = True

    @staticmethod
    def _focus_events(event: Event, obj, mouse_x, mouse_y) -> None:

        if _event_match(event, Event.FOCUS):
            if ApplicationManager.FOCUSED_OBJECT is not None:
                # If another clickable object is clicked
                ApplicationManager.FOCUSED_OBJECT.lost_focus()

            obj.focus(mouse_x, mouse_y)
            ApplicationManager.FOCUSED_OBJECT = obj
