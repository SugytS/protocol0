"""
Генерация комнат
"""

import random
from config import *

class RoomGenerator:
    """Генератор комнат"""

    def __init__(self):
        self.room_counter = 0

    def generate_room(self):
        """Генерация одной комнаты"""
        room = {
            "id": self.room_counter,
            "width": ROOM_WIDTH,
            "height": ROOM_HEIGHT,
            "walls": [],
            "floor": [],
            "enemies": [],
            "items": [],
            "crates": [],
        }

        self.room_counter += 1

        # Заполняем пол
        for x in range(ROOM_WIDTH):
            for y in range(ROOM_HEIGHT):
                room["floor"].append((x, y))

        # Добавляем стены по краям (полностью закрытая комната)
        for x in range(ROOM_WIDTH):
            # Нижняя стена
            room["walls"].append((x, 0))
            # Верхняя стена
            room["walls"].append((x, ROOM_HEIGHT - 1))

        for y in range(ROOM_HEIGHT):
            # Левая стена
            room["walls"].append((0, y))
            # Правая стена
            room["walls"].append((ROOM_WIDTH - 1, y))

        # Добавляем ящики (препятствия) - но не в центре комнаты
        crate_count = random.randint(3, 8)
        for _ in range(crate_count):
            # Ставим ящик так, чтобы не блокировать центр комнаты
            x = random.randint(2, ROOM_WIDTH - 3)
            y = random.randint(2, ROOM_HEIGHT - 3)

            # Не ставим ящики в центре комнаты (место для двери)
            center_x = ROOM_WIDTH // 2
            center_y = ROOM_HEIGHT // 2
            if abs(x - center_x) > 1 or abs(y - center_y) > 1:
                if (x, y) not in room["walls"]:
                    room["crates"].append((x, y))

        # Добавляем врагов
        enemy_count = random.randint(3, 8)
        for i in range(enemy_count):
            # Выбираем тип врага
            if i == enemy_count - 1 and enemy_count > 4:
                enemy_type = "tank"
            elif i % 3 == 0:
                enemy_type = "ranged"
            else:
                enemy_type = "melee"

            # Генерируем позицию, избегая стен и ящиков
            attempts = 0
            while attempts < 20:
                x = random.randint(2, ROOM_WIDTH - 3) * TILE_SIZE + TILE_SIZE // 2
                y = random.randint(2, ROOM_HEIGHT - 3) * TILE_SIZE + TILE_SIZE // 2

                # Проверяем, не в центре ли комнаты (место для двери)
                center_x = SCREEN_WIDTH // 2
                center_y = SCREEN_HEIGHT // 2
                if abs(x - center_x) > 50 and abs(y - center_y) > 50:
                    # Проверяем, не на стене ли и не на ящике
                    tile_x = int(x / TILE_SIZE)
                    tile_y = int(y / TILE_SIZE)
                    if ((tile_x, tile_y) not in room["walls"] and
                        (tile_x, tile_y) not in room["crates"]):
                        room["enemies"].append({
                            "type": enemy_type,
                            "x": x,
                            "y": y
                        })
                        break
                attempts += 1

        return room