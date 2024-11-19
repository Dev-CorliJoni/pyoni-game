from pyonigame.elements.controls import AlignableButton


class ButtonGroup:
    def __init__(self, button_list_params, handle_key_navigation=True, next_keys=("p1_down", "p2_down", "p1_right", "p2_right"), last_keys=("p1_up", "p2_up", "p1_left", "p2_left")):
        self.current_index = 0
        self.buttons = []

        self.handle_key_navigation = handle_key_navigation

        self.next_keys = next_keys
        self.last_keys = last_keys

        for button_params in button_list_params:
            self.buttons.append(AlignableButton(**button_params))

    def update(self, inputs):
        for input_ in filter(lambda i: i.type == "key", inputs):
            if input_.second_value in self.next_keys:
                self.current_index = 0 if self.current_index + 1 == len(self.buttons) else self.current_index + 1
            elif input_.second_value in self.last_keys:
                self.current_index = len(self.buttons) - 1 if self.current_index - 1 < 0 else self.current_index - 1

        updates = []

        for button in self.buttons:
            if self.handle_key_navigation:
                button.active = False

                if self.buttons.index(button) == self.current_index:
                    button.active = True

            updates.extend(button.update(inputs))

        return updates
