import arcade
import math
import random

class Enemy:
    def __init__(self):
        self.sprite = arcade.SpriteCircle(25, arcade.color.RED)
        self.center_x = 0
        self.center_y = 0
        self.health = 30
        self.max_health = 30
        self.damage = 5
        self.speed = 2
        self.attack_range = 50
        self.attack_cooldown = 0
        
    @property
    def center_x(self):
        return self.sprite.center_x
    
    @center_x.setter
    def center_x(self, value):
        self.sprite.center_x = value
        
    @property
    def center_y(self):
        return self.sprite.center_y
    
    @center_y.setter
    def center_y(self, value):
        self.sprite.center_y = value
    
    def update(self, player):
        # Движение к игроку
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # Если враг слишком близко к игроку, отступаем
        if distance < 50:
            self.center_x -= (dx / distance) * self.speed
            self.center_y -= (dy / distance) * self.speed
        else:
            # Двигаемся к игроку
            self.center_x += (dx / distance) * self.speed
            self.center_y += (dy / distance) * self.speed
        
        # Обновляем cooldown атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
    
    def draw(self):
        self.sprite.draw() 