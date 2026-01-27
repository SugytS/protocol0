"""
Классы врагов
"""

import arcade
import random
import math
from config import *

class Enemy(arcade.Sprite):
    """Базовый класс врага"""

    def __init__(self, enemy_type="melee"):
        super().__init__()

        self.type = enemy_type
        self.speed = ENEMY_SPEEDS.get(enemy_type, 100)
        self.max_health = ENEMY_HEALTH.get(enemy_type, 30)
        self.health = self.max_health
        self.attack_damage = 10
        self.attack_cooldown = 0

        # Загрузка текстур в зависимости от типа
        if enemy_type == "melee":
            self.texture = arcade.load_texture(
                ":resources:images/animated_characters/zombie/zombie_idle.png"
            )
        elif enemy_type == "ranged":
            self.texture = arcade.load_texture(
                ":resources:images/animated_characters/robot/robot_idle.png"
            )
        elif enemy_type == "tank":
            self.scale = 1.5
            self.texture = arcade.load_texture(
                ":resources:images/animated_characters/robot/robot_idle.png"
            )
        elif enemy_type == "boss":
            self.scale = 2.0
            self.texture = arcade.load_texture(
                ":resources:images/animated_characters/male_person/malePerson_idle.png"
            )
        else:
            self.texture = arcade.load_texture(
                ":resources:images/enemies/slimeBlock.png"
            )

    def update_ai(self, player, delta_time):
        """Искусственный интеллект врага"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

        # Движение к игроку
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y

        # Нормализация направления
        distance = max(0.1, math.hypot(dx, dy))
        if distance > 0:
            dx = (dx / distance) * self.speed * delta_time
            dy = (dy / distance) * self.speed * delta_time

        # Обновление позиции
        self.center_x += dx
        self.center_y += dy

        # Поворот в сторону игрока
        if dx != 0 or dy != 0:
            self.angle = math.degrees(math.atan2(dy, dx))

    def take_damage(self, damage):
        """Получение урона"""
        self.health -= damage
        return self.health <= 0