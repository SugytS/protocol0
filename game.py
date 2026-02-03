"""
Основной класс игры (с дверью в центре карты и меню улучшений)
"""

import arcade
import math
import random
from config import *
from player import Player
from enemy import Enemy
from level_generator import LevelGenerator
from weapon import Bullet
from items import Item
from crate import Crate

class DungeonGame(arcade.View):
    """Главный класс игры как View"""
    
    def __init__(self):
        super().__init__()
        
        # Игровые объекты
        self.player = None
        self.level_generator = None
        self.current_level = None
        self.current_room = None

        # Списки для рисования
        self.wall_list = None
        self.floor_list = None
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None
        self.enemy_bullet_list = None
        self.item_list = None
        self.door_list = None
        self.crate_list = None

        # Управление
        self.keys_pressed = set()
        self.mouse_position = (0, 0)

        # Состояние игры
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.room_cleared = False
        self.showing_upgrade_menu = False

        # Таймеры
        self.fire_timer = 0

        self.setup()

    def setup(self):
        """Настройка начального состояния игры"""
        print(f"Запуск уровня {self.level}")

        # Инициализируем списки спрайтов
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.crate_list = arcade.SpriteList()

        # Создаем игрока
        self.player = Player()
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)

        # Генерируем уровень
        self.level_generator = LevelGenerator(self.level)
        self.current_level = self.level_generator.generate_level()
        self.current_room = self.current_level['rooms'][0]
        self.load_room(self.current_room)

        print("Настройка завершена")

    def load_room(self, room_data):
        """Загрузка комнаты из данных"""
        # Очищаем списки
        self.wall_list.clear()
        self.floor_list.clear()
        self.enemy_list.clear()
        self.bullet_list.clear()
        self.enemy_bullet_list.clear()
        self.item_list.clear()
        self.door_list.clear()
        self.crate_list.clear()

        # Добавляем стены и пол
        for tile in room_data["walls"]:
            wall = arcade.Sprite()
            wall.texture = arcade.make_soft_square_texture(TILE_SIZE, WALL_COLOR)
            wall.center_x = tile[0] * TILE_SIZE + TILE_SIZE // 2
            wall.center_y = tile[1] * TILE_SIZE + TILE_SIZE // 2
            self.wall_list.append(wall)

        for tile in room_data["floor"]:
            floor = arcade.Sprite()
            floor.texture = arcade.make_soft_square_texture(TILE_SIZE, FLOOR_COLOR)
            floor.center_x = tile[0] * TILE_SIZE + TILE_SIZE // 2
            floor.center_y = tile[1] * TILE_SIZE + TILE_SIZE // 2
            self.floor_list.append(floor)

        # Добавляем ящики (черные прямоугольники)
        for crate_pos in room_data["crates"]:
            crate = Crate()
            crate.center_x = crate_pos[0] * TILE_SIZE + TILE_SIZE // 2
            crate.center_y = crate_pos[1] * TILE_SIZE + TILE_SIZE // 2
            self.crate_list.append(crate)

        # Добавляем врагов
        for enemy_data in room_data["enemies"]:
            enemy = Enemy(enemy_data["type"], self.level)
            enemy.center_x = enemy_data["x"]
            enemy.center_y = enemy_data["y"]
            self.enemy_list.append(enemy)

        # Добавляем дверь в SpriteList (но она пока невидима)
        if "door" in room_data:
            door_sprite = arcade.Sprite()
            # Создаем яркую красную текстуру для двери
            door_sprite.texture = arcade.make_soft_square_texture(60, arcade.color.RED)
            door_sprite.width = room_data["door"].get("width", 60)
            door_sprite.height = room_data["door"].get("height", 40)
            door_sprite.center_x = room_data["door"]["x"]
            door_sprite.center_y = room_data["door"]["y"]
            door_sprite.destination_room = room_data["door"]["destination"]
            door_sprite.visible = False  # Дверь невидима до зачистки комнаты
            self.door_list.append(door_sprite)
            print(f"Дверь создана в центре комнаты ({door_sprite.center_x}, {door_sprite.center_y})")

        # Добавляем предметы
        self.spawn_items()

        # Позиция игрока (немного выше центра, чтобы не стоять на двери)
        if "start_x" in room_data and "start_y" in room_data:
            self.player.center_x = room_data["start_x"]
            self.player.center_y = room_data["start_y"]
        else:
            self.player.center_x = SCREEN_WIDTH // 2
            self.player.center_y = SCREEN_HEIGHT // 2 + 100

        self.room_cleared = False
        self.showing_upgrade_menu = False

    def spawn_items(self):
        """Создание предметов в комнате"""
        for _ in range(5):
            coin = Item("coin")
            attempts = 0
            while attempts < 10:
                coin.center_x = random.randint(100, SCREEN_WIDTH - 100)
                coin.center_y = random.randint(100, SCREEN_HEIGHT - 100)

                # Не спавним предметы в центре (где будет дверь)
                if abs(coin.center_x - SCREEN_WIDTH // 2) > 50 and abs(coin.center_y - SCREEN_HEIGHT // 2) > 50:
                    wall_collision = arcade.check_for_collision_with_list(coin, self.wall_list)
                    crate_collision = arcade.check_for_collision_with_list(coin, self.crate_list)

                    if not wall_collision and not crate_collision:
                        self.item_list.append(coin)
                        break
                attempts += 1

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()

        # Рисуем в правильном порядке
        self.floor_list.draw()
        self.wall_list.draw()
        self.crate_list.draw()
        self.item_list.draw()
        self.enemy_list.draw()

        # Рисуем дверь, если она есть и видима
        self.door_list.draw()

        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()

        # Рисуем UI
        self.draw_ui()

        # Убрали отрисовку "GAME OVER" здесь, так как теперь переключаемся на GameOverView

    def draw_ui(self):
        """Отрисовка интерфейса"""
        # Здоровье
        arcade.draw_text(f"HP: {self.player.health}/{self.player.max_health}",
                        10, SCREEN_HEIGHT - 30, UI_COLOR, 20)

        # Патроны
        arcade.draw_text(f"Ammo: {self.player.ammo}",
                        10, SCREEN_HEIGHT - 60, UI_COLOR, 20)

        # Счет
        arcade.draw_text(f"Score: {self.score}",
                        SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30, UI_COLOR, 20)

        # Уровень
        arcade.draw_text(f"Level: {self.level}",
                        SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, UI_COLOR, 20)

        # Множитель урона
        arcade.draw_text(f"Damage: {self.player.damage_multiplier:.1f}x",
                        10, SCREEN_HEIGHT - 90, UI_COLOR, 20)

        # Номер комнаты
        room_num = 1
        for i, room in enumerate(self.current_level['rooms']):
            if room == self.current_room:
                room_num = i + 1
                break
        arcade.draw_text(f"Room: {room_num}/{len(self.current_level['rooms'])}",
                        SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 30, UI_COLOR, 20)

    def on_update(self, delta_time):
        """Обновление игровой логики"""
        if self.game_over or self.paused or self.showing_upgrade_menu:
            return

        if self.fire_timer > 0:
            self.fire_timer -= delta_time

        # Обновляем игрока
        self.player.update(delta_time, self.keys_pressed)

        # Проверяем столкновения игрока со стенами и ящиками
        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x -= self.player.change_x
            self.player.center_y -= self.player.change_y

        if arcade.check_for_collision_with_list(self.player, self.crate_list):
            self.player.center_x -= self.player.change_x
            self.player.center_y -= self.player.change_y

        # Обновляем врагов
        for enemy in self.enemy_list:
            enemy.update_ai(self.player, delta_time, self.enemy_bullet_list)

        # Обновляем пули
        for bullet in self.bullet_list:
            bullet.update(delta_time)
        for bullet in self.enemy_bullet_list:
            bullet.update(delta_time)

        # Проверяем столкновения
        self.check_collisions()

        # Проверяем очистку комнаты
        if len(self.enemy_list) == 0 and not self.room_cleared:
            self.room_cleared = True
            # Делаем дверь видимой и зеленой
            if len(self.door_list) > 0:
                self.door_list[0].visible = True
                self.door_list[0].texture = arcade.make_soft_square_texture(60, arcade.color.GREEN)  # Зеленая дверь
            print("Комната очищена! Дверь открыта в центре комнаты.")

        # Проверяем смерть игрока - ПЕРЕНОСИМ В ОТДЕЛЬНЫЙ МЕТОД
        if self.player.health <= 0:
            self.handle_game_over()

    def handle_game_over(self):
        """Обработка завершения игры"""
        self.game_over = True
        self.paused = True
        
        # Импортируем здесь, чтобы избежать циклического импорта
        from menu import GameOverView
        game_over_view = GameOverView(self.score, self.level, self.window)
        self.window.show_view(game_over_view)

    def check_collisions(self):
        """Проверка всех столкновений"""
        # Пули игрока с врагами (с учетом множителя урона)
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in hit_list:
                actual_damage = bullet.damage * self.player.damage_multiplier
                enemy.take_damage(actual_damage)
                bullet.remove_from_sprite_lists()
                if enemy.health <= 0:
                    enemy.remove_from_sprite_lists()
                    self.score += 10

        # Пули игрока с ящиками
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.crate_list)
            for crate in hit_list:
                if crate.take_damage(bullet.damage):
                    crate.remove_from_sprite_lists()
                    self.score += 5
                bullet.remove_from_sprite_lists()

        # Пули врагов с игроком
        for bullet in self.enemy_bullet_list:
            if arcade.check_for_collision(bullet, self.player):
                self.player.take_damage(bullet.damage)
                bullet.remove_from_sprite_lists()

        # Игрок с врагами (ближний бой)
        hit_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for enemy in hit_list:
            if enemy.attack_cooldown <= 0:
                self.player.take_damage(10)
                enemy.attack_cooldown = 1.0
            else:
                enemy.attack_cooldown -= 0.016

        # Игрок с предметами
        hit_list = arcade.check_for_collision_with_list(self.player, self.item_list)
        for item in hit_list:
            item.collect(self.player)
            item.remove_from_sprite_lists()
            self.score += ITEM_SCORES.get(item.type, 0)

        # Игрок с дверью (только если комната очищена и дверь видима)
        if self.room_cleared and len(self.door_list) > 0 and self.door_list[0].visible:
            if arcade.check_for_collision(self.player, self.door_list[0]):
                self.transition_to_room(self.door_list[0].destination_room)

        # Удаление пуль при столкновении со стенами
        for bullet in self.bullet_list:
            if arcade.check_for_collision_with_list(bullet, self.wall_list):
                bullet.remove_from_sprite_lists()

        for bullet in self.enemy_bullet_list:
            if arcade.check_for_collision_with_list(bullet, self.wall_list):
                bullet.remove_from_sprite_lists()

    def transition_to_room(self, room_index):
        """Переход в указанную комнату или на следующий уровень"""
        print(f"Переход: {room_index}")

        # Если room_index = -1, это последняя комната уровня
        if room_index == -1:
            print("Последняя комната уровня пройдена! Показываем меню улучшений.")
            self.show_upgrade_menu()
            return

        # Ищем комнату по индексу
        for room in self.current_level['rooms']:
            if room['id'] == room_index:
                self.current_room = room
                self.load_room(room)
                print(f"Переход в комнату {room_index}")
                return

    def show_upgrade_menu(self):
        """Показать меню улучшений"""
        self.showing_upgrade_menu = True
        self.paused = True

        # Импортируем здесь, чтобы избежать циклического импорта
        from menu import UpgradeMenuView
        upgrade_menu = UpgradeMenuView(self, self.apply_upgrade_and_continue)
        self.window.show_view(upgrade_menu)

    def apply_upgrade_and_continue(self, upgrade_type, value):
        """Применить улучшение и перейти на следующий уровень"""
        result = self.player.apply_upgrade(upgrade_type, value)
        print(f"Применено улучшение: {result}")

        # Возвращаемся в игру и переходим на следующий уровень
        self.showing_upgrade_menu = False
        self.paused = False
        self.next_level()

    def next_level(self):
        """Переход на следующий уровень"""
        self.level += 1
        print(f"Переход на уровень {self.level}")

        # Даем бонус за прохождение уровня
        self.player.heal(self.player.max_health * 0.5)  # Восстанавливаем 50% здоровья
        self.player.add_ammo(50)
        self.score += 500 * (self.level - 1)  # Бонусные очки

        # Генерируем новый уровень
        self.level_generator = LevelGenerator(self.level)
        self.current_level = self.level_generator.generate_level()
        self.current_room = self.current_level['rooms'][0]
        self.load_room(self.current_room)

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.P:
            self.paused = not self.paused
        elif key == arcade.key.R and self.game_over:
            self.setup()
        elif key == arcade.key.N:  # Для тестирования: принудительный переход на следующий уровень
            self.level += 1
            self.setup()

        movement_keys = {
            arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D,
            arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT
        }
        if key in movement_keys:
            self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_motion(self, x, y, dx, dy):
        """Обработка движения мыши"""
        self.mouse_position = (x, y)

        if self.player:
            delta_x = x - self.player.center_x
            delta_y = y - self.player.center_y
            self.player.angle = math.degrees(math.atan2(delta_y, delta_x))

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка нажатия кнопки мыши"""
        if button == arcade.MOUSE_BUTTON_LEFT and not self.game_over and not self.paused and not self.showing_upgrade_menu:
            self.fire_bullet()

    def fire_bullet(self):
        """Создание пули игрока"""
        if self.fire_timer <= 0 and self.player.ammo > 0:
            bullet = Bullet()
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y

            # Направляем пулю в курсор мыши
            bullet.set_direction(
                self.player.center_x, self.player.center_y,
                self.mouse_position[0], self.mouse_position[1]
            )

            # Учитываем множитель урона игрока
            bullet.damage = BULLET_DAMAGE * self.player.damage_multiplier

            self.bullet_list.append(bullet)

            self.fire_timer = FIRE_RATE
            self.player.ammo -= 1
