"""
Класс ящиков-препятствий
"""

import arcade
from config import *

class Crate(arcade.Sprite):
    """Класс ящика-препятствия"""

    def __init__(self):
        super().__init__()

        # Используем текстуру деревянного ящика из ресурсов
        try:
            self.texture = arcade.load_texture(
                ":resources:images/tiles/boxCrate_double.png"
            )
        except:
            # Если текстура не найдена, создаем коричневый прямоугольник
            self.texture = arcade.make_soft_square_texture(
                TILE_SIZE, arcade.color.BROWN
            )

        self.scale = 0.5
        self.health = 50

    def take_damage(self, damage):
        """Получение урона ящиком"""
        self.health -= damage
        return self.health <= 0
