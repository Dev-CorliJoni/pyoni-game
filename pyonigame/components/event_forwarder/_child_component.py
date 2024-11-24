from typing import Type

from pyonigame.components.base import EventBase
from pyonigame.components.event_forwarder import ParentComponent


def child_component(cls: Type[EventBase]):
    """
    A decorator that forwards all events (e.g., clicks, focus changes, theme updates) from the decorated child class to its `ParentComponent`, including information about which child sent the event.

    **Important**: A decorated class requires an instance of the parent as its first parameter during initialization.

     Example:
        # In the following example, the parent is notified when one of the two rectangles is clicked.

        from pyonigame.events import Event

         @child_component
         class NamedChildRect(Rect):
             def __init__(self, x, y, width, height, name):
                black = (0, 0, 0)
                super().__init__(x, y, width, height, black, event_subscription = Event.MOUSE)
                self.name = name

         class MyParentComponent(ParentComponent):
            def __init__(self, child1, child2):
                self.children = [
                    NamedChildRect(self, 0, 0, 20, 20, "rect 1"),
                    NamedChildRect(self, 20, 0, 20, 20, "rect 2"),
                ]

            def update(passed_time):
                return [child.update(passed_time) for child in self.children]

            def left_click(self, child, mouse_x, mouse_y):
                print(f"{child.name} clicked at ({mouse_x}, {mouse_y})")
     """
    old_constructor = cls.__init__

    def constructor(self, parent: ParentComponent, *args, **kwargs):
        self._parent = parent
        old_constructor(self, *args, **kwargs)

    cls.__init__ = constructor

    for method in ('resolve_text_shape', 'theme_changed', 'language_changed', 'screen_size_changed',
                   'left_click', 'middle_click', 'right_click', 'hover',
                   'focus', 'lost_focus',
                   'drag_start', 'dragging', 'drop',
                   'scroll_up', 'scroll_down',
                   'key_press', 'key_release'):
        old_method = getattr(cls, method)

        def new_method(self, *args, _old_method=old_method, _method_name=method, **kwargs):
            # Call the original method
            _old_method(self, *args, **kwargs)
            # Forward the call to the parent
            getattr(self._parent, _method_name)(self, *args, **kwargs)

        setattr(cls, method, new_method)  # Replace the method with the new one

    return cls


def create_child_component_type(cls: Type[EventBase]):
    """
    Creates a new class based on the provided `EventBase`-derived class that forwards all events
    (e.g., clicks, focus changes, theme updates) from the child class to its `ParentComponent`,
    including which child sent the event.

    **Important**: The created class requires an instance of the parent as its first parameter during initialization.

     Example:
        # In this example, the parent is notified when one of two rectangles is clicked.

        from pyonigame.events import Event

         class MyParentComponent(ParentComponent):
            def __init__(self):
                child_type = create_child_component_type(Rect)
                black = (0, 0, 0)
                self.children = [
                    child_type(self, 0, 0, 20, 20, black, event_subscription = Event.MOUSE),
                    child_type(self, 20, 0, 20, 20, black, event_subscription = Event.MOUSE),
                ]

            def update(passed_time):
                return [child.update(passed_time) for child in self.children]

            def left_click(self, child, mouse_x, mouse_y):
                print(f"{child.id} clicked at ({mouse_x}, {mouse_y})")
     """

    @child_component
    class ChildClass(cls):
        pass

    ChildClass.__name__ = f"{cls.__name__}ChildClass"
    return ChildClass
