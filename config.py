"""
Конфигурационные константы игры Dungeon Shooter
"""

import arcade
import random

# Размеры окна
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Dungeon Shooter"

# Игровые константы
TILE_SIZE = 64
ROOM_WIDTH = SCREEN_WIDTH // TILE_SIZE  # 16
ROOM_HEIGHT = SCREEN_HEIGHT // TILE_SIZE  # 12

# Цвета
BACKGROUND_COLOR = arcade.color.DARK_SLATE_GRAY
WALL_COLOR = arcade.color.DARK_BROWN
FLOOR_COLOR = arcade.color.DARK_SLATE_GRAY
UI_COLOR = arcade.color.GOLDEN_YELLOW

# Настройки игрока
PLAYER_SPEED = 300
PLAYER_HEALTH = 100
PLAYER_STARTING_AMMO = 50

# Настройки оружия
BULLET_SPEED = 800
BULLET_DAMAGE = 20
FIRE_RATE = 0.2  # Секунд между выстрелами

# Настройки врагов
ENEMY_SPEEDS = {
    "melee": 150,
    "ranged": 100,
    "tank": 80,
    "boss": 120
}

ENEMY_HEALTH = {
    "melee": 30,
    "ranged": 25,
    "tank": 100,
    "boss": 200
}

# Настройки предметов
ITEM_SCORES = {
    "coin": 10,
    "health": 0,
    "ammo": 0
}

ITEM_VALUES = {
    "coin": 10,
    "health": 25,
    "ammo": 15
}

# Настройки уровней
LEVELS_CONFIG = {
    1: {"rooms": 3, "boss_room": 3},
    2: {"rooms": 4, "boss_room": 4},
    3: {"rooms": 5, "boss_room": 5},
    4: {"rooms": 6, "boss_room": 6},
    5: {"rooms": 7, "boss_room": 7},
    6: {"rooms": 8, "boss_room": 8},
    7: {"rooms": 9, "boss_room": 9},
    8: {"rooms": 10, "boss_room": 10},
    9: {"rooms": 12, "boss_room": 12},
    10: {"rooms": 15, "boss_room": 15}
}