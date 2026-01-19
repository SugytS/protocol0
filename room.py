"""
Генерация комнат и уровней
"""

import random
from config import *

class RoomGenerator:
    """Генератор комнат"""
    
    def __init__(self):
        self.rooms = []
        self.current_level = 1
        
    def generate_room(self):
        """Генерация одной комнаты"""
        room = {
            "width": ROOM_WIDTH,
            "height": ROOM_HEIGHT,
            "walls": [],
            "floor": [],
            "enemies": [],
            "items": []
        }
        
        # Заполняем пол
        for x in range(ROOM_WIDTH):
            for y in range(ROOM_HEIGHT):
                room["floor"].append((x, y))
        
        # Добавляем стены по краям
        for x in range(ROOM_WIDTH):
            room["walls"].append((x, 0))  # Нижняя стена
            room["walls"].append((x, ROOM_HEIGHT - 1))  # Верхняя стена
        for y in range(ROOM_HEIGHT):
            room["walls"].append((0, y))  # Левая стена
            room["walls"].append((ROOM_WIDTH - 1, y))  # Правая стена
        
        # Добавляем несколько внутренних стен
        for _ in range(random.randint(3, 8)):
            x = random.randint(2, ROOM_WIDTH - 3)
            y = random.randint(2, ROOM_HEIGHT - 3)
            room["walls"].append((x, y))
        
        # Добавляем врагов
        enemy_count = random.randint(3, 8)
        for _ in range(enemy_count):
            enemy_type = random.choice(["melee", "ranged", "tank"])
            x = random.randint(2, ROOM_WIDTH - 3) * TILE_SIZE + TILE_SIZE // 2
            y = random.randint(2, ROOM_HEIGHT - 3) * TILE_SIZE + TILE_SIZE // 2
            room["enemies"].append({
                "type": enemy_type,
                "x": x,
                "y": y
            })
        
        return room
    
    def generate_level(self, room_count=None):
        """Генерация уровня из нескольких комнат"""
        if room_count is None:
            room_count = random.randint(MIN_ROOMS, MAX_ROOMS)
        
        level = {
            "rooms": [],
            "connections": []
        }
        
        for i in range(room_count):
            room_type = random.choice(ROOM_TYPES)
            if i == room_count - 1:  # Последняя комната - босс
                room_type = "boss"
            elif i == 0:  # Первая комната - стартовая
                room_type = "start"
            
            room = self.generate_room()
            room["type"] = room_type
            level["rooms"].append(room)
        
        return level
