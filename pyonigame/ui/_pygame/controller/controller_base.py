from abc import ABC, abstractmethod


class ControllerBase(ABC):

    BUTTONS = {
    }
    AXES = {
    }

    def __init__(self, joystick):
        self._axes = None
        self._buttons = None
        self.joystick_handle = joystick

    def quit(self):
        self.joystick_handle.quit()

    @property
    def id(self):
        return self.joystick_handle.get_id()

    @property
    def instance_id(self):
        return self.joystick_handle.get_instance_id()

    @property
    def name(self):
        return self.joystick_handle.get_name()

    @property
    def _name_pattern(self):
        return self.name.replace("(R)", "Small").replace("(L)", "Small")

    @property
    def axes(self):
        return self.AXES[self._name_pattern]

    @axes.setter
    def axes(self, axes):
        if self._name_pattern not in self.AXES:
            self.AXES[self._name_pattern] = axes

    @property
    def buttons(self):
        return self.BUTTONS[self._name_pattern]

    @buttons.setter
    def buttons(self, buttons):
        if self._name_pattern not in self.BUTTONS:
            self.BUTTONS[self._name_pattern] = buttons

    @property
    def is_loaded(self):
        return self._name_pattern in self.BUTTONS and self._name_pattern in self.AXES

    @abstractmethod
    def _get_button_data(self, button):
        pass

    @abstractmethod
    def _get_axis_data(self, axis):
        pass

    def get_button_data(self, button):
        if self.is_loaded:
            return self._get_button_data(button)

    def get_axis_data(self, axis):
        if self.is_loaded:
            return self._get_axis_data(axis)

    def gen_axes_data(self):
        if self.is_loaded:
            for axis in self.axes:
                yield self._get_axis_data(axis)
