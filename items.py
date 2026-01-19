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
        
        # Загрузка текстур в зависимости от типа
        if item_type == "coin":
            self.texture = arcade.load_texture(
                ":resources:images/items/coinGold.png"
            )
            self.value = 10
        elif item_type == "health":
            self.texture = arcade.load_texture(
                ":resources:images/items/health.png"
            )
            self.value = 25
        elif item_type == "ammo":
            self.texture = arcade.load_texture(
                ":resources:images/items/ammo.png"
            )
            self.value = 15
        else:
            self.texture = arcade.load_texture(
                ":resources:images/items/gemBlue.png"
            )
            self.value = 5
        
        self.scale = 0.5
        
    def collect(self, player):
        """Сбор предмета игроком"""
        if self.type == "coin":
            player.score += self.value
        elif self.type == "health":
            player.heal(self.value)
        elif self.type == "ammo":
            player.add_ammo(self.value)
            
        return True
