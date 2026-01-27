"""
Классы оружия и снарядов
"""

import arcade
import math
from config import *

class Bullet(arcade.Sprite):
    """Класс пули"""
    
    def __init__(self):
        super().__init__()
        
        self.texture = arcade.load_texture(
            ":resources:images/space_shooter/laserBlue01.png"
        )
        self.scale = 0.5
        self.speed = BULLET_SPEED
        self.damage = BULLET_DAMAGE
        
        # Направление движения
        self.change_x = 0
        self.change_y = 0
        
    def set_direction(self, target_x, target_y):
        """Установка направления движения к цели"""
        dx = target_x - self.center_x
        dy = target_y - self.center_y
        
        # Нормализация
        distance = max(0.1, math.hypot(dx, dy))
        self.change_x = (dx / distance) * self.speed
        self.change_y = (dy / distance) * self.speed

        # Поворот спрайта в направлении движения (правильный расчет)
        self.angle = math.degrees(math.atan2(dy, dx))

    def update(self, delta_time=1/60):
        """Обновление позиции пули"""
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        # Удаление пули, если она вышла за пределы экрана
        margin = 100
        if (self.center_x < -margin or self.center_x > SCREEN_WIDTH + margin or
            self.center_y < -margin or self.center_y > SCREEN_HEIGHT + margin):
            self.remove_from_sprite_lists()