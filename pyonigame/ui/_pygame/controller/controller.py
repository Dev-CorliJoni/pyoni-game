from pyonigame.ui.pygame_.controller import ControllerBase


class Controller(ControllerBase):

    def __init__(self, joystick):
        super().__init__(joystick)

    def _get_button_data(self, button):
        return self.id, self.name, self.buttons[button]

    def _get_axis_data(self, axis):
        joystick_name, axis_name = self.axes[axis]
        axis_value = self.joystick_handle.get_axis(axis)
        return self.id, self.name, joystick_name, axis_name, axis_value
