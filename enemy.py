"""
Классы врагов
"""

import arcade
import random
import math
from config import *
from weapon import Bullet

class Enemy(arcade.Sprite):
    """Базовый класс врага"""

    def __init__(self, enemy_type="melee", level=1):
        super().__init__()

        self.type = enemy_type
        self.level = level

        # Масштабируем характеристики в зависимости от уровня
        base_speed = ENEMY_SPEEDS.get(enemy_type, 100)
        base_health = ENEMY_HEALTH.get(enemy_type, 30)

        self.speed = base_speed * (1 + (level - 1) * 0.1)
        self.max_health = base_health * (1 + (level - 1) * 0.15)
        self.health = self.max_health
        self.attack_damage = 10 * (1 + (level - 1) * 0.1)
        self.attack_cooldown = 0

        # Для стреляющих врагов
        self.shoot_timer = 0
        self.shoot_cooldown = 2.0

        # Загрузка текстур
        if enemy_type == "melee":
            self.texture = arcade.load_texture(
                ":resources:images/animated_characters/zombie/zombie_idle.png"
            )
            self.scale = 0.8
        elif enemy_type == "ranged":
            self.texture = arcade.load_texture(
                ":resources:images/animated_characters/robot/robot_idle.png"
            )
            self.scale = 0.7
            self.shoot_cooldown = 1.5
        elif enemy_type == "tank":
            self.scale = 1.2
            self.texture = arcade.load_texture(
                ":resources:images/animated_characters/robot/robot_idle.png"
            )
        elif enemy_type == "boss":
            self.scale = 1.8
            self.texture = arcade.load_texture(
                ":resources:images/animated_characters/male_person/malePerson_idle.png"
            )
        else:
            self.texture = arcade.load_texture(
                ":resources:images/enemies/slimeBlock.png"
            )

    def update_ai(self, player, delta_time, enemy_bullet_list=None):
        """Искусственный интеллект врага"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

        if self.type == "ranged":
            if self.shoot_timer > 0:
                self.shoot_timer -= delta_time

        # Движение к игроку
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = max(0.1, math.hypot(dx, dy))

        # Поворот в сторону игрока
        if dx != 0 or dy != 0:
            self.angle = math.degrees(math.atan2(dy, dx))

        # Разное поведение для разных типов
        if self.type == "ranged":
            # Стреляющие враги держат дистанцию
            if distance > 300:
                move_factor = 1.0
            elif distance < 200:
                move_factor = -0.5
            else:
                move_factor = 0

            # Стрельба
            if self.shoot_timer <= 0 and distance < 400 and enemy_bullet_list is not None:
                self.shoot(player, enemy_bullet_list)
                self.shoot_timer = self.shoot_cooldown
        else:
            move_factor = 1.0

        # Движение
        if distance > 0 and move_factor != 0:
            dx = (dx / distance) * self.speed * delta_time * move_factor
            dy = (dy / distance) * self.speed * delta_time * move_factor

            self.center_x += dx
            self.center_y += dy

    def shoot(self, player, bullet_list):
        """Стрельба врага"""
        bullet = Bullet()
        bullet.center_x = self.center_x
        bullet.center_y = self.center_y

        bullet.set_direction(
            self.center_x, self.center_y,
            player.center_x, player.center_y
        )

        bullet.damage = self.attack_damage * 0.7
        bullet_list.append(bullet)

    def take_damage(self, damage):
        """Получение урона"""
        self.health -= damage
        return self.health <= 0