import pygame
from time import time


class Controller:
    BUTTONS = {
    }
    AXES = {
    }

    def __init__(self, joystick_):
        self.joystick = joystick_

    @property
    def id(self):
        return self.joystick.get_id()

    @property
    def instance_id(self):
        return self.joystick.get_instance_id()

    @property
    def name(self):
        return self.joystick.get_name()

    @property
    def axes(self):
        return self.AXES

    def quit(self):
        self.joystick.quit()

    def get_button_data(self, button, button_event):
        return self.id, self.name, self.BUTTONS[button]

    def get_axis_data(self, axis):
        joystick_name, axis_name = self.AXES[axis]
        axis_value = self.joystick.get_axis(axis)
        return self.id, self.name, joystick_name, axis_name, axis_value


class SwitchSmallController(Controller):
    BUTTONS = {
        0: "action_right",
        1: "action_down",
        2: "action_up",
        3: "action_left",
        5: "home",
        6: "option_1",
        7: "joystick_1_click",
        9: "trigger_left",
        10: "trigger_right",
    }
    AXES = {
        0: ("joystick_1", "horizontal"),
        1: ("joystick_1", "vertical"),
    }


class SwitchBigController(Controller):
    BUTTONS = {
        **SwitchSmallController.BUTTONS,
        4: "option_2",
        8: "joystick_2_click",
        11: "up",
        12: "down",
        13: "left",
        14: "right",
        15: "capture"
    }
    AXES = {
        **SwitchSmallController.AXES,
        2: ("joystick_2", "horizontal"),
        3: ("joystick_2", "vertical"),
        4: ("trigger_left", None),
        5: ("trigger_right", None)
    }


class SwitchBigSplittableController(Controller):

    SIDE = {
        "L": 1,
        "R": 0,
    }

    BUTTONS = {
        # button: side, button_name
        0: ("R", "action_down"),
        1: ("R", "action_left"),
        2: ("R", "action_right"),
        3: ("R", "action_up"),
        4: ("L", "option_1"),
        5: ("R", "home"),
        6: ("R", "option_1"),
        7: ("L", "joystick_1_click"),
        8: ("R", "joystick_1_click"),
        11: ("L", "action_left"),
        12: ("L", "action_right"),
        13: ("L", "action_down"),
        14: ("L", "action_up"),
        15: ("L", "home"),
        16: ("R", "trigger_right"),
        17: ("L", "trigger_left"),
        18: ("R", "trigger_left"),
        19: ("L", "trigger_right"),
    }

    AXES = {
        # axis: side, (joystick, axis_name)
        0: ("L", "joystick_1", "vertical"),
        1: ("L", "joystick_1", "horizontal"),
        2: ("R", "joystick_1", "vertical"),
        3: ("R", "joystick_1", "horizontal")
    }

    def __init__(self, joystick_):
        super().__init__(joystick_)
        self.one_controller_mode = True
        self.controller_mode_change_init_data = None

    def get_button_data(self, button, button_event):
        controller_name, button_name = self.name, ""
        internal_id = 0

        if self.one_controller_mode:
            if button in SwitchBigController.BUTTONS:
                button_name = SwitchBigController.BUTTONS[button]
            # 16 and 18 or 17 and 19 are the triggers of the split Controllers and not available for combined. Therefore, controller mode is inverted
            elif button_event == "press" and (self.joystick.get_button(16) and self.joystick.get_button(18)):
                self.controller_mode_change_init(16, 18)
            elif button_event == "press" and (self.joystick.get_button(17) and self.joystick.get_button(19)):
                self.controller_mode_change_init(17, 19)
        else:
            if button in SwitchBigSplittableController.BUTTONS:
                side, button_name = SwitchBigSplittableController.BUTTONS[button]
                internal_id, controller_name = self.get_split_controller_information(side)
            # 9 and 10 are the triggers of the Combined Controller and not available for split mode. Therefore,  controller mode is inverted
            elif button_event == "press" and self.joystick.get_button(9) and self.joystick.get_button(10):
                self.controller_mode_change_init(9, 10)

        if button_event == "release" and self.controller_mode_change_init_data is not None:
            button_1, button_2, timestamp = self.controller_mode_change_init_data
            buttons_released = not self.joystick.get_button(button_1) and not self.joystick.get_button(button_2)
            if buttons_released and time() - timestamp > 1:
                self.one_controller_mode = not self.one_controller_mode

            if buttons_released:
                self.controller_mode_change_init_data = None

        return self.id + internal_id, controller_name, button_name

    def controller_mode_change_init(self, button_1, button_2):
        self.controller_mode_change_init_data = button_1, button_2, time()

    def get_axis_data(self, axis):
        controller_name = self.name
        axis_value = self.joystick.get_axis(axis)
        internal_id = 0

        if self.one_controller_mode:
            joystick_name, axis_name = SwitchBigController.AXES[axis]
        else:
            side, joystick_name, axis_name = SwitchBigSplittableController.AXES[axis]
            internal_id, controller_name = self.get_split_controller_information(side)
            # value needs to be inverted because system handles it as one controller
            if (side == "L" and axis_name == "vertical") or (side == "R" and axis_name == "horizontal"):
                axis_value *= -1

        return self.id + internal_id, controller_name, joystick_name, axis_name, axis_value

    def get_split_controller_information(self, side):
        return SwitchBigSplittableController.SIDE[side], self.name.replace("L/R", side)

    @property
    def axes(self):
        if self.one_controller_mode:
            return SwitchBigController.AXES
        else:
            return SwitchBigSplittableController.AXES


