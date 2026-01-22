import arcade
from constants import *


class Ship(arcade.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__("assets/textures/ship.png", 0.5)

        # корабль в центре экрана
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2

        self.angle = 0
        self.speed = 0.0

        self.rotate_left = False
        self.rotate_right = False
        self.thrust = False  # ускорение
        self.thrust_dir = 0  # -1 назад, 0 нет, 1 вперёд

    def update(self, delta_time: float = 1 / 60):
        if self.thrust_dir != 0:
            self.speed += SHIP_ACCELERATION * self.thrust_dir
            self.speed = max(-SHIP_MAX_SPEED, min(self.speed, SHIP_MAX_SPEED))
        else:
            self.speed *= FRICTION

        # поворот
        if self.rotate_left:
            self.angle -= SHIP_ROTATION_SPEED  # влево
        if self.rotate_right:
            self.angle += SHIP_ROTATION_SPEED  # вправо

        # ускорение
        if self.thrust:
            self.speed += SHIP_ACCELERATION
            self.speed = min(self.speed, SHIP_MAX_SPEED)
        else:
            self.speed *= FRICTION
