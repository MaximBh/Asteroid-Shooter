import arcade


class Explosion(arcade.SpriteCircle):
    def __init__(self, x, y):
        super().__init__(6, arcade.color.ORANGE)
        self.center_x = x
        self.center_y = y
        self.life = 15

    def update(self, delta_time: float = 1 / 60):
        self.life -= 1
        self.alpha = max(0, self.life * 17)

        if self.life <= 0:
            self.remove_from_sprite_lists()
