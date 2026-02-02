"""
Класс ящиков-препятствий
"""

import arcade
from config import *

class Crate(arcade.Sprite):
    """Класс ящика-препятствия"""

    def __init__(self):
        super().__init__()

        # Создаем черный прямоугольник
        self.texture = arcade.make_soft_square_texture(
            TILE_SIZE, arcade.color.BLACK
        )

        self.scale = 1.0
        self.health = 50

    def take_damage(self, damage):
        """Получение урона ящиком"""
        self.health -= damage
        return self.health <= 0