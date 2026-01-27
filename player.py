"""
Класс игрока
"""

import arcade
import math
from config import *

class Player(arcade.Sprite):
    """Класс игрока"""

    def __init__(self):
        super().__init__()

        # Основные характеристики
        self.scale = 1.0
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.ammo = PLAYER_STARTING_AMMO
        self.score = 0

        # Загрузка текстур (используем встроенные для начала)
        self.texture = arcade.load_texture(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        )

        # Направление взгляда
        self.angle = 0

    def update(self, delta_time, keys_pressed):
        """Обновление позиции игрока"""
        dx, dy = 0, 0

        # Обработка управления
        if arcade.key.W in keys_pressed or arcade.key.UP in keys_pressed:
            dy += self.speed * delta_time
        if arcade.key.S in keys_pressed or arcade.key.DOWN in keys_pressed:
            dy -= self.speed * delta_time
        if arcade.key.A in keys_pressed or arcade.key.LEFT in keys_pressed:
            dx -= self.speed * delta_time
        if arcade.key.D in keys_pressed or arcade.key.RIGHT in keys_pressed:
            dx += self.speed * delta_time

        # Нормализация диагонального движения
        if dx != 0 and dy != 0:
            factor = 0.7071  # 1/√2
            dx *= factor
            dy *= factor

        # Обновление позиции
        self.center_x += dx
        self.center_y += dy

        # Ограничение движения в пределах экрана
        self.center_x = max(self.width/2, min(SCREEN_WIDTH - self.width/2, self.center_x))
        self.center_y = max(self.height/2, min(SCREEN_HEIGHT - self.height/2, self.center_y))

    def take_damage(self, damage):
        """Получение урона"""
        self.health -= damage
        self.health = max(0, self.health)  # Не даем уйти ниже 0

    def heal(self, amount):
        """Лечение"""
        self.health += amount
        self.health = min(self.max_health, self.health)  # Не даем превысить максимум

    def add_ammo(self, amount):
        """Добавление патронов"""
        self.ammo += amount