"""
Генератор уровней с соединёнными комнатами
"""

import random
from room import RoomGenerator
from config import *


class LevelGenerator:
    """Генератор уровней"""

    def __init__(self, level_number):
        self.level = level_number
        self.room_generator = RoomGenerator()

    def generate_level(self):
        """Генерация уровня с соединёнными комнатами"""
        # Для первого уровня - 1 комната, затем добавляем по 1 комнате каждые 2 уровня
        room_count = max(1, 1 + (self.level - 1) // 2)
        print(f"Генерация уровня {self.level} с {room_count} комнатами")

        level = {
            "level": self.level,
            "rooms": []
        }

        # Генерируем комнаты
        rooms = []
        for i in range(room_count):
            room = self.room_generator.generate_room()
            room["id"] = i
            # В каждой комнате будет дверь в центре, ведущая в следующую комнату
            room["door"] = {
                "destination": i + 1 if i < room_count - 1 else -1,  # -1 для последней комнаты (конец уровня)
                "x": SCREEN_WIDTH // 2,  # Центр экрана
                "y": SCREEN_HEIGHT // 2,  # Центр экрана
                "width": 60,  # Ширина двери
                "height": 40   # Высота двери
            }
            rooms.append(room)

        # Начальная позиция в первой комнате (немного выше центра, чтобы не стоять на двери)
        if rooms:
            rooms[0]["start_x"] = SCREEN_WIDTH // 2
            rooms[0]["start_y"] = SCREEN_HEIGHT // 2 + 100

        level["rooms"] = rooms
        return level