def load_controller(joystick_):
    controller_name = joystick_.get_name()
    if "Nintendo Switch" in controller_name:
        if "Pro" in controller_name:
            return SwitchBigController(joystick_)
        elif "(L/R)" in controller_name:
            return SwitchBigSplittableController(joystick_)
        elif any((type_ in controller_name for type_ in ("(L)", "(R)"))):
            return SwitchSmallController(joystick_)

    if "PLAYSTATION(R)3 Controller" == joystick_.get_name():
        return None

    print("Unknown Controller type")
    return SwitchBigController(joystick_)


# Pygame und das Joystick-Modul initialisieren
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

pygame.joystick.init()

# Joystick initialisieren (hier der erste verbundene Joystick)
controller_devices = []
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    controller = load_controller(joystick)
    if controller is not None:
        controller_devices.append(controller)
        print(f"Joystick verbunden: {controller.name}")

# Hauptloop
running = True
while running:
    try:
        events = pygame.event.get()
    except SystemError as e:
        print(f"Error processing events: {e}", f"Reloading Controller")
        events = []
        controller_devices = []
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            controller = load_controller(joystick)
            if controller is not None:
                controller_devices.append(controller)
                print(f"Joystick verbunden: {controller.name}")

    output = ""

    for event in events:
        try:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYDEVICEADDED:
                if not any((event.device_index == c.id for c in controller_devices)):
                    joystick = pygame.joystick.Joystick(event.device_index)
                    joystick.init()
                    controller = load_controller(joystick)
                    if controller is not None:
                        controller_devices.append(controller)
                        print(f"Joystick verbunden: {joystick.get_name()}")
            elif event.type == pygame.JOYDEVICEREMOVED:
                controller = next(filter(lambda c: c.instance_id == event.instance_id, controller_devices), None)
                if controller is not None:
                    controller_devices.remove(controller)
                    print(f"Joystick getrennt: {controller.name}")
                    controller.quit()
            elif event.type == pygame.JOYBUTTONDOWN:
                controller = next(filter(lambda c: c.instance_id == event.instance_id, controller_devices), None)
                if controller is not None:
                    id_, name, value = controller.get_button_data(event.button, "press")
                    output += f"\nController: {name}({id_}), Button {value} gedrückt"
            elif event.type == pygame.JOYBUTTONUP:
                controller = next(filter(lambda c: c.instance_id == event.instance_id, controller_devices), None)
                if controller is not None:
                    id_, name, value = controller.get_button_data(event.button, "release")
                    output += f"\nController: {name}({id_}), Button {value} losgelassen"

        except KeyError as e:
            print(f"KeyError beim Verarbeiten eines Events: {e}")

    for controller in controller_devices:
        for axis_number in controller.axes:
            id_, name, joystick, axis_name, value = controller.get_axis_data(axis_number)
            output += f"\nController: {name}, Part: {joystick}, Axis: {axis_name}, Value: {value}"

    print(f"{output}\n")

    # Hier kannst du z.B. eine Pause einfügen, damit die Konsole nicht überflutet wird
    pygame.time.wait(500)

pygame.quit()
