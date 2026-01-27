import arcade

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Dungeon Shooter"

TILE_SIZE = 64
ROOM_WIDTH = 20
ROOM_HEIGHT = 15

BACKGROUND_COLOR = arcade.color.DARK_SLATE_GRAY
WALL_COLOR = arcade.color.DARK_BROWN
#FLOOR_COLOR = arcade.color.DARK_SLATE_GREY
FLOOR_COLOR = (47, 79, 79)
UI_COLOR = arcade.color.GOLDEN_YELLOW

PLAYER_SPEED = 300
PLAYER_HEALTH = 100
PLAYER_STARTING_AMMO = 50

BULLET_SPEED = 800
BULLET_DAMAGE = 20
FIRE_RATE = 0.2

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

ITEM_SCORES = {
    "coin": 10,
    "health": 0,
    "ammo": 0
}

MIN_ROOMS = 3
MAX_ROOMS = 8
ROOM_TYPES = ["normal", "treasure", "boss"]