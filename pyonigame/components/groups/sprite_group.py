from pyonigame.events import Event
from pyonigame.models.components import SpriteData
from pyonigame.components.event_forwarder import ParentComponent, create_child_component_type
from pyonigame.components.base import CoordinateBase, ShapeBase, Base
from pyonigame.components.core import Sprite


class SpriteGroup(CoordinateBase, ShapeBase, ParentComponent):

    Layer = Base.Layer

    def __init__(self, x, y, sprite_data_list: list[list[SpriteData]], scale_factor=1, layer=Base.Layer.GAME_ELEMENT, event_subscription: Event = Event.NONE):
        """

        :param x: The x-coordinate on the UI.
        :param y: The y-coordinate on the UI.
        :param sprite_data_list: A nested list of `SpriteData` objects. For example, a 2x2 grid of sprites would look like:
            ((SpriteData(...), SpriteData(...)),
             (SpriteData(...), SpriteData(...)))
        :param scale_factor: The factor by which to scale the sprites.
        :param layer: Specifies the layer of the UI in hierarchical order. Layers are arranged from back to front as follows: BACKGROUND -> GAME_ELEMENT -> CONTROL.
        :param event_subscription: Defines the events that the object will subscribe to
        """
        super().__init__(x, y)
        super(ParentComponent, self).__init__()
        child_type = create_child_component_type(Sprite)

        self.sprites = []
        max_x = 0

        max_sprite_width = max(sprite_data.width for i in range(len(sprite_data_list)) for sprite_data in sprite_data_list[i] if sprite_data.is_locator_valid()) * scale_factor
        max_sprite_height = max(sprite_data.height for i in range(len(sprite_data_list)) for sprite_data in sprite_data_list[i] if sprite_data.is_locator_valid()) * scale_factor

        for i in range(len(sprite_data_list)):
            for sprite_data in sprite_data_list[i]:
                if sprite_data.is_locator_valid():
                    self.sprites.append(child_type(self, x, y, sprite_data, scale_factor=scale_factor, layer=layer, event_subscription=event_subscription))

                if sprite_data_list[i][-1] is sprite_data:
                    y = y + max_sprite_height
                    max_x = x + max_sprite_width
                    x = self.x
                else:
                    x = x + max_sprite_width

        ShapeBase.__init__(self, max_x - self.x, y - self.y)

    def update(self, inputs):
        return [sprite.update(inputs) for sprite in self.sprites]

    def move(self, dx, dy):
        super().move(dx, dy)
        for sprite in self.sprites:
            sprite.move(dx, dy)

    @property
    def state_changed(self):
        return any([sprite.state_changed for sprite in self.sprites])

    @state_changed.setter
    def state_changed(self, value):
        for sprite in self.sprites:
            sprite.state_changed = value
