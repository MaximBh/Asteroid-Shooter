import arcade
import random
import math

BUFF_SIZE = 20  # размер квадратика

class Buff(arcade.SpriteSolidColor):
    def __init__(self, color, x, y):
        super().__init__(BUFF_SIZE, BUFF_SIZE, color)

        self.center_x = x
        self.center_y = y

        # медленное движение (эффект космоса)
        angle = random.uniform(0, 360)
        speed = random.uniform(0.2, 0.5)

        rad = math.radians(angle)
        self.velocity_x = math.cos(rad) * speed
        self.velocity_y = math.sin(rad) * speed

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.velocity_x
        self.center_y += self.velocity_y

    def apply(self, game_view):
        pass
