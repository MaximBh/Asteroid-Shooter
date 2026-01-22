import arcade
import math
from constants import *

class Projectile(arcade.Sprite):
    def __init__(self, ship):
        super().__init__("assets/textures/bullet.png", 0.3)

        rad = math.radians(ship.angle)

        self.center_x = ship.center_x
        self.center_y = ship.center_y

        self.dx = math.sin(rad) * BULLET_SPEED
        self.dy = math.cos(rad) * BULLET_SPEED

        self.life = BULLET_LIFETIME

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.dx
        self.center_y += self.dy
        self.life -= 1

        if self.life <= 0:
            self.remove_from_sprite_lists()

