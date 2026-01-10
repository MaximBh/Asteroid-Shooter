import arcade
import random
import math
from constants import *


class Asteroid(arcade.Sprite):
    def __init__(self, level, x, y):
        super().__init__("assets/textures/asteroid.png")

        self.center_x = x
        self.center_y = y

        angle = random.uniform(0, 360)
        speed = ASTEROID_BASE_SPEED

        rad = math.radians(angle)
        self.dx = math.sin(rad) * speed
        self.dy = math.cos(rad) * speed

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.dx
        self.center_y += self.dy

        # граница X
        if self.center_x < -self.width:
            self.center_x = SCREEN_WIDTH + self.width
        elif self.center_x > SCREEN_WIDTH + self.width:
            self.center_x = -self.width

        # граница Y
        if self.center_y < -self.height:
            self.center_y = SCREEN_HEIGHT + self.height
        elif self.center_y > SCREEN_HEIGHT + self.height:
            self.center_y = -self.height
