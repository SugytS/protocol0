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
        self.base_speed = PLAYER_SPEED
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.ammo = PLAYER_STARTING_AMMO
        self.score = 0
        self.change_x = 0
        self.change_y = 0

        # Модификаторы улучшений
        self.damage_multiplier = 1.0  # Множитель урона

        # Загрузка текстур
        self.texture = arcade.load_texture(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        )

        # Направление взгляда
        self.angle = 0
        self.prev_angle = 0  # Предыдущий угол для проверки столкновений

    def update(self, delta_time, keys_pressed):
        """Обновление позиции игрока"""
        self.change_x = 0
        self.change_y = 0

        # Обработка управления
        if arcade.key.W in keys_pressed or arcade.key.UP in keys_pressed:
            self.change_y += self.speed * delta_time
        if arcade.key.S in keys_pressed or arcade.key.DOWN in keys_pressed:
            self.change_y -= self.speed * delta_time
        if arcade.key.A in keys_pressed or arcade.key.LEFT in keys_pressed:
            self.change_x -= self.speed * delta_time
        if arcade.key.D in keys_pressed or arcade.key.RIGHT in keys_pressed:
            self.change_x += self.speed * delta_time

        # Нормализация диагонального движения
        if self.change_x != 0 and self.change_y != 0:
            factor = 0.7071  # 1/√2
            self.change_x *= factor
            self.change_y *= factor

        # Сохраняем предыдущую позицию для отката при столкновении
        prev_x = self.center_x
        prev_y = self.center_y
        prev_angle = self.angle

        # Обновление позиции
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Сохраняем предыдущий угол
        self.prev_angle = prev_angle

        # Ограничение движения в пределах комнаты
        self.center_x = max(TILE_SIZE, min(SCREEN_WIDTH - TILE_SIZE, self.center_x))
        self.center_y = max(TILE_SIZE, min(SCREEN_HEIGHT - TILE_SIZE, self.center_y))

    def take_damage(self, damage):
        """Получение урона"""
        self.health -= damage
        self.health = max(0, self.health)

    def heal(self, amount):
        """Лечение"""
        old_health = self.health
        self.health += amount
        self.health = min(self.max_health, self.health)
        return self.health - old_health  # Возвращаем реально вылеченное количество

    def add_ammo(self, amount):
        """Добавление патронов"""
        self.ammo += amount

    def apply_upgrade(self, upgrade_type, value):
        """Применение улучшения"""
        if upgrade_type == "damage":
            self.damage_multiplier *= value
            return f"Урон увеличен до {self.damage_multiplier:.1f}x"

        elif upgrade_type == "health":
            self.max_health += value
            self.health += value
            return f"Максимальное здоровье: {self.max_health}"

        elif upgrade_type == "speed":
            self.speed = self.base_speed * value
            return f"Скорость: {self.speed:.0f}"

        elif upgrade_type == "ammo":
            self.ammo += value
            return f"Патроны: {self.ammo}"

        elif upgrade_type == "heal":
            healed = self.heal(value)
            return f"Восстановлено {healed} здоровья"

        return "Улучшение применено"
