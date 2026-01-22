import arcade
import math
import random
from arcade.camera import Camera2D
from entities.ship import Ship
from entities.asteroid import Asteroid
from entities.projectile import Projectile
from entities.explosion import Explosion
from systems.storage import load_high_score, save_high_score
from systems.sound import explosion, game_over
from game.level_manager import LevelManager
from game.game_over_view import GameOverView
from constants import *


# Замедление у границы зоны движения
def slowdown_factor(pos, min_pos, max_pos, margin):
    if pos < min_pos + margin:
        return max(0.0, (pos - min_pos) / margin)
    if pos > max_pos - margin:
        return max(0.0, (max_pos - pos) / margin)
    return 1.0


# Звездный фон
class Star:
    def __init__(self):
        self.x = random.uniform(0, SCREEN_WIDTH)
        self.y = random.uniform(0, SCREEN_HEIGHT)
        self.speed_factor = random.uniform(0.2, 0.6)

    def move(self, dx, dy):
        self.x -= dx * self.speed_factor
        self.y -= dy * self.speed_factor

        if self.x < 0:
            self.x += SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x -= SCREEN_WIDTH

        if self.y < 0:
            self.y += SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y -= SCREEN_HEIGHT

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, 1.5, arcade.color.WHITE)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # Корабль
        self.ship = Ship(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.ship_list = arcade.SpriteList()
        self.ship_list.append(self.ship)
        self.camera = Camera2D()

        # Мир
        self.asteroids = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()

        # Фон
        self.stars = [Star() for _ in range(140)]

        # Игровые данные
        self.level_manager = LevelManager()
        self.score = 0
        self.high_score = load_high_score()

        # Центральная зона движения
        self.zone_width = SCREEN_WIDTH / 3
        self.zone_height = SCREEN_HEIGHT / 3

        self.zone_left = SCREEN_WIDTH / 2 - self.zone_width / 2
        self.zone_right = SCREEN_WIDTH / 2 + self.zone_width / 2
        self.zone_bottom = SCREEN_HEIGHT / 2 - self.zone_height / 2
        self.zone_top = SCREEN_HEIGHT / 2 + self.zone_height / 2

        self.soft_margin = 40  # зона мягкого торможения

        self.spawn_asteroids()

    # Создание астероидов
    def spawn_asteroids(self):
        self.asteroids.clear()

        for _ in range(self.level_manager.asteroid_count()):
            while True:
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)

                if math.hypot(
                        x - self.ship.center_x,
                        y - self.ship.center_y
                ) > 200:
                    self.asteroids.append(
                        Asteroid(self.level_manager.level, x, y)
                    )
                    break

    # Движение мира
    def move_world(self, dx, dy):
        for obj in self.asteroids:
            obj.center_x -= dx
            obj.center_y -= dy

        for bullet in self.bullets:
            bullet.center_x -= dx
            bullet.center_y -= dy

        for explosion in self.explosions:
            explosion.center_x -= dx
            explosion.center_y -= dy

        for star in self.stars:
            star.move(dx, dy)

    def on_update(self, delta_time):
        self.ship.update(delta_time)

        if self.ship.speed > 0:
            rad = math.radians(self.ship.angle)
            dx = math.sin(rad) * self.ship.speed
            dy = math.cos(rad) * self.ship.speed

            fx = slowdown_factor(
                self.ship.center_x,
                self.zone_left,
                self.zone_right,
                self.soft_margin
            )

            fy = slowdown_factor(
                self.ship.center_y,
                self.zone_bottom,
                self.zone_top,
                self.soft_margin
            )

            # движение корабля
            self.ship.center_x += dx * fx
            self.ship.center_y += dy * fy

            # движение мира
            self.move_world(dx * (1 - fx), dy * (1 - fy))

        self.asteroids.update(delta_time)
        self.bullets.update(delta_time)
        self.explosions.update(delta_time)

        # Обработка попаданий
        for bullet in self.bullets:
            hits = arcade.check_for_collision_with_list(bullet, self.asteroids)
            for asteroid in hits:
                explosion.play()
                self.score += 10

                self.explosions.append(
                    Explosion(asteroid.center_x, asteroid.center_y)
                )

                asteroid.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

        # Столкновение с кораблём
        if arcade.check_for_collision_with_list(self.ship, self.asteroids):
            game_over.play()
            if self.score > self.high_score:
                save_high_score(self.score)

            self.window.show_view(
                GameOverView(self.score, max(self.score, self.high_score))
            )

        # Новый уровень
        if len(self.asteroids) == 0:
            self.level_manager.next_level()
            self.spawn_asteroids()

    def on_draw(self):
        self.clear()

        self.camera.use()

        # рисуем мир
        for star in self.stars:
            star.draw()

        self.ship_list.draw()
        self.asteroids.draw()
        self.bullets.draw()
        self.explosions.draw()

        # Отрисовка счета и уровня
        arcade.draw_text(
            f"Score: {self.score}",
            20,
            20,
            arcade.color.WHITE,
            18
        )

        arcade.draw_text(
            f"Level: {self.level_manager.level}",
            20,
            45,
            arcade.color.WHITE,
            18
        )

    # Управление
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.ship.rotate_left = True
        elif key == arcade.key.RIGHT:
            self.ship.rotate_right = True
        elif key == arcade.key.UP:
            self.ship.thrust_dir = 1  # вперёд
        elif key == arcade.key.DOWN:
            self.ship.thrust_dir = -1  # назад
        elif key == arcade.key.SPACE:
            self.bullets.append(Projectile(self.ship))

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.ship.rotate_left = False
        elif key == arcade.key.RIGHT:
            self.ship.rotate_right = False
        elif key == arcade.key.UP:
            self.ship.thrust = False
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.ship.thrust_dir = 0
