from pyonigame.elements.base import CoordinateBase, ShapeBase, Base


class SpriteGroup(CoordinateBase, ShapeBase):

    Layer = Base.Layer

    # coordinate list example (((c1.x, c1.y), (c2.x, c2.y)), ((c3.x, c3.y), (c4.x, c4.y)))
    def __init__(self, x, y, loader, coordinate_list, scale_factor=1, layer=Base.Layer.GAME_ELEMENT):
        super().__init__(x, y)

        self.sprites = []
        max_x = 0

        max_sprite_width = max(c[2] for i in range(len(coordinate_list)) for c in coordinate_list[i] if len(c) == 4) * scale_factor
        max_sprite_height = max(c[3] for i in range(len(coordinate_list)) for c in coordinate_list[i] if len(c) == 4) * scale_factor

        for i in range(len(coordinate_list)):
            for coordinate in coordinate_list[i]:
                if len(coordinate) > 0:
                    self.sprites.append(loader.create_sprite(coordinate, x=x, y=y, scale_factor=scale_factor, layer=layer))

                if coordinate_list[i][-1] == coordinate:
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
