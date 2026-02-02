"""
Классы предметов
"""

import arcade
import random
from config import *

class Item(arcade.Sprite):
    """Базовый класс предмета"""
    
    def __init__(self, item_type="coin"):
        super().__init__()
        
        self.type = item_type
        self.value = ITEM_VALUES.get(item_type, 10)

        # Загрузка текстур в зависимости от типа
        if item_type == "coin":
            # Используем существующую текстуру монеты
            self.texture = arcade.load_texture(
                ":resources:images/items/coinGold.png"
            )
            self.scale = 0.5
        elif item_type == "health":
            # Для здоровья используем красный сердечко-подобный спрайт
            # Можно использовать текстуру из других ресурсов
            try:
                self.texture = arcade.load_texture(
                    ":resources:images/items/coinGold_ul.png"
                )
            except:
                # Если текстура не найдена, создаем цветной спрайт
                self.texture = arcade.make_soft_square_texture(30, arcade.color.RED)
            self.scale = 0.7
        elif item_type == "ammo":
            # Для патронов используем синий спрайт
            try:
                self.texture = arcade.load_texture(
                    ":resources:images/items/coinSilver.png"
                )
            except:
                self.texture = arcade.make_soft_square_texture(30, arcade.color.BLUE)
            self.scale = 0.7
        else:
            # По умолчанию - золотая монета
            self.texture = arcade.load_texture(
                ":resources:images/items/coinGold.png"
            )
            self.scale = 0.5

    def collect(self, player):
        """Сбор предмета игроком"""
        if self.type == "coin":
            player.score += self.value
            print(f"Собрана монета! +{self.value} очков")
        elif self.type == "health":
            player.heal(self.value)
            print(f"Собрано здоровье! +{self.value} HP")
        elif self.type == "ammo":
            player.add_ammo(self.value)
            print(f"Собраны патроны! +{self.value} патронов")

        return True