import json
import pygame
from threading import Thread

from pyonigame.models import DictObject
from pyonigame.ui._pygame.controller import Controller
from pyonigame.helper._resource_path_provider import get_resource_path


def load_controller_mapping(path, controller):
    with open(path, "r") as f:
        data = json.load(f)

    controller.axes = data["axes"]
    controller.buttons = data["buttons"]


class ControllerManager:

    def __init__(self):
        pygame.joystick.init()
        self._controllers = []

    def initialize_controllers(self):
        for i in range(pygame.joystick.get_count()):
            self.add_controller(i)

    def add_controller(self, index):
        joystick = pygame.joystick.Joystick(index)
        joystick.init()
        controller = Controller(joystick)

        name = None
        if "Nintendo Switch" in controller.name:
            if "Pro" in controller.name:
                name = "nintendo_switch_pro_controller.json"
            elif "(L/R)" in controller.name:
                name = "nintendo_switch_combined_joy_con.json"
            elif any((type_ in controller.name for type_ in ("(L)", "(R)"))):
                name = "nintendo_switch_small_joy_con.json"
        else:
            name = "nintendo_switch_pro_controller.json"  # Todo evaluate proper mapping

        if name is not None:
            path = get_resource_path(f"controller_mappings/{name}")
            Thread(target=load_controller_mapping, args=(path, controller)).start()

        self._controllers.append(controller)

    def remove_controller(self, instance_id):
        controller = next(filter(lambda c: c.instance_id == instance_id, self._controllers), None)
        if controller is not None:
            self._controllers.remove(controller)
            controller.quit()

    def gen_controller_button(self, instance_id, button, button_action):
        controller = next(filter(lambda c: c.instance_id == instance_id, self._controllers), None)
        if controller is not None:
            id_, name, value = controller.get_button_data(button)
            yield DictObject({"type": "controller", "event": button_action, "id": id_, "name": name, "value": value})

    def gen_all_controller_axes(self):
        for controller in self._controllers:
            for axis_number in controller.axes:
                id_, name, joystick, axis_name, value = controller.get_axis_data(axis_number)
                yield DictObject({"type": "controller", "event": "axes", "id": id_, "name": name, "joystick": joystick, "axis_name": axis_name, "value": value})